import re
from .resume_model import ResumeData

# ---------------- GLOBAL DATA ----------------

ACTION_VERBS = {
    "developed", "built", "designed", "implemented", "led",
    "managed", "created", "optimized", "analyzed", "engineered"
}

SOFT_SKILLS = {
    "communication", "leadership", "teamwork",
    "problem solving", "adaptability", "collaboration"
}

EXPECTED_ORDER = [
    "summary",
    "skills",
    "experience",
    "projects",
    "education"
]

TECH_OBJECTS = {
    "model", "system", "pipeline", "api", "application",
    "database", "dashboard", "algorithm", "service"
}

IMPACT_KEYWORDS = {
    "increased", "reduced", "improved", "optimized",
    "achieved", "delivered", "boosted", "accuracy",
    "performance", "%", "percent"
}

DATE_REGEX = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4})"


# ---------------- TAILORING RULES ----------------

def rule_soft_skills(resume: ResumeData):
    text = resume.raw_text.lower()
    found = [s for s in SOFT_SKILLS if s in text]

    if len(found) < 3:
        return {
            "id": "soft_skills",
            "category": "Tailoring",
            "priority": "High",
            "penalty": 5,
            "message": "Limited soft skills detected",
            "reason": "ATS favors resumes that balance technical and interpersonal skills",
            "fix": "Integrate soft skills like leadership or communication into experience bullets"
        }
    return None


def rule_action_verbs(resume: ResumeData):
    if not resume.bullets:
        return None

    weak = 0
    for b in resume.bullets:
        first = b.strip("•- ").split(" ")[0].lower()
        if first not in ACTION_VERBS:
            weak += 1

    if weak / len(resume.bullets) > 0.6:
        return {
            "id": "action_verbs",
            "category": "Tailoring",
            "priority": "High",
            "penalty": 5,
            "message": "Bullet points lack strong action verbs",
            "reason": "ATS prefers accomplishment-driven bullet points",
            "fix": "Start bullets with action verbs like Developed, Built, Led, or Analyzed"
        }
    return None


def rule_tailored_title(resume: ResumeData):
    header = resume.header_text.lower()
    keywords = ["engineer", "analyst", "developer", "scientist"]

    if not any(k in header for k in keywords):
        return {
            "id": "tailored_title",
            "category": "Tailoring",
            "priority": "High",
            "penalty": 5,
            "message": "No clear professional title detected",
            "reason": "ATS uses job titles to classify candidate profiles",
            "fix": "Add a clear professional title below your name (e.g., Data Analyst)"
        }
    return None


# ---------------- ADVANCED INTELLIGENCE ----------------

def rule_section_order(resume: ResumeData):
    actual = [s for s in resume.sections.keys() if s in EXPECTED_ORDER]

    if len(actual) < 3:
        return None

    disorder = sum(
        abs(EXPECTED_ORDER.index(s) - actual.index(s))
        for s in actual
    )

    if disorder >= 6:
        return {
            "id": "section_order",
            "category": "Sections",
            "priority": "Medium",
            "penalty": 6,
            "message": "Suboptimal section order detected",
            "reason": "ATS scores resumes higher when sections follow a predictable flow",
            "fix": "Reorder sections as: Summary → Skills → Experience → Projects → Education"
        }
    return None


def rule_experience_density(resume: ResumeData):
    text = " ".join(
        resume.sections.get("experience", []) +
        resume.sections.get("projects", [])
    )

    if not text:
        return None

    ratio = len(text.split()) / max(resume.word_count, 1)

    if ratio < 0.25:
        return {
            "id": "experience_density",
            "category": "Content",
            "priority": "High",
            "penalty": 7,
            "message": "Low experience signal density detected",
            "reason": "ATS favors resumes where experience forms a strong portion of content",
            "fix": "Expand experience and project sections with concrete responsibilities and outcomes"
        }
    return None


def rule_bullet_quality(resume: ResumeData):
    if not resume.bullets:
        return None

    weak = 0
    for bullet in resume.bullets:
        words = bullet.lower().split()
        has_verb = words and words[0] in ACTION_VERBS
        has_object = any(o in bullet.lower() for o in TECH_OBJECTS)
        has_impact = any(k in bullet.lower() for k in IMPACT_KEYWORDS)

        if sum([has_verb, has_object, has_impact]) < 2:
            weak += 1

    if weak / len(resume.bullets) > 0.4:
        return {
            "id": "bullet_quality",
            "category": "Content",
            "priority": "High",
            "penalty": 8,
            "message": "Bullet points lack clear impact or technical focus",
            "reason": "ATS and recruiters favor bullets showing action, scope, and results",
            "fix": "Rewrite bullets using Verb + Technical Object + Measurable Impact"
        }
    return None


def rule_timeline_consistency(resume: ResumeData):
    exp = resume.sections.get("experience", [])
    if not exp:
        return None

    date_lines = [l for l in exp if re.search(DATE_REGEX, l.lower())]

    if len(date_lines) < 2:
        return {
            "id": "timeline_consistency",
            "category": "Content",
            "priority": "High",
            "penalty": 7,
            "message": "Experience entries missing clear dates",
            "reason": "ATS relies on timelines to assess career progression",
            "fix": "Add start and end dates for each role (Month Year – Month Year)"
        }
    return None


def rule_ats_failure_modes(resume: ResumeData):
    risks = []

    if len(resume.header_text.split()) > 10:
        risks.append("Header Misclassification")

    if len(resume.sections) > 12:
        risks.append("Section Fragmentation")

    if len(" ".join(resume.sections.get("experience", [])).split()) < 150:
        risks.append("Experience Under-Indexing")

    if risks:
        return {
            "id": "ats_failure_modes",
            "category": "ATS Essentials",
            "priority": "High",
            "penalty": 10,
            "message": "Potential ATS failure modes detected",
            "reason": "Certain resume patterns can cause ATS parsing or ranking failures",
            "fix": f"Mitigate risks: {', '.join(risks)}"
        }
    return None


# ---------------- STRUCTURE & ESSENTIALS ----------------

def rule_missing_sections(resume: ResumeData):
    required = {"education", "skills", "experience"}
    missing = required - set(resume.sections.keys())

    if missing:
        return {
            "id": "missing_sections",
            "category": "Sections",
            "priority": "High",
            "penalty": 15,
            "message": f"Missing essential sections: {', '.join(missing)}",
            "reason": "ATS expects a standard resume structure",
            "fix": "Add clearly labeled Education, Skills, and Experience sections"
        }
    return None


def rule_fragmented_structure(resume: ResumeData):
    standard = {
        "education", "skills", "experience",
        "projects", "certifications", "summary", "languages"
    }

    extra = [s for s in resume.sections if s not in standard]

    if len(extra) >= 5:
        return {
            "id": "fragmented_structure",
            "category": "Sections",
            "priority": "High",
            "penalty": 8,
            "message": "Too many non-standard section headings detected",
            "reason": "ATS may fragment resume into unrelated sections",
            "fix": "Use standard section headings and avoid styling labels as headers"
        }
    return None


def rule_header_noise(resume: ResumeData):
    if len(resume.header_text.split()) > 10:
        return {
            "id": "header_noise",
            "category": "ATS Essentials",
            "priority": "Medium",
            "penalty": 6,
            "message": "Non-contact content detected in header area",
            "reason": "ATS may misclassify content placed in headers",
            "fix": "Avoid placing experience or project lines near page top"
        }
    return None


def rule_contact_info(resume: ResumeData):
    text = resume.raw_text.lower()
    has_email = "@" in text
    has_phone = re.search(r"\d{10}", text)

    if not (has_email and has_phone):
        return {
            "id": "contact_info",
            "category": "ATS Essentials",
            "priority": "Medium",
            "penalty": 4,
            "message": "Incomplete contact information",
            "reason": "Recruiters may not be able to contact you",
            "fix": "Ensure email and phone number are clearly visible at the top"
        }
    return None
