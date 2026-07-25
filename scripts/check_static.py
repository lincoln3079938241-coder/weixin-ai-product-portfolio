from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        reference = values.get("href") or values.get("src")
        if reference:
            self.references.append(reference)


def check_html(relative_path: str) -> None:
    path = ROOT / relative_path
    parser = ReferenceParser()
    parser.feed(path.read_text(encoding="utf-8"))
    missing = [
        reference
        for reference in parser.references
        if not urlparse(reference).scheme
        and not reference.startswith("#")
        and not (path.parent / reference).exists()
    ]
    print(f"{relative_path}: references={len(parser.references)}, missing={missing}")
    if missing:
        raise SystemExit(1)


def check_pdf(relative_path: str, expected_pages: int) -> None:
    reader = PdfReader(ROOT / relative_path)
    links = []
    for page in reader.pages:
        for annotation in page.get("/Annots", []):
            action = annotation.get_object().get("/A")
            if action and action.get("/URI"):
                links.append(str(action.get("/URI")))
    print(f"{relative_path}: pages={len(reader.pages)}, clickable_links={len(links)}")
    if len(reader.pages) != expected_pages or not links:
        raise SystemExit(1)


if __name__ == "__main__":
    check_html("index.html")
    check_html("drivemate.html")
    check_pdf("assets/Chen-Weixin-AI-Product-Portfolio.pdf", 7)
    check_pdf("assets/DriveMate-Concept-Proposal.pdf", 2)
