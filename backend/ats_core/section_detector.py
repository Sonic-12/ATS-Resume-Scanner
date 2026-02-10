import re

COMMON_SECTIONS = [
    "education",
    "experience",
    "projects",
    "skills",
    "certifications",
    "summary",
    "objective",
    "internships",
    "achievements"
]


def is_heading(line: str) -> bool:
    if len(line) > 40:
        return False

    if line.endswith(":"):
        line = line[:-1]

    # ALL CAPS
    if line.isupper():
        return True

    # Title Case
    if line.istitle():
        return True

    return False


def normalize_section_name(line: str) -> str:
    clean = re.sub(r"[^a-zA-Z ]", "", line).lower().strip()

    for sec in COMMON_SECTIONS:
        if sec in clean:
            return sec

    return clean if clean else "unknown"


def detect_sections(lines: list[str]) -> dict:
    sections = {}
    current_section = "unknown"
    sections[current_section] = []

    for line in lines:
        if is_heading(line):
            sec_name = normalize_section_name(line)
            current_section = sec_name
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections[current_section].append(line)

    return sections

