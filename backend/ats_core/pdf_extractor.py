import pdfplumber
import re
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)

from .resume_model import ResumeData
from .section_detector import detect_sections

BULLET_CHARS = ["•", "-", "–", "—", "●", "▪"]


def extract_pdf(path: str) -> ResumeData:
    full_text = []
    lines = []
    header_text = []
    footer_text = []
    bullets_found = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            page_lines = text.split("\n")

            # Page dimensions
            height = page.height

            # Extract words with layout info
            words = page.extract_words(use_text_flow=True)

            # Detect header and footer text
            for w in words:
                if w["top"] < height * 0.1:
                    header_text.append(w["text"])
                elif w["top"] > height * 0.9:
                    footer_text.append(w["text"])

            # Process lines
            for line in page_lines:
                clean = line.strip()
                if not clean:
                    continue

                lines.append(clean)
                full_text.append(clean)

                if any(clean.startswith(b) for b in BULLET_CHARS):
                    bullets_found.append(clean)

    # Build raw text
    raw_text = "\n".join(full_text)

    # Word count (ATS-critical)
    word_count = len(re.findall(r"\b\w+\b", raw_text))

    # Phase 2: Section detection
    sections = detect_sections(lines)

    return ResumeData(
        raw_text=raw_text,
        lines=lines,
        word_count=word_count,
        header_text=" ".join(header_text),
        footer_text=" ".join(footer_text),
        bullets=bullets_found,
        sections=sections
    )
