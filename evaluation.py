"""
evaluation.py — Deterministic Evaluation Engine
Computes user readiness score using dynamic weights.

Input scales:
  - medium_accuracy : 0–1
  - confidence      : 0–1
  - problems_solved : raw count (capped at 200)
  - topics_covered  : raw count (capped at 30)
  - subjects_covered: raw count (capped at 6)
  - company_attributes intensities: 0–1

Output: all scores on 0–100 scale; weights on 0–1 scale.
All computations are strictly deterministic.
"""

# ─────────────────────────────────────────────
#  STEP 2: Role importance multipliers
# ─────────────────────────────────────────────
ROLE_IMPORTANCE = {
    "SDE": {
        "dsa": 1.0,
        "system_design": 0.8,
        "cs": 0.9,
    },
    "BACKEND": {
        "dsa": 0.8,
        "system_design": 1.0,
        "cs": 0.9,
    },
    "QUANT": {
        "dsa": 0.9,
        "system_design": 0.5,
        "cs": 0.7,
    },
    "FRONTEND": {
        "dsa": 0.7,
        "system_design": 0.7,
        "cs": 0.8,
    },
    "FULLSTACK": {
        "dsa": 0.8,
        "system_design": 0.8,
        "cs": 0.9,
    },
    "DEFAULT": {
        "dsa": 0.85,
        "system_design": 0.75,
        "cs": 0.80,
    },
}

MAX_PROBLEMS_SOLVED = 200.0
MAX_TOPICS_COVERED  = 20.0   # realistic max: ~20 core system design topics
MAX_SUBJECTS        = 6.0    # OS, DBMS, CN, Algo, Networks, Architecture
MAX_HARD_ATTEMPTS   = 50.0
HARD_ATTEMPT_BONUS  = 10.0   # max bonus points for hard attempts


def _get_role_importance(role: str) -> dict:
    """Return the role importance multipliers (defaults if unknown role)."""
    key = (role or "DEFAULT").upper()
    return ROLE_IMPORTANCE.get(key, ROLE_IMPORTANCE["DEFAULT"])


# ─────────────────────────────────────────────
#  STEP 1: Compute skill scores (0–100)
# ─────────────────────────────────────────────

def compute_dsa_score(dsa: dict) -> float:
    """
    DSA score (0–100):
      1. Scale problems_solved (cap at 200) → [0, 100]
      2. Multiply by medium_accuracy (0–1)
      3. Add bonus for hard_attempts (capped at MAX_HARD_ATTEMPTS, gives up to HARD_ATTEMPT_BONUS pts)
    """
    problems_solved  = float(dsa.get("problems_solved", 0))
    medium_accuracy  = float(dsa.get("medium_accuracy", 0))  # 0–1
    hard_attempts    = float(dsa.get("hard_attempts", 0))

    scaled_problems  = min(problems_solved, MAX_PROBLEMS_SOLVED) / MAX_PROBLEMS_SOLVED * 100.0
    base_score       = scaled_problems * medium_accuracy
    hard_bonus       = min(hard_attempts, MAX_HARD_ATTEMPTS) / MAX_HARD_ATTEMPTS * HARD_ATTEMPT_BONUS
    raw_score        = base_score + hard_bonus
    return min(round(raw_score, 2), 100.0)


def compute_system_design_score(system_design: dict) -> float:
    """
    System Design score (0–100):
      1. Scale topics_covered (cap at 30) → [0, 100]
      2. Multiply by confidence (0–1)
    """
    topics_covered = float(system_design.get("topics_covered", 0))
    confidence     = float(system_design.get("confidence", 0))  # 0–1

    scaled_topics  = min(topics_covered, MAX_TOPICS_COVERED) / MAX_TOPICS_COVERED * 100.0
    raw_score      = scaled_topics * confidence
    return min(round(raw_score, 2), 100.0)


def compute_cs_score(cs_fundamentals: dict) -> float:
    """
    CS Fundamentals score (0–100):
      1. Scale subjects_covered (cap at 6) → [0, 100]
      2. Multiply by confidence (0–1)
    """
    subjects_covered = float(cs_fundamentals.get("subjects_covered", 0))
    confidence       = float(cs_fundamentals.get("confidence", 0))  # 0–1

    scaled_subjects  = min(subjects_covered, MAX_SUBJECTS) / MAX_SUBJECTS * 100.0
    raw_score        = scaled_subjects * confidence
    return min(round(raw_score, 2), 100.0)


# ─────────────────────────────────────────────
#  STEP 3: Deficiency factor
# ─────────────────────────────────────────────

def compute_deficiency_factor(score: float) -> float:
    """
    deficiency        = (100 - score) / 100
    deficiency_factor = 1 + deficiency
    Higher deficiency → higher weight (more focus needed on weaker areas).
    """
    deficiency = (100.0 - score) / 100.0
    return round(1.0 + deficiency, 4)


# ─────────────────────────────────────────────
#  STEP 4 & 5: Raw weights → Normalized weights
# ─────────────────────────────────────────────

def compute_weights(
    scores: dict,
    company_attributes: dict,
    role_importance: dict,
) -> dict:
    """
    Step 4: raw_weight = intensity × role_importance × deficiency_factor
    Step 5: Normalize so they sum to 1.
    Returns normalized weights dict.
    """
    dsa_intensity  = float(company_attributes.get("dsa_intensity", 0.5))
    sd_intensity   = float(company_attributes.get("system_design_intensity", 0.5))
    cs_depth       = float(company_attributes.get("cs_depth", 0.5))

    df_dsa = compute_deficiency_factor(scores["dsa"])
    df_sd  = compute_deficiency_factor(scores["system_design"])
    df_cs  = compute_deficiency_factor(scores["cs"])

    raw_dsa = dsa_intensity * role_importance["dsa"] * df_dsa
    raw_sd  = sd_intensity  * role_importance["system_design"] * df_sd
    raw_cs  = cs_depth      * role_importance["cs"]  * df_cs

    total = raw_dsa + raw_sd + raw_cs
    if total == 0:
        return {"dsa": 1/3, "system_design": 1/3, "cs": 1/3}

    return {
        "dsa":           round(raw_dsa / total, 4),
        "system_design": round(raw_sd  / total, 4),
        "cs":            round(raw_cs  / total, 4),
    }


# ─────────────────────────────────────────────
#  STEP 6: Final readiness score
# ─────────────────────────────────────────────

def compute_final_score(scores: dict, weights: dict) -> float:
    """Weighted sum of all skill scores → overall readiness (0–100)."""
    total = (
        scores["dsa"]           * weights["dsa"] +
        scores["system_design"] * weights["system_design"] +
        scores["cs"]            * weights["cs"]
    )
    return round(total, 2)


# ─────────────────────────────────────────────
#  STEP 7: Explainability
# ─────────────────────────────────────────────

def build_reasoning(
    scores: dict,
    weights: dict,
    final_score: float,
    role: str,
    company_attributes: dict,
) -> list:
    """Build a list of human-readable reasoning strings."""
    reasoning = []

    reasoning.append(
        f"DSA Score: {scores['dsa']:.1f}/100. "
        f"Computed from scaled problems_solved × medium_accuracy + hard_attempt bonus."
    )
    reasoning.append(
        f"System Design Score: {scores['system_design']:.1f}/100. "
        f"Computed from scaled topics_covered × confidence."
    )
    reasoning.append(
        f"CS Fundamentals Score: {scores['cs']:.1f}/100. "
        f"Computed from scaled subjects_covered × confidence."
    )
    reasoning.append(
        f"Role '{role}' importance multipliers applied: "
        f"DSA={_get_role_importance(role)['dsa']}, "
        f"SD={_get_role_importance(role)['system_design']}, "
        f"CS={_get_role_importance(role)['cs']}."
    )
    reasoning.append(
        f"Deficiency factors applied (weaker areas get higher weight): "
        f"DSA factor={compute_deficiency_factor(scores['dsa']):.4f}, "
        f"SD factor={compute_deficiency_factor(scores['system_design']):.4f}, "
        f"CS factor={compute_deficiency_factor(scores['cs']):.4f}."
    )
    reasoning.append(
        f"Normalized weights — DSA: {weights['dsa']:.4f}, "
        f"System Design: {weights['system_design']:.4f}, "
        f"CS: {weights['cs']:.4f}."
    )
    reasoning.append(
        f"Overall readiness score = "
        f"({scores['dsa']:.1f} × {weights['dsa']:.4f}) + "
        f"({scores['system_design']:.1f} × {weights['system_design']:.4f}) + "
        f"({scores['cs']:.1f} × {weights['cs']:.4f}) = {final_score:.2f}."
    )

    return reasoning


# ─────────────────────────────────────────────
#  MAIN EVALUATION FUNCTION
# ─────────────────────────────────────────────

def evaluate(user_profile: dict, target: dict) -> dict:
    """
    Full evaluation pipeline.

    Args:
        user_profile: {
            "dsa": { "problems_solved", "medium_accuracy" (0–1), "hard_attempts" },
            "system_design": { "topics_covered", "confidence" (0–1) },
            "cs_fundamentals": { "subjects_covered", "confidence" (0–1) }
        }
        target: {
            "company_attributes": { "dsa_intensity", "system_design_intensity", "cs_depth" },
            "role": str,
            "experience_level": str
        }

    Returns:
        {
            "scores":       { "dsa", "system_design", "cs" },
            "weights":      { "dsa", "system_design", "cs" },
            "final_score":  float,
            "reasoning":    [str, ...]
        }
    """
    dsa_data  = user_profile.get("dsa", {})
    sd_data   = user_profile.get("system_design", {})
    cs_data   = user_profile.get("cs_fundamentals", {})

    company_attributes = target.get("company_attributes", {})
    role               = target.get("role", "DEFAULT")
    role_importance    = _get_role_importance(role)

    # Step 1
    scores = {
        "dsa":           compute_dsa_score(dsa_data),
        "system_design": compute_system_design_score(sd_data),
        "cs":            compute_cs_score(cs_data),
    }

    # Steps 3–5
    weights = compute_weights(scores, company_attributes, role_importance)

    # Step 6
    final_score = compute_final_score(scores, weights)

    # Step 7
    reasoning = build_reasoning(scores, weights, final_score, role, company_attributes)

    return {
        "scores":      scores,
        "weights":     weights,
        "final_score": final_score,
        "reasoning":   reasoning,
    }
