from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD_PATH = ROOT / "build-guides.py"
SPEC = importlib.util.spec_from_file_location("offline_build", BUILD_PATH)
assert SPEC and SPEC.loader
build_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_module
SPEC.loader.exec_module(build_module)
PRINT_BUILD_PATH = ROOT / "build-localized-printouts.py"
PRINT_SPEC = importlib.util.spec_from_file_location("print_build", PRINT_BUILD_PATH)
assert PRINT_SPEC and PRINT_SPEC.loader
print_module = importlib.util.module_from_spec(PRINT_SPEC)
sys.modules[PRINT_SPEC.name] = print_module
PRINT_SPEC.loader.exec_module(print_module)


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.online = build_module.build("online")
        cls.german_online = build_module.build("online", locale_code="de")
        cls.offline = build_module.build("offline")

    def test_explicit_fragment_plans_are_canonical(self) -> None:
        self.assertEqual(
            build_module.ONLINE_FRAGMENTS,
            (
                build_module.SHELL_OPENING, build_module.STEP_1, build_module.STEP_2,
                build_module.STEP_3, build_module.STEP_4, build_module.STEP_5_ONLINE,
                build_module.STEP_6, build_module.SHELL_ENDING,
            ),
        )
        self.assertEqual(
            build_module.OFFLINE_FRAGMENTS,
            (
                build_module.SHELL_OPENING, build_module.STEP_0_OFFLINE, build_module.STEP_1,
                build_module.STEP_2,
                build_module.STEP_3_4_OFFLINE, build_module.STEP_6, build_module.SHELL_ENDING,
            ),
        )
        self.assertEqual(
            (self.online / "index.html").read_text(encoding="utf-8"),
            build_module.online_html(build_module.compose_html(build_module.ONLINE_FRAGMENTS)),
        )
        self.assertEqual((self.online / "styles.css").read_bytes(), (ROOT / "guide-src" / "styles.css").read_bytes())
        self.assertEqual((self.online / "script.js").read_bytes(), (ROOT / "guide-src" / "script.js").read_bytes())
        self.assertEqual(
            (self.online / "locale.js").read_text(encoding="utf-8"),
            build_module.runtime_locale_javascript("en"),
        )
        german = (self.german_online / "index.html").read_text(encoding="utf-8")
        self.assertEqual(
            german,
            build_module.online_html(build_module.compose_html(build_module.ONLINE_FRAGMENTS, "de"), "de"),
        )
        self.assertEqual(
            (self.german_online / "locale.js").read_text(encoding="utf-8"),
            build_module.runtime_locale_javascript("de"),
        )
        self.assertIn('<html lang="de">', german)
        self.assertIn('BitsToWords-de.pdf', german)
        self.assertIn('BIP39_Wordlist_Binary_Decimal_Searchable.pdf', german)
        self.assertNotIn('BIP39_Wordlist_Binary_Decimal_Searchable-de.pdf', german)
        self.assertIn('HowToRollYourOwnSeedphrase-de.pdf', german)
        self.assertTrue((self.german_online / "HowToRollYourOwnSeedphrase-de.html").is_file())
        self.assertFalse((ROOT / "BIP39_Wordlist_Binary_Decimal_Searchable-de.pdf").exists())
        self.assertFalse((ROOT / "additional_ressources" / "BIP39_Wordlist_Binary_Decimal_Searchable-de.ods").exists())

    def test_german_uses_shared_templates_and_complete_catalog(self) -> None:
        catalog = build_module.translation_catalog()
        self.assertEqual(catalog["format"], 2)
        self.assertEqual(
            set(catalog["fragments"]),
            {fragment.as_posix() for fragment in build_module.ONLINE_FRAGMENTS},
        )
        for fragment in build_module.ONLINE_FRAGMENTS:
            source = (ROOT / "guide-src" / fragment).read_text(encoding="utf-8")
            message_keys = set(build_module.fragment_messages(fragment))
            placeholder_keys = set(re.findall(r"\{\{([a-z][a-z0-9-]*)\}\}", source))
            self.assertEqual(placeholder_keys, message_keys)
            build_module.validate_fragment_template(source, fragment, build_module.fragment_messages(fragment))
            self.assertNotIn("{{", build_module.fragment_text(fragment))
            self.assertNotIn("{{", build_module.fragment_text(fragment, "de"))
        self.assertFalse((ROOT / "guide-src" / "de").exists())
        self.assertNotIn("Dauerhafte Netzwerk-Trennung erforderlich", (ROOT / "guide-src" / "script.js").read_text(encoding="utf-8"))
        self.assertIn("Dauerhafte Netzwerk-Trennung erforderlich", (self.german_online / "locale.js").read_text(encoding="utf-8"))

    def test_quick_guides_use_shared_template_and_paired_catalog(self) -> None:
        catalog = print_module.quick_guide_catalog()
        print_module.validate_quick_guide_catalog(catalog)
        self.assertEqual(catalog["format"], 1)
        self.assertEqual(
            [entry["slot"] for entry in catalog["html"]["body"]],
            list(print_module.QUICK_GUIDE_SLOTS),
        )
        self.assertFalse((ROOT / "print-src" / "HowToRollYourOwnSeedphrase-de.html").exists())
        for locale_code in ("en", "de"):
            html_output = ROOT / print_module.quick_guide_name(locale_code, "html")
            self.assertEqual(html_output.read_text(encoding="utf-8"), print_module.render_quick_guide_html(locale_code))
        english_print = (ROOT / "HowToRollYourOwnSeedphrase.html").read_text(encoding="utf-8")
        german_print = (ROOT / "HowToRollYourOwnSeedphrase-de.html").read_text(encoding="utf-8")
        self.assertIn("You can use this printed guide for a real seed phrase.", english_print)
        self.assertIn("If you use regular dice and binary quantization, we recommend you use 24 words.", english_print)
        self.assertIn("Du kannst diese gedruckte Anleitung für eine echte Seed-Phrase verwenden.", german_print)
        self.assertIn("Falls du normale Würfel und binäre Quantisierung verwenden willst, empfehlen wir 24 Wörter zu nutzen.", german_print)

    def test_generated_selectors_match_their_layouts(self) -> None:
        online = (self.online / "index.html").read_text(encoding="utf-8")
        root_index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(self.online, ROOT / "dist" / "en")
        self.assertEqual(root_index, build_module.local_selector_forwarder_html("dist/index.html"))
        self.assertEqual(root_index.count(build_module.GENERATED_FILE_NOTICE), 1)
        self.assertNotIn(build_module.GENERATED_FILE_NOTICE, online)
        self.assertFalse((ROOT / "dist" / "online").exists())
        self.assertEqual(
            (ROOT / "dist" / "index.html").read_text(encoding="utf-8"),
            build_module.language_selector_html("en/index.html", "de/index.html"),
        )
        self.assertFalse((ROOT / "dist" / "site-index.html").exists())
        self.assertIn('href="dist/index.html"', root_index)
        self.assertIn('🇬🇧', (ROOT / "dist" / "index.html").read_text(encoding="utf-8"))
        self.assertIn('🇩🇪', (ROOT / "dist" / "index.html").read_text(encoding="utf-8"))
        for fragment in build_module.ONLINE_FRAGMENTS + build_module.OFFLINE_FRAGMENTS:
            self.assertNotIn(build_module.GENERATED_FILE_NOTICE, build_module.fragment_text(fragment))

    def test_step_variants_are_exact(self) -> None:
        online = (self.online / "index.html").read_text(encoding="utf-8")
        offline = (self.offline / "index.html").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'data-step-panel="(\d+)"', online), ["1", "2", "3", "4", "5", "6"])
        self.assertEqual(re.findall(r'data-step-panel="(\d+)"', offline), ["0", "1", "2", "3", "4"])
        self.assertNotIn("data-checksum-calculator", online)
        self.assertNotIn("air-gap-step", online)
        self.assertIn("final-candidate", online)
        self.assertIn("data-bw-table", offline)
        self.assertIn("data-die-entry", offline)
        self.assertNotIn("data-checksum-calculator", offline)
        self.assertIn("your funds may be at risk", offline.lower())
        self.assertNotIn("final-candidate", offline)
        self.assertIn('<p class="step-number">Step 6 · complete</p>', online)
        self.assertIn('<p class="step-number">Step 4 · complete</p>', offline)
        self.assertNotIn("VARIANT_STEP_5", online + offline)
        self.assertNotIn("OFFLINE_STEP_0_INSERT", online + offline)

    def test_dice_policy_and_guide_use_are_consistent(self) -> None:
        online = (self.online / "index.html").read_text(encoding="utf-8")
        german = (self.german_online / "index.html").read_text(encoding="utf-8")
        offline = (self.offline / "index.html").read_text(encoding="utf-8")
        source_script = (ROOT / "guide-src" / "script.js").read_text(encoding="utf-8")
        self.assertIn("let selectedDice = 'consumer';", source_script)
        self.assertIn('data-dice="consumer" aria-pressed="true">Regular dice', online)
        self.assertIn("For 12 words, use casino-grade dice. With regular dice, choose 24 words or use base-4.", online)
        self.assertIn("With regular dice, select 24 words or use base-4.", online)
        self.assertIn("Do not use this online guide for a real seed phrase.", online)
        self.assertNotIn("turn off or cover its camera", online)
        self.assertIn('data-dice="consumer" aria-pressed="true">Normale Würfel', german)
        self.assertIn("Mit normalen Würfeln wähle 24 Wörter oder Basis 4.", german)
        self.assertIn("Ich habe im Feld Bezeichnung einen nicht geheimen Namen eingetragen.", german)
        self.assertNotIn("I filled the worksheet Identifier", german)
        self.assertIn("Nutze diese Online-Anleitung nicht für eine echte Seed-Phrase.", german)
        self.assertNotIn("Keep it private, offline, and safely backed up.", online)
        self.assertNotIn("Keep your seed phrase private, offline, and backed up safely.", online)
        self.assertNotIn("Verwahre sie privat, offline und sicher.", german)
        self.assertNotIn("Halte deine Seed-Phrase privat, offline und sicher gesichert.", german)
        self.assertIn("This offline edition is for experts.", offline)
        self.assertIn("Keep it private, offline, and safely backed up.", offline)
        self.assertIn("Keep your seed phrase private, offline, and backed up safely.", offline)
        self.assertNotIn("Use this online guide to learn the method", offline)

    def test_variant_sources_cannot_cross_contaminate(self) -> None:
        online_sources = set(build_module.ONLINE_FRAGMENTS)
        offline_sources = set(build_module.OFFLINE_FRAGMENTS)
        self.assertNotIn(build_module.STEP_0_OFFLINE, online_sources)
        self.assertNotIn(build_module.STEP_3_4_OFFLINE, online_sources)
        self.assertNotIn(build_module.STEP_5_ONLINE, offline_sources)
        self.assertNotIn(build_module.STEP_3, offline_sources)
        self.assertNotIn(build_module.STEP_4, offline_sources)
        self.assertEqual(
            online_sources & offline_sources,
            {
                build_module.SHELL_OPENING, build_module.STEP_1, build_module.STEP_2,
                build_module.STEP_6, build_module.SHELL_ENDING,
            },
        )

    def test_offline_artifact_is_self_contained(self) -> None:
        html = (self.offline / "index.html").read_text(encoding="utf-8")
        css = (self.offline / "styles.css").read_text(encoding="utf-8")
        self.assertNotRegex(html + css, r"https?:")
        self.assertNotIn("@import", css)
        for name in (
            "index.html", "styles.css", "locale.js", "script.js", "sha256.js",
            "bits-words.js", "bip39-english.js", "BitsToWords.pdf",
            "BIP39_Wordlist_Binary_Decimal_Searchable.pdf",
            "HowToRollYourOwnSeedphrase.pdf", "LICENSE", "LICENSES/BIP39.txt", "MANIFEST.txt"
        ):
            self.assertTrue((self.offline / name).is_file(), name)
        self.assertFalse((self.offline / "calculator.js").exists())
        self.assertNotIn('language-picker', html)
        self.assertNotIn('Deutsch', html)
        self.assertNotIn('offline-de', html)

    def test_offline_rejects_non_english_locale(self) -> None:
        with self.assertRaisesRegex(build_module.BuildError, "English-only"):
            build_module.build("offline", locale_code="de")

    def test_forbidden_browser_capabilities_are_absent(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.offline.rglob("*")
            if path.suffix in {".html", ".css", ".js", ".txt"}
        )
        for pattern in (
            r"\bfetch\s*\(", r"XMLHttpRequest", r"WebSocket", r"EventSource",
            r"serviceWorker", r"localStorage", r"sessionStorage", r"indexedDB",
            r"\.clipboard\b", r"crypto\s*\.", r"document\.cookie"
        ):
            self.assertIsNone(re.search(pattern, combined, flags=re.IGNORECASE), pattern)

        bits_words = (self.offline / "bits-words.js").read_text(encoding="utf-8")
        shared_script = (self.offline / "script.js").read_text(encoding="utf-8")
        self.assertIn("guide:stepchange", bits_words)
        self.assertIn("guide:stepchange", shared_script)
        self.assertIn("addEventListener('pagehide'", bits_words)
        self.assertIn("addEventListener('pageshow'", bits_words)
        self.assertNotIn("isGerman", bits_words)

    def test_offline_dice_bits_step(self) -> None:
        html = (self.offline / "index.html").read_text(encoding="utf-8")
        bw = (self.offline / "bits-words.js").read_text(encoding="utf-8")
        css = (self.offline / "styles.css").read_text(encoding="utf-8")
        self.assertIn("data-bw-table", html)
        self.assertIn("data-die-entry", html)
        self.assertIn('class="die-btn"', html)
        self.assertIn('data-face="6"', html)
        self.assertNotIn("<datalist", html)
        self.assertNotIn("<textarea", html)
        self.assertNotIn("data-checksum-calculator", html)
        self.assertIn("function enterFace", bw)
        self.assertIn("function undoLastRoll", bw)
        self.assertIn("function updateLastRow", bw)
        self.assertIn("function deriveFinalWord", bw)
        self.assertIn("OfflineBitsWordsCore", bw)
        self.assertIn("OfflineHash.sha256", bw)
        self.assertIn("guide:stepchange", bw)
        self.assertIn("addEventListener('pagehide'", bw)
        self.assertIn(".die-btn", css)
        self.assertIn(".bw-row", css)

    def test_deterministic_package(self) -> None:
        first = build_module.package("0.0.0-test")
        first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
        second = build_module.package("0.0.0-test")
        self.assertEqual(first_hash, hashlib.sha256(second.read_bytes()).hexdigest())
        with zipfile.ZipFile(second) as archive:
            names = archive.namelist()
            self.assertEqual(names, sorted(names))
            self.assertTrue(all(name.startswith("RollYourOwnSeedphrase-offline/") for name in names))
            self.assertTrue(all(info.date_time == build_module.FIXED_ZIP_TIME for info in archive.infolist()))
            self.assertTrue(all((info.external_attr >> 16) & 0o777 == 0o644 for info in archive.infolist()))


if __name__ == "__main__":
    unittest.main()
