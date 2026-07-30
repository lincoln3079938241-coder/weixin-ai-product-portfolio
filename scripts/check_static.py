from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []
        self.ids: set[str] = set()
        self.lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang", "")
        if values.get("id"):
            self.ids.add(values["id"])
        reference = values.get("href") or values.get("src")
        if reference:
            self.references.append(reference)


def check_html(relative_path: str, expected_lang: str) -> None:
    path = ROOT / relative_path
    parser = ReferenceParser()
    source = path.read_text(encoding="utf-8")
    parser.feed(source)
    missing = [
        reference
        for reference in parser.references
        if not urlparse(reference).scheme
        and not reference.startswith("#")
        and not (path.parent / reference).exists()
    ]
    missing_fragments = [
        reference
        for reference in parser.references
        if reference.startswith("#") and reference[1:] not in parser.ids
    ]
    print(
        f"{relative_path}: lang={parser.lang}, references={len(parser.references)}, "
        f"missing={missing}, missing_fragments={missing_fragments}"
    )
    if not path.exists() or parser.lang != expected_lang or missing or missing_fragments:
        raise AssertionError(f"HTML validation failed: {relative_path}")

    if expected_lang == "en":
        untranslated = re.findall(r"[\u3400-\u9fff]+", source.replace("中文", ""))
        print(f"{relative_path}: untranslated_cjk={untranslated}")
        if untranslated:
            raise AssertionError(f"Untranslated Chinese remains in {relative_path}: {untranslated}")


def check_pdf(relative_path: str, expected_pages: int, required_links: tuple[str, ...] = ()) -> None:
    reader = PdfReader(ROOT / relative_path)
    links = []
    for page in reader.pages:
        for annotation in page.get("/Annots", []):
            action = annotation.get_object().get("/A")
            if action and action.get("/URI"):
                links.append(str(action.get("/URI")))
    missing_links = [link for link in required_links if link not in links]
    print(
        f"{relative_path}: pages={len(reader.pages)}, clickable_links={len(links)}, "
        f"missing_required_links={missing_links}"
    )
    if len(reader.pages) != expected_pages or not links or missing_links:
        raise AssertionError(f"PDF validation failed: {relative_path}")


def check_assets() -> None:
    required = [
        "styles.css",
        "assets/Chen-Weixin-AI-Product-Portfolio.pdf",
        "assets/DriveMate-Concept-Proposal.pdf",
        "assets/Chen-Weixin-AI-Product-Portfolio-EN.pdf",
        "assets/DriveMate-Concept-EN.pdf",
        "assets/screenshots/auto-01-home.jpg",
        "assets/screenshots/auto-02-result.jpg",
        "assets/screenshots/auto-03-confirm.jpg",
        "assets/screenshots/auto-04-update.jpg",
        "assets/screenshots/radar-01-home.jpg",
        "assets/screenshots/radar-02-filter.jpg",
        "assets/screenshots/radar-03-sources.jpg",
        "assets/screenshots/radar-04-quality.jpg",
    ]
    missing = [relative for relative in required if not (ROOT / relative).is_file()]
    print(f"required_assets={len(required)}, missing={missing}")
    if missing:
        raise AssertionError(f"Missing required assets: {missing}")


if __name__ == "__main__":
    check_assets()
    check_html("index.html", "zh-CN")
    check_html("drivemate.html", "zh-CN")
    check_html("en/index.html", "en")
    check_html("en/drivemate.html", "en")
    check_pdf("assets/Chen-Weixin-AI-Product-Portfolio.pdf", 7)
    check_pdf("assets/DriveMate-Concept-Proposal.pdf", 2)
    check_pdf(
        "assets/Chen-Weixin-AI-Product-Portfolio-EN.pdf",
        7,
        required_links=(
            "https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/en/",
            "https://github.com/lincoln3079938241-coder",
            "https://auto-lifeos-demo.streamlit.app/",
            "https://shanghai-2027-job-radar-demo.streamlit.app/",
            "mailto:Lincoln3079938241@163.com",
        ),
    )
    check_pdf(
        "assets/DriveMate-Concept-EN.pdf",
        2,
        required_links=(
            "https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/en/",
            "https://lincoln3079938241-coder.github.io/weixin-ai-product-portfolio/en/drivemate.html",
        ),
    )
    print("Static validation passed.")
