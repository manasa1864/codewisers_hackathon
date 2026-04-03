"""
readiness.py — Deterministic Readiness Model (No Calibration)

readiness_score = 0.6 × current_test_score + 0.4 × completion_percentage

Target thresholds are generated from the Company Intelligence Layer,
not from historical data calibration.
"""

# ── Target threshold tables (Company Intelligence) ──────────────
# These are rule-based targets per importance level
IMPORTANCE_TARGETS = {
    "high":   80.0,
    "medium": 60.0,
    "low":    40.0,
    "none":   0.0,
}

# Readiness brackets
READINESS_LEVELS = [
    (80, "Excellent",  "You are well-prepared for this role."),
    (65, "Good",       "Strong preparation with minor gaps to address."),
    (50, "Moderate",   "Decent foundation but several areas need improvement."),
    (35, "Developing", "Clear gaps exist — focused effort needed."),
    ( 0, "Beginner",   "Significant preparation required across multiple areas."),
]


def compute_target_thresholds(importance_map: dict) -> dict:
    """
    Generate target score thresholds using Company Intelligence.

    Args:
        importance_map: { "dsa": "high|medium|low|none", "cs": ..., "system_design": ... }

    Returns:
        { "dsa_target": float, "cs_target": float, "system_design_target": float }
    """
    return {
        "dsa_target":           IMPORTANCE_TARGETS.get(importance_map.get("dsa",    "medium"), 60.0),
        "cs_target":            IMPORTANCE_TARGETS.get(importance_map.get("cs",     "medium"), 60.0),
        "system_design_target": IMPORTANCE_TARGETS.get(importance_map.get("system_design", "medium"), 60.0),
    }


def compute_readiness_score(
    test_scores: dict,
    completion: dict,
    sections: list,
) -> float:
    """
    readiness_score = 0.6 × avg_test_score + 0.4 × overall_completion

    Args:
        test_scores:  { "dsa_score": float, "cs_score": float, "system_design_score": float }
        completion:   { "dsa": float, "cs": float, "system_design": float, "overall": float }
        sections:     List of included section names

    Returns:
        float in [0, 100]
    """
    section_score_keys = {
        "DSA":             "dsa_score",
        "CS Fundamentals": "cs_score",
        "System Design":   "system_design_score",
    }

    included_scores = []
    for sec in sections:
        key = section_score_keys.get(sec)
        if key and key in test_scores:
            included_scores.append(float(test_scores[key]))

    avg_test = sum(included_scores) / len(included_scores) if included_scores else 0.0
    overall_completion = float(completion.get("overall", 0.0))

    readiness = 0.6 * avg_test + 0.4 * overall_completion
    return round(min(readiness, 100.0), 2)


def get_readiness_level(readiness_score: float) -> dict:
    """Return readiness level label and description."""
    for threshold, label, desc in READINESS_LEVELS:
        if readiness_score >= threshold:
            return {"level": label, "description": desc}
    return {"level": "Beginner", "description": READINESS_LEVELS[-1][2]}


def build_threshold_config_for_gap_detection(
    company: str,
    importance_map: dict,
    targets: dict,
) -> dict:
    """
    Build threshold_config in the format expected by gap_detection.py.
    No calibration — purely rule-based from Company Intelligence.
    """
    company_key = company

    thresholds_for_company = {
        "medium_accuracy_min":        targets["dsa_target"],
        "system_design_min":          targets["system_design_target"],
        "total_problems_min":         150 if importance_map.get("dsa") in ("high","medium") else 50,
        "cs_min":                     targets["cs_target"],
        "consistency_min":            8   if importance_map.get("dsa") == "high" else 5,
        "system_design_topics_min":   8   if importance_map.get("system_design") == "high" else 4,
    }

    return {
        "source":  "company_intelligence",
        "version": "v2.0",
        "thresholds": {
            company_key: thresholds_for_company,
        },
    }


def build_user_data_for_gap_detection(
    company: str,
    role: str,
    scores: dict,
    completion: dict,
) -> dict:
    """Convert CareerForge profile data into gap_detection.py's expected format."""
    return {
        "target_company": company,
        "role":           role,
        "dsa": {
            "easy_accuracy":    min(scores.get("dsa_score", 0) + 10, 100),
            "medium_accuracy":  scores.get("dsa_score", 0),
            "hard_attempts":    5,
            "total_problems":   int(completion.get("dsa", 0) * 2),
        },
        "system_design": {
            "score":            scores.get("system_design_score", 0),
            "topics_completed": int(completion.get("system_design", 0) / 10),
        },
        "cs_fundamentals": {
            "os":   scores.get("cs_score", 0),
            "dbms": scores.get("cs_score", 0),
            "cn":   scores.get("cs_score", 0),
        },
        "consistency": {
            "days_active_last_14": 14,
        },
    }


def generate_readiness_explanation(
    readiness_score: float,
    test_scores: dict,
    targets: dict,
    completion: dict,
) -> str:
    """Generate human-readable readiness explanation."""
    level_info = get_readiness_level(readiness_score)
    avg_test   = round(
        (test_scores.get("dsa_score",0) + test_scores.get("cs_score",0) +
         test_scores.get("system_design_score",0)) / 3, 1
    )
    overall_comp = completion.get("overall", 0)

    return (
        f"Your CareerForge readiness score is {readiness_score:.1f}/100 — {level_info['level']}. "
        f"{level_info['description']} "
        f"Score breakdown: test performance contributes {0.6*avg_test:.1f} points "
        f"(60% weight × {avg_test:.1f} avg score), "
        f"completion contributes {0.4*overall_comp:.1f} points "
        f"(40% weight × {overall_comp:.1f}% completion)."
    )
