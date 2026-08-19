#!/usr/bin/env python3
"""Build deterministic online and offline guide artifacts using only the standard library."""

from __future__ import annotations

import argparse
import functools
import hashlib
import html
import html.parser
import json
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent
GUIDE_SOURCE = ROOT / "guide-src"
OFFLINE_SOURCE = ROOT / "offline-package" / "src"
DIST = ROOT / "dist"
WORDLIST_SOURCE = ROOT / "additional_ressources" / "BIP39_Wordlist_Binary_Decimal_Searchable.ods"
WORDLIST_SOURCE_SHA256 = "967bb0b0cb39fdbaede6186cfb6f732f1979e072495ffb48e2d453ee92a2c542"
WORDLIST_NORMALIZED_SHA256 = "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda"
SHA256_SOURCE_SHA256 = "e9540c4fe6fa3cb5edd0eeb2ef2c80f6c5107b3e75f9789263c2e4922275b444"
SHELL_OPENING = Path("shared/00-shell-opening.html")
STEP_0_OFFLINE = Path("offline/05-step-00-air-gap.html")
STEP_1 = Path("shared/10-step-01-prepare.html")
STEP_2 = Path("shared/20-step-02-decide.html")
STEP_3 = Path("shared/30-step-03-roll.html")
STEP_4 = Path("shared/40-step-04-lookup.html")
STEP_3_4_OFFLINE = Path("offline/30-step-03-dice-bits.html")  # combined dice-entry + lookup
STEP_5_ONLINE = Path("online/50-step-05-wallet.html")
STEP_6 = Path("shared/60-step-06-complete.html")
SHELL_ENDING = Path("shared/70-shell-ending.html")
CATALOG_SOURCE = GUIDE_SOURCE / "i18n" / "catalog.json"
HTML_TOKEN_RE = re.compile(r"(<!--.*?-->|<![^>]*>|<[^>]*>)", flags=re.DOTALL)
ATTRIBUTE_RE = re.compile(
    r"(?P<name>[A-Za-z_:][A-Za-z0-9:_.-]*)(?P<equals>\s*=\s*)(?P<quote>['\"])(?P<value>.*?)(?P=quote)",
    flags=re.DOTALL,
)
ONLINE_FRAGMENTS = (
    SHELL_OPENING,
    STEP_1,
    STEP_2,
    STEP_3,
    STEP_4,
    STEP_5_ONLINE,
    STEP_6,
    SHELL_ENDING,
)
OFFLINE_FRAGMENTS = (
    SHELL_OPENING,
    STEP_0_OFFLINE,
    STEP_1,
    STEP_2,
    STEP_3_4_OFFLINE,
    STEP_6,
    SHELL_ENDING,
)
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)
GENERATED_FILE_NOTICE = "<!-- GENERATED FILE — DO NOT EDIT. Edit guide-src/ and run python3 build-guides.py online. -->"
LOCALIZED_PRINTOUTS = frozenset({"BitsToWords.pdf", "HowToRollYourOwnSeedphrase.pdf"})


@dataclass(frozen=True)
class Locale:
    code: str
    output_directory: str
    print_suffix: str


LOCALES = {
    "en": Locale("en", "online", ""),
    "de": Locale("de", "de", "-de"),
}


class BuildError(RuntimeError):
    """A deterministic build or security invariant failed."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(path: Path) -> str:
    if not path.is_file():
        raise BuildError(f"Required source file is missing: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_hash(path: Path, expected: str) -> None:
    actual = digest(path.read_bytes())
    if actual != expected:
        raise BuildError(
            f"Pinned source changed: {path.relative_to(ROOT)}\n"
            f"expected {expected}\nactual   {actual}"
        )


def extract_wordlist() -> list[str]:
    require_hash(WORDLIST_SOURCE, WORDLIST_SOURCE_SHA256)
    with zipfile.ZipFile(WORDLIST_SOURCE) as archive:
        root = ElementTree.fromstring(archive.read("content.xml"))

    indexed: dict[int, str] = {}
    pattern = re.compile(r"(\d+)\s*[-–]\s*[01-]+\s*:\s*([a-z]+)")
    for cell in (element for element in root.iter() if element.tag.endswith("}table-cell")):
        match = pattern.fullmatch("".join(cell.itertext()).strip())
        if match:
            index = int(match.group(1))
            word = match.group(2)
            if index in indexed and indexed[index] != word:
                raise BuildError(f"Conflicting words found for BIP39 index {index}.")
            indexed[index] = word

    if not indexed:
        pages: dict[int, ElementTree.Element] = {}
        table_name = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name"
        for table in (element for element in root.iter() if element.tag.endswith("}table")):
            match = re.fullmatch(r"Page (\d+)", table.attrib.get(table_name, ""))
            if match:
                pages[int(match.group(1))] = table

        if set(pages) != set(range(1, 9)):
            raise BuildError("The redesigned BIP39 source is missing one or more Page 1–8 tables.")

        for page_number, table in pages.items():
            rows = [element for element in table if element.tag.endswith("}table-row")]
            if len(rows) < 33:
                raise BuildError(f"Page {page_number} does not contain 32 lookup rows.")
            for row_index, row in enumerate(rows[1:33]):
                cells = [
                    element for element in row
                    if element.tag.endswith("}table-cell") or element.tag.endswith("}covered-table-cell")
                ]
                if len(cells) < 19:
                    raise BuildError(f"Page {page_number}, lookup row {row_index} is incomplete.")
                for column_index in range(8):
                    index = (page_number - 1) * 256 + column_index * 32 + row_index
                    displayed_index = "".join(cells[3 + column_index * 2].itertext()).strip()
                    word = "".join(cells[4 + column_index * 2].itertext()).strip()
                    if displayed_index != str(index) or not re.fullmatch(r"[a-z]+", word):
                        raise BuildError(
                            f"Page {page_number}, column {column_index}, row {row_index} failed lookup validation."
                        )
                    indexed[index] = word

    if set(indexed) != set(range(2048)):
        missing = sorted(set(range(2048)) - set(indexed))
        raise BuildError(f"The BIP39 source does not contain exactly indices 0–2047; missing: {missing[:8]}")
    words = [indexed[index] for index in range(2048)]
    if len(set(words)) != 2048 or words[:4] != ["abandon", "ability", "able", "about"] or words[-4:] != ["zebra", "zero", "zone", "zoo"]:
        raise BuildError("The extracted English BIP39 list failed structure checks.")
    normalized = ("\n".join(words) + "\n").encode("ascii")
    if digest(normalized) != WORDLIST_NORMALIZED_SHA256:
        raise BuildError("The normalized English BIP39 list failed its pinned SHA-256 check.")
    return words


class LocalReferenceParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append(value)


def locale_config(locale_code: str) -> Locale:
    try:
        return LOCALES[locale_code]
    except KeyError as error:
        raise BuildError(f"Unsupported locale: {locale_code}") from error


@functools.cache
def translation_catalog() -> dict[str, object]:
    try:
        catalog = json.loads(read_text(CATALOG_SOURCE))
    except json.JSONDecodeError as error:
        raise BuildError(f"Translation catalog is not valid JSON: {CATALOG_SOURCE.relative_to(ROOT)}") from error
    if catalog.get("format") != 1 or not isinstance(catalog.get("fragments"), dict) or not isinstance(catalog.get("runtime"), dict):
        raise BuildError("Translation catalog has an unsupported structure.")
    return catalog


def translated_fragment(source: str, relative_path: Path, locale_code: str) -> str:
    if locale_code == "en":
        return source

    catalog = translation_catalog()
    entries = catalog["fragments"].get(relative_path.as_posix())
    if not isinstance(entries, list):
        raise BuildError(f"Translation catalog is missing {relative_path}.")

    text_values: dict[str, str] = {}
    attribute_values: dict[tuple[str, str], str] = {}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("kind") not in {"text", "attr"}:
            raise BuildError(f"Translation catalog has an invalid entry for {relative_path}.")
        english = entry.get("en")
        localized = entry.get(locale_code)
        if not isinstance(english, str) or not isinstance(localized, str):
            raise BuildError(f"Translation catalog has an incomplete {locale_code} entry for {relative_path}.")
        if entry["kind"] == "text":
            if text_values.setdefault(english, localized) != localized:
                raise BuildError(f"Translation catalog has ambiguous text for {relative_path}: {english!r}")
        else:
            name = entry.get("name")
            if not isinstance(name, str):
                raise BuildError(f"Translation catalog has an unnamed attribute for {relative_path}.")
            key = (name, english)
            if attribute_values.setdefault(key, localized) != localized:
                raise BuildError(f"Translation catalog has ambiguous attribute {name} for {relative_path}: {english!r}")

    def replace_attribute(match: re.Match[str]) -> str:
        name = match.group("name")
        value = html.unescape(match.group("value"))
        localized = attribute_values.get((name, value))
        if localized is None:
            return match.group(0)
        return f'{name}{match.group("equals")}{match.group("quote")}{html.escape(localized, quote=True)}{match.group("quote")}'

    def replace_tag(tag: str) -> str:
        return ATTRIBUTE_RE.sub(replace_attribute, tag)

    pieces = HTML_TOKEN_RE.split(source)
    for index in range(0, len(pieces), 2):
        english = html.unescape(pieces[index])
        if english in text_values:
            pieces[index] = html.escape(text_values[english], quote=False)
    for index in range(1, len(pieces), 2):
        pieces[index] = replace_tag(pieces[index])
    translated = "".join(pieces)
    if translated == source:
        raise BuildError(f"Translation catalog did not change {relative_path} for locale {locale_code}.")
    return translated


def fragment_text(relative_path: Path, locale_code: str = "en") -> str:
    locale_config(locale_code)
    return translated_fragment(read_text(GUIDE_SOURCE / relative_path), relative_path, locale_code)


def validate_fragment_plan(locale_code: str = "en", include_offline: bool = True) -> None:
    expected_online = (SHELL_OPENING, STEP_1, STEP_2, STEP_3, STEP_4, STEP_5_ONLINE, STEP_6, SHELL_ENDING)
    expected_offline = (SHELL_OPENING, STEP_0_OFFLINE, STEP_1, STEP_2, STEP_3_4_OFFLINE, STEP_6, SHELL_ENDING)
    if ONLINE_FRAGMENTS != expected_online or OFFLINE_FRAGMENTS != expected_offline:
        raise BuildError("The declared HTML fragment order does not match the guide architecture.")

    expected_steps = {
        STEP_0_OFFLINE: [0],
        STEP_1: [1],
        STEP_2: [2],
        STEP_3: [3],
        STEP_3_4_OFFLINE: [3],
        STEP_4: [4],
        STEP_5_ONLINE: [5],
        STEP_6: [6],
    }
    all_fragments = dict.fromkeys(ONLINE_FRAGMENTS + (OFFLINE_FRAGMENTS if include_offline else ()))
    for relative_path in all_fragments:
        source = fragment_text(relative_path, locale_code)
        if "OFFLINE_STEP_0_INSERT" in source or "VARIANT_STEP_5" in source:
            raise BuildError(f"Obsolete build marker found in {relative_path}.")
        panels = [int(value) for value in re.findall(r'data-step-panel="(\d+)"', source)]
        if panels != expected_steps.get(relative_path, []):
            raise BuildError(f"Fragment {relative_path} has unexpected step panels: {panels}")

    online_step_five = fragment_text(STEP_5_ONLINE, locale_code)
    if "final-candidate" not in online_step_five or "data-checksum-calculator" in online_step_five:
        raise BuildError("The online Step 5 fragment is not the wallet workflow.")
    if include_offline:
        offline_dice_step = fragment_text(STEP_3_4_OFFLINE, locale_code)
        if "data-bw-table" not in offline_dice_step or "data-die-entry" not in offline_dice_step:
            raise BuildError("The offline combined step is missing its die-entry or bit-table.")
        if "air-gap-step" not in fragment_text(STEP_0_OFFLINE, locale_code):
            raise BuildError("The offline Step 0 fragment is missing its air-gap content.")


def compose_html(fragments: tuple[Path, ...], locale_code: str = "en") -> str:
    return "".join(fragment_text(relative_path, locale_code) for relative_path in fragments)


def localized_print_name(name: str, locale_code: str) -> str:
    locale = locale_config(locale_code)
    if not locale.print_suffix or name not in LOCALIZED_PRINTOUTS:
        return name
    stem, suffix = name.rsplit(".", 1)
    return f"{stem}{locale.print_suffix}.{suffix}"


def online_html(source_html: str, locale_code: str = "en") -> str:
    output = source_html
    for name in ("BitsToWords.pdf", "BIP39_Wordlist_Binary_Decimal_Searchable.pdf", "HowToRollYourOwnSeedphrase.pdf"):
        output = output.replace(f"../{localized_print_name(name, locale_code)}", localized_print_name(name, locale_code))
    output = output.replace(
        '  <script src="script.js"></script>',
        '  <script src="locale.js"></script>\n'
        '  <script src="script.js"></script>',
    )
    return output


def language_selector_html(english_href: str, german_href: str) -> str:
        return f"""<!doctype html>
{GENERATED_FILE_NOTICE}
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ display: grid; min-height: 100vh; place-items: center; margin: 0; background: #eff7ed; font-family: "DM Sans", Arial, sans-serif; }}
        main {{ display: grid; grid-template-columns: repeat(2, minmax(132px, 180px)); gap: 1rem; padding: 1.5rem; }}
        a {{ display: grid; min-height: 180px; place-items: center; align-content: center; gap: 0.8rem; padding: 1rem; color: #203933; background: #fffdf7; border: 2px solid #15483e; border-radius: 8px; box-shadow: 0 8px 18px rgba(21, 72, 62, 0.12); font-size: 1.15rem; font-weight: 700; text-decoration: none; }}
        a:hover, a:focus-visible {{ color: #fff; background: #15483e; outline: 3px solid #c7922f; outline-offset: 3px; }}
        .flag {{ font-size: 3rem; line-height: 1; }}
        @media (max-width: 360px) {{ main {{ grid-template-columns: 1fr; width: min(100%, 220px); }} a {{ min-height: 130px; }} }}
    </style>
</head>
<body>
    <main aria-label="Language selection">
        <a href="{english_href}"><span class="flag" aria-hidden="true">🇬🇧</span><span>English</span></a>
        <a href="{german_href}" lang="de"><span class="flag" aria-hidden="true">🇩🇪</span><span>Deutsch</span></a>
    </main>
</body>
</html>
"""


def offline_html(source_html: str) -> str:
    output = source_html
    output = output.replace(
        '<meta name="description" content="A calm, visual guide to creating a BIP-39 seed phrase with physical dice.">',
        '<meta name="description" content="A self-contained offline guide to creating an English BIP-39 seed phrase with physical dice.">\n'
        '  <meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'self\'; style-src \'self\'; img-src \'self\'; connect-src \'none\'; font-src \'none\'; object-src \'none\'; media-src \'none\'; frame-src \'none\'; child-src \'none\'; worker-src \'none\'; manifest-src \'none\'; form-action \'none\'; base-uri \'none\'">',
    )
    output = output.replace("<title>Roll Your Own Seed Phrase</title>", "<title>Roll Your Own Seed Phrase — Verified Offline Edition</title>")
    output = output.replace("<body>", '<body class="offline-edition wizard-active">')
    output = re.sub(r'\s*<div class="language-picker"[^>]*>.*?</div>', "", output, count=1)
    output = re.sub(
        r'<a class="plain-guide-link"[^>]*>.*?</a>',
        '<span class="plain-guide-link">Verified offline edition</span>',
        output,
        count=1,
    )
    output = output.replace(
        '<span class="progress-label">Step <strong data-current-step>1</strong> of 6</span>',
        '<span class="progress-label">Step <strong data-current-step>0</strong> of 4</span>',
    )
    output = output.replace("<span data-progress-title>Prepare privately</span>", "<span data-progress-title>Permanent air gap required</span>")
    # Rename completion step panel 6 → 4 so offline panels are [0,1,2,3,4]
    output = output.replace(
        'data-step-panel="6" data-step-title="Your seed phrase is ready"',
        'data-step-panel="4" data-step-title="Your seed phrase is ready"',
    )
    output = output.replace('<p class="step-number">Step 6 · complete</p>', '<p class="step-number">Step 4 · complete</p>')
    output = output.replace(
        '<p class="small-note">This website is an aid to the paper guide, not a place to enter or store your rolls, bits, or seed words.</p>',
        '<p class="small-note">This verified offline edition derives BIP39 words directly from dice results entered in Step 3. All data is cleared when you navigate away or close the guide.</p>',
    )
    for name in ("BitsToWords.pdf", "BIP39_Wordlist_Binary_Decimal_Searchable.pdf", "HowToRollYourOwnSeedphrase.pdf"):
        output = output.replace(f"../{name}", name)
    output = output.replace(
        '  <script src="script.js"></script>',
        '  <script src="bip39-english.js"></script>\n'
        '  <script src="sha256.js"></script>\n'
        '  <script src="bits-words.js"></script>\n'
        '  <script src="locale.js"></script>\n'
        '  <script src="script.js"></script>',
    )
    return output


def offline_styles(source_css: str) -> str:
    without_remote_fonts = re.sub(r"\A@import\s+url\([^\n]+\);\s*", "", source_css, count=1)
    return without_remote_fonts.rstrip() + "\n\n" + read_text(OFFLINE_SOURCE / "offline.css")


def wordlist_javascript(words: list[str]) -> str:
    payload = json.dumps(words, ensure_ascii=True, separators=(",", ":"))
    return (
        "/* English BIP39 list, derived from the pinned local worksheet source. */\n"
        f"globalThis.BIP39_ENGLISH_WORDS = Object.freeze({payload});\n"
    )


def runtime_locale_javascript(locale_code: str) -> str:
    def resolve(value: object) -> object:
        if isinstance(value, str):
            return value
        if not isinstance(value, dict):
            raise BuildError("Translation catalog runtime values must be strings or objects.")
        if locale_code in value:
            localized = value[locale_code]
            if not isinstance(localized, str):
                raise BuildError(f"Translation catalog runtime value for {locale_code} must be a string.")
            return localized
        return {key: resolve(child) for key, child in value.items()}

    runtime = translation_catalog()["runtime"]
    localized = resolve(runtime)
    payload = json.dumps(localized, ensure_ascii=False, separators=(",", ":"))
    return f"/* Build-generated runtime locale: {locale_code}. */\nglobalThis.GUIDE_LOCALE_TEXT = Object.freeze({payload});\n"


def copy_common_files(target: Path, locale_code: str) -> None:
    shutil.copytree(GUIDE_SOURCE / "assets", target / "assets")
    shutil.copy2(ROOT / "LICENSE", target / "LICENSE")
    for name in ("BitsToWords.pdf", "BIP39_Wordlist_Binary_Decimal_Searchable.pdf", "HowToRollYourOwnSeedphrase.pdf"):
        localized_name = localized_print_name(name, locale_code)
        shutil.copy2(ROOT / localized_name, target / localized_name)
    if locale_code == "de":
        for name in ("HowToRollYourOwnSeedphrase-de.html", "HowToRollYourOwnSeedphrase-de.txt"):
            shutil.copy2(ROOT / name, target / name)


def source_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def write_manifest(target: Path, build_target: str, version: str, locale_code: str) -> None:
    manifest = (
        "Roll Your Own Seed Phrase\n"
        f"Build target: {build_target}\n"
        f"Guide locale: {locale_code}\n"
        f"Release version: {version}\n"
        f"Source commit: {source_commit()}\n"
        f"English BIP39 normalized SHA-256: {WORDLIST_NORMALIZED_SHA256}\n"
        f"SHA-256 implementation source SHA-256: {SHA256_SOURCE_SHA256}\n"
    )
    (target / "MANIFEST.txt").write_text(manifest, encoding="utf-8", newline="\n")


def validate_local_references(
    target: Path,
    allow_remote_css: bool = False,
    allowed_cross_edition_links: frozenset[str] = frozenset(),
) -> None:
    parser = LocalReferenceParser()
    parser.feed((target / "index.html").read_text(encoding="utf-8"))
    for reference in parser.references:
        if reference.startswith("#"):
            continue
        if reference in allowed_cross_edition_links:
            continue
        if ":" in reference or reference.startswith("//") or ".." in Path(reference).parts:
            raise BuildError(f"Non-local or escaping reference in offline HTML: {reference}")
        if not (target / reference).is_file():
            raise BuildError(f"Missing offline HTML reference: {reference}")

    css = (target / "styles.css").read_text(encoding="utf-8")
    for reference in re.findall(r"url\([\"']?([^\"')]+)", css):
        if reference.startswith("data:"):
            continue
        if allow_remote_css and reference.startswith(("http:", "https:")):
            continue
        if ":" in reference or reference.startswith("//") or ".." in Path(reference).parts:
            raise BuildError(f"Non-local or escaping reference in CSS: {reference}")
        if not (target / reference).is_file():
            raise BuildError(f"Missing offline CSS reference: {reference}")


def validate_output(target: Path, build_target: str, locale_code: str = "en") -> None:
    html_text = (target / "index.html").read_text(encoding="utf-8")
    panels = [int(value) for value in re.findall(r'data-step-panel="(\d+)"', html_text)]
    if build_target == "online":
        if panels != [1, 2, 3, 4, 5, 6] or "data-checksum-calculator" in html_text or "air-gap-step" in html_text:
            raise BuildError("The online output has the wrong steps or contains offline-only inputs.")
        completion_caption = '<p class="step-number">Step 6 · complete</p>' if locale_code == "en" else '<p class="step-number">Schritt 6 · fertig</p>'
        if completion_caption not in html_text:
            raise BuildError("The online completion caption has the wrong step number.")
        language_link = "de/" if locale_code == "en" else "../"
        validate_local_references(
            target,
            allow_remote_css=True,
            allowed_cross_edition_links=frozenset({language_link}),
        )
        return

    if panels != [0, 1, 2, 3, 4]:
        raise BuildError(f"The offline output has the wrong step order: {panels}")
    if "data-bw-table" not in html_text or "data-die-entry" not in html_text or "final-candidate" in html_text:
        raise BuildError("The offline output does not contain the combined dice-entry + bits-to-words step.")
    air_gap_warning = "your funds may be at risk" if locale_code == "en" else "deine mittel koennen gefaehrdet sein"
    if air_gap_warning not in html_text.lower():
        raise BuildError("The mandatory Step 0 funds-at-risk warning is missing.")
    completion_caption = '<p class="step-number">Step 4 · complete</p>' if locale_code == "en" else '<p class="step-number">Schritt 4 · fertig</p>'
    if completion_caption not in html_text:
        raise BuildError("The offline completion caption has the wrong step number.")

    forbidden = {
        r"https?:": "network URL",
        r"\bfetch\s*\(": "Fetch API",
        r"XMLHttpRequest": "XMLHttpRequest",
        r"WebSocket": "WebSocket",
        r"EventSource": "EventSource",
        r"serviceWorker": "service worker",
        r"localStorage": "local storage",
        r"sessionStorage": "session storage",
        r"indexedDB": "IndexedDB",
        r"\.clipboard\b": "clipboard API",
        r"crypto\s*\.": "browser cryptography API",
        r"document\.cookie": "cookies",
    }
    text_files = sorted(path for path in target.rglob("*") if path.suffix in {".html", ".css", ".js", ".txt"})
    combined = "\n".join(path.read_text(encoding="utf-8") for path in text_files)
    for pattern, label in forbidden.items():
        if re.search(pattern, combined, flags=re.IGNORECASE):
            raise BuildError(f"Forbidden {label} reference found in the offline output.")
    validate_local_references(target)


def build(target_name: str, version: str = "development", locale_code: str = "en") -> Path:
    if target_name not in {"online", "offline"}:
        raise BuildError(f"Unknown build target: {target_name}")
    if target_name == "offline" and locale_code != "en":
        raise BuildError("The offline edition is English-only.")
    locale = locale_config(locale_code)
    build_locale = locale_code if target_name == "online" else "en"

    source_css = read_text(GUIDE_SOURCE / "styles.css")
    source_script = read_text(GUIDE_SOURCE / "script.js")
    validate_fragment_plan(locale_code, include_offline=target_name == "offline")
    require_hash(OFFLINE_SOURCE / "sha256.js", SHA256_SOURCE_SHA256)
    words = extract_wordlist()

    target = DIST / (locale.output_directory if target_name == "online" else "offline")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    copy_common_files(target, locale_code if target_name == "online" else "en")

    if target_name == "online":
        deployable_html = online_html(compose_html(ONLINE_FRAGMENTS, locale_code), locale_code)
        (target / "index.html").write_text(deployable_html, encoding="utf-8", newline="\n")
        (ROOT / "index.html").write_text(
            language_selector_html("dist/online/index.html", "dist/de/index.html"), encoding="utf-8", newline="\n"
        )
        (DIST / "site-index.html").write_text(
            language_selector_html("en/index.html", "de/index.html"), encoding="utf-8", newline="\n"
        )
        (target / "styles.css").write_text(source_css, encoding="utf-8", newline="\n")
    else:
        (target / "index.html").write_text(offline_html(compose_html(OFFLINE_FRAGMENTS)), encoding="utf-8", newline="\n")
        (target / "styles.css").write_text(offline_styles(source_css), encoding="utf-8", newline="\n")
        (target / "bip39-english.js").write_text(wordlist_javascript(words), encoding="utf-8", newline="\n")
        shutil.copy2(OFFLINE_SOURCE / "sha256.js", target / "sha256.js")
        shutil.copy2(OFFLINE_SOURCE / "bits-words.js", target / "bits-words.js")
        shutil.copytree(OFFLINE_SOURCE / "LICENSES", target / "LICENSES")

    (target / "locale.js").write_text(runtime_locale_javascript(build_locale), encoding="utf-8", newline="\n")
    (target / "script.js").write_text(source_script, encoding="utf-8", newline="\n")
    write_manifest(target, target_name, version, build_locale)
    validate_output(target, target_name, build_locale)
    return target


def deterministic_zip(source: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as output:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = Path("RollYourOwnSeedphrase-offline") / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, path.read_bytes())


def package(version: str) -> Path:
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?", version):
        raise BuildError("Version must look like 1.0.0 or 1.0.0-rc1.")
    offline = build("offline", version)
    release = DIST / "release"
    release.mkdir(parents=True, exist_ok=True)
    archive = release / f"RollYourOwnSeedphrase-offline-{version}.zip"
    deterministic_zip(offline, archive)
    checksum = f"{digest(archive.read_bytes())}  {archive.name}\n"
    (release / "SHA256SUMS").write_text(checksum, encoding="ascii", newline="\n")
    return archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=("online", "offline", "all", "package"))
    parser.add_argument("--version", help="Required for the package target, for example 1.0.0")
    parser.add_argument("--locale", choices=tuple(LOCALES), default="en", help="Guide locale for the online target")
    args = parser.parse_args()
    try:
        if args.target == "all":
            build("online", locale_code="en")
            build("online", locale_code="de")
            build("offline", locale_code="en")
        elif args.target == "package":
            if not args.version:
                raise BuildError("--version is required for the package target.")
            package(args.version)
        else:
            build(args.target, locale_code=args.locale)
    except (BuildError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        print(f"build failed: {error}", file=sys.stderr)
        return 1
    print(f"build succeeded: {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
