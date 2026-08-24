#!/usr/bin/env python3
"""Verify that committed printable artifacts match the current source generators."""

from __future__ import annotations

import filecmp
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXACT_ARTIFACTS = (
    Path("HowToRollYourOwnSeedphrase.html"),
    Path("HowToRollYourOwnSeedphrase-de.html"),
)
PDF_ARTIFACTS = (
    Path("BitsToWords.pdf"),
    Path("BitsToWords-de.pdf"),
    Path("HowToRollYourOwnSeedphrase.pdf"),
    Path("HowToRollYourOwnSeedphrase-de.pdf"),
)
RASTER_DPI = "144"


class VerificationError(RuntimeError):
    """A committed printable artifact is stale or a required verifier is missing."""


def run(*arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(arguments, cwd=cwd, check=True, capture_output=True)


def require_tools() -> None:
    missing = [tool for tool in ("pdfinfo", "pdftotext", "pdftoppm") if shutil.which(tool) is None]
    if missing:
        raise VerificationError(f"Missing PDF verification tools: {', '.join(missing)}")


def copy_artifacts(destination: Path) -> None:
    for relative_path in EXACT_ARTIFACTS + PDF_ARTIFACTS:
        source = ROOT / relative_path
        if not source.is_file():
            raise VerificationError(f"Committed printable artifact is missing: {relative_path}")
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def pdf_page_geometry(path: Path) -> tuple[bytes, bytes]:
    info = run("pdfinfo", str(path)).stdout.decode("utf-8")
    pages = next((line for line in info.splitlines() if line.startswith("Pages:")), None)
    page_size = next((line for line in info.splitlines() if line.startswith("Page size:")), None)
    if pages is None or page_size is None:
        raise VerificationError(f"Could not read page geometry from {path.name}")
    return pages.encode("utf-8"), page_size.encode("utf-8")


def raster_hashes(path: Path, destination: Path) -> tuple[tuple[str, str], ...]:
    destination.mkdir(parents=True, exist_ok=True)
    prefix = destination / path.stem
    run("pdftoppm", "-r", RASTER_DPI, "-png", str(path), str(prefix))
    images = sorted(destination.glob(f"{path.stem}-*.png"))
    if not images:
        raise VerificationError(f"Could not rasterize {path.name}")
    return tuple((image.name, hashlib.sha256(image.read_bytes()).hexdigest()) for image in images)


def compare_pdf(committed: Path, generated: Path, workspace: Path) -> list[str]:
    differences: list[str] = []
    if pdf_page_geometry(committed) != pdf_page_geometry(generated):
        differences.append("page count or page size")
    if run("pdftotext", str(committed), "-").stdout != run("pdftotext", str(generated), "-").stdout:
        differences.append("extracted text")
    if raster_hashes(committed, workspace / "committed") != raster_hashes(generated, workspace / "generated"):
        differences.append(f"rendered pages at {RASTER_DPI} DPI")
    return differences


def main() -> int:
    try:
        require_tools()
        with tempfile.TemporaryDirectory(prefix="print-artifact-verify-") as temporary_directory:
            temporary = Path(temporary_directory)
            committed = temporary / "committed"
            committed.mkdir()
            copy_artifacts(committed)
            run(sys.executable, "build-localized-printouts.py", "all", cwd=ROOT)

            stale: list[str] = []
            for relative_path in EXACT_ARTIFACTS:
                if not filecmp.cmp(committed / relative_path, ROOT / relative_path, shallow=False):
                    stale.append(f"{relative_path}: generated text or HTML differs")
            for relative_path in PDF_ARTIFACTS:
                differences = compare_pdf(committed / relative_path, ROOT / relative_path, temporary / relative_path.stem)
                if differences:
                    stale.append(f"{relative_path}: {', '.join(differences)} differs")
            if stale:
                raise VerificationError("Committed printable artifacts are stale:\n" + "\n".join(f"- {item}" for item in stale))
    except (OSError, subprocess.CalledProcessError, VerificationError) as error:
        print(f"print artifact verification failed: {error}", file=sys.stderr)
        return 1
    print("committed printable artifacts match the current generators")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())