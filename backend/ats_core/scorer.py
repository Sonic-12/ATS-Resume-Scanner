from collections import defaultdict
from .rules import *

# ---------------- CATEGORY CONFIG ----------------

CATEGORY_CAPS = {
    "Tailoring": 15,
    "Content": 20,
    "Sections": 15,
    "ATS Essentials": 10
}

CATEGORY_MAX_SCORES = {
    "Tailoring": 45,
    "Content": 30,
    "Sections": 25,
    "ATS Essentials": 45
}

ALL_RULES = [
    # Tailoring
    rule_soft_skills,
    rule_action_verbs,
    rule_tailored_title,

    # Advanced Intelligence
    rule_section_order,
    rule_experience_density,
    rule_bullet_quality,
    rule_timeline_consistency,
    rule_ats_failure_modes,

    # Structure & Essentials
    rule_missing_sections,
    rule_fragmented_structure,
    rule_header_noise,
    rule_contact_info
]


def evaluate_resume(resume):
    base_score = 100
    issues = []

    category_penalties = defaultdict(int)

    for rule in ALL_RULES:
        result = rule(resume)
        if not result:
            continue

        issues.append(result)

        cat = result["category"]
        pen = result["penalty"]

        if category_penalties[cat] < CATEGORY_CAPS[cat]:
            remaining = CATEGORY_CAPS[cat] - category_penalties[cat]
            category_penalties[cat] += min(pen, remaining)

    total_penalty = sum(category_penalties.values())
    final_score = max(base_score - total_penalty, 0)

    # ---- CATEGORY SCORES (OXFORDCV STYLE) ----
    category_scores = {}

    for cat, max_score in CATEGORY_MAX_SCORES.items():
        penalty = category_penalties.get(cat, 0)
        # Scale penalty proportionally
        scaled_penalty = round((penalty / CATEGORY_CAPS[cat]) * max_score) if CATEGORY_CAPS[cat] else 0
        category_scores[cat] = max(max_score - scaled_penalty, 0)

    status = (
        "ATS-Safe" if final_score >= 75
        else "Borderline" if final_score >= 55
        else "High Auto-Reject Risk"
    )

    return {
        "score": final_score,
        "status": status,
        "issues": issues,
        "category_scores": category_scores,
        "category_max_scores": CATEGORY_MAX_SCORES
    }
