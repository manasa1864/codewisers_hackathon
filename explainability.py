"""
explainability.py — Deterministic Explainability Layer
Generates clear, structured, human-readable explanations for all system outputs.

All explanations are derived only from provided data and predefined rules.
No ML, no probabilistic reasoning, no assumptions.
"""

# ─────────────────────────────────────────────
#  FUNCTION 1: explain_score_calculation
# ─────────────────────────────────────────────
def explain_score_calculation(scores: dict, weights: dict) -> str:
    """
    Explain how the overall readiness score was computed,
    describing each component's contribution.
    """
    dsa_score = scores.get("dsa", scores.get("dsa_score", 0))
    sd_score  = scores.get("system_design", scores.get("system_design_score", 0))
    cs_score  = scores.get("cs", scores.get("cs_fundamentals_score", 0))
    consistency_score = scores.get("consistency", scores.get("consistency_score", None))

    dsa_w = weights.get("dsa", weights.get("dsa_weight", 0))
    sd_w  = weights.get("system_design", weights.get("system_design_weight", 0))
    cs_w  = weights.get("cs", weights.get("cs_weight", 0))
    con_w = weights.get("consistency", weights.get("consistency_weight", 0))

    dsa_pct = round(dsa_w * 100, 1)
    sd_pct  = round(sd_w * 100, 1)
    cs_pct  = round(cs_w * 100, 1)
    con_pct = round(con_w * 100, 1)

    parts = [
        f"Your overall readiness score is computed as a weighted combination "
        f"of DSA, System Design, CS Fundamentals"
    ]
    if consistency_score is not None:
        parts[0] += ", and Consistency"
    parts[0] += "."

    parts.append(
        f"DSA contributes {dsa_pct}% (score: {dsa_score:.1f}), "
        f"System Design contributes {sd_pct}% (score: {sd_score:.1f}), "
        f"CS Fundamentals contributes {cs_pct}% (score: {cs_score:.1f})"
        + (f", Consistency contributes {con_pct}% (score: {consistency_score:.1f})."
           if consistency_score is not None else ".")
    )
    parts.append(
        "Weights are dynamically computed based on your deficiency in each area, "
        "the company's skill intensity requirements, and role-based importance multipliers."
    )

    return " ".join(parts)


# ─────────────────────────────────────────────
#  FUNCTION 2: explain_individual_scores
# ─────────────────────────────────────────────
def explain_individual_scores(scores: dict) -> dict:
    """
    Explain each score separately.
    Returns a dictionary of explanations per skill.
    """
    dsa_score = scores.get("dsa", scores.get("dsa_score", None))
    sd_score  = scores.get("system_design", scores.get("system_design_score", None))
    cs_score  = scores.get("cs", scores.get("cs_fundamentals_score", None))

    explanations = {}

    if dsa_score is not None:
        level = "strong" if dsa_score >= 70 else ("moderate" if dsa_score >= 50 else "weak")
        explanations["dsa"] = (
            f"Your DSA score is {dsa_score:.1f}/100, indicating a {level} performance. "
            f"This is derived from your problems solved (capped at 200), "
            f"medium accuracy (0–1 scale), and a bonus for hard problem attempts."
        )

    if sd_score is not None:
        level = "strong" if sd_score >= 70 else ("moderate" if sd_score >= 50 else "weak")
        explanations["system_design"] = (
            f"Your System Design score is {sd_score:.1f}/100, indicating {level} readiness. "
            f"This is computed from the number of topics covered (scaled to 30 max) "
            f"multiplied by your confidence level."
        )

    if cs_score is not None:
        level = "strong" if cs_score >= 70 else ("moderate" if cs_score >= 50 else "weak")
        explanations["cs_fundamentals"] = (
            f"Your CS Fundamentals score is {cs_score:.1f}/100, indicating {level} readiness. "
            f"Computed from subjects covered (scaled to 6 max) multiplied by confidence."
        )

    # Consistency may be absent in scores from Evaluation Engine
    con_score = scores.get("consistency", scores.get("consistency_score", None))
    if con_score is not None:
        level = "strong" if con_score >= 70 else ("moderate" if con_score >= 50 else "weak")
        explanations["consistency"] = (
            f"Your Consistency score is {con_score:.1f}/100, indicating {level} discipline. "
            f"Based on active practice days in the last 14 days."
        )
    else:
        explanations["consistency"] = (
            "Consistency score not separately computed in this evaluation. "
            "Refer to the gap analysis for consistency-related feedback."
        )

    return explanations


# ─────────────────────────────────────────────
#  FUNCTION 3: explain_gap
# ─────────────────────────────────────────────
def explain_gap(gap_object: dict) -> str:
    """
    Generate explanation for a single gap.
    Includes: current vs required, rule triggered, threshold source and version.
    """
    name     = gap_object.get("gap_name", "metric")
    current  = gap_object.get("current_value", "N/A")
    required = gap_object.get("required_value", "N/A")
    rule     = gap_object.get("rule_triggered", "threshold rule")
    source   = gap_object.get("threshold_source", "static")
    version  = gap_object.get("threshold_version", "v1.0")
    severity = gap_object.get("severity", "Medium")

    return (
        f"[{severity} Severity] Your {name} is {current}, "
        f"which is below the required {required}. "
        f"This triggered the rule: '{rule}'. "
        f"The threshold is derived from a {source} configuration (version {version})."
    )


# ─────────────────────────────────────────────
#  FUNCTION 4: explain_all_gaps
# ─────────────────────────────────────────────
def explain_all_gaps(gaps_list: list) -> list:
    """Iterate over all gaps and generate an explanation for each."""
    return [explain_gap(gap) for gap in gaps_list]


# ─────────────────────────────────────────────
#  FUNCTION 5: map_recommendations_to_gaps
# ─────────────────────────────────────────────
def map_recommendations_to_gaps(gaps: list, recommendations: list) -> dict:
    """
    Create mapping: gap_name → list of actions addressing it.
    """
    mapping: dict[str, list] = {}

    # Build a set of gap names for reference
    gap_names = {g.get("gap_name", "") for g in gaps}

    for rec in recommendations:
        # recommendations may be decision objects or flat action dicts
        mapped_gap = rec.get("gap_name") or rec.get("mapped_gap", "")
        if not mapped_gap and gap_names:
            mapped_gap = next(iter(gap_names))  # fallback

        mapping.setdefault(mapped_gap, []).append(rec)

    return mapping


# ─────────────────────────────────────────────
#  FUNCTION 6: explain_recommendation
# ─────────────────────────────────────────────
def explain_recommendation(action: dict, gap_name: str) -> str:
    """
    Explain why a specific recommendation is given, linking it to the gap.
    """
    task      = action.get("recommended_task") or action.get("action", "Improve this area.")
    area      = action.get("resource_type", "preparation area")
    priority  = action.get("priority", None)
    pri_label = {1: "High", 2: "Medium", 3: "Low"}.get(priority, "")

    priority_str = f" (Priority: {pri_label})" if pri_label else ""

    return (
        f"This recommendation{priority_str} is given because of the gap: '{gap_name}'. "
        f"Action: {task} "
        f"Addressing this gap will improve your readiness in the {area} area."
    )


# ─────────────────────────────────────────────
#  FUNCTION 7: explain_all_recommendations
# ─────────────────────────────────────────────
def explain_all_recommendations(gaps: list, recommendations: list) -> list:
    """
    Use mapping function to generate an explanation for each recommendation.
    """
    if not recommendations:
        return []

    mapping = map_recommendations_to_gaps(gaps, recommendations)
    explanations = []

    for gap_name, actions in mapping.items():
        for action in actions:
            explanations.append(explain_recommendation(action, gap_name))

    return explanations


# ─────────────────────────────────────────────
#  FUNCTION 8: generate_summary
# ─────────────────────────────────────────────
def generate_summary(scores: dict, gaps: list, recommendations: list) -> str:
    """
    High-level summary: readiness level, key weaknesses, suggested focus.

    Two dimensions are considered:
      1. Absolute readiness score   (from Evaluation Engine)
      2. Gap status                 (from Gap Detection Engine)

    If no gaps exist the user meets company thresholds regardless of
    absolute score, which is acknowledged explicitly.
    """
    final = scores.get("final_score", scores.get("overall_readiness", None))
    if final is None:
        dsa = scores.get("dsa", scores.get("dsa_score", 0))
        sd  = scores.get("system_design", scores.get("system_design_score", 0))
        cs  = scores.get("cs", scores.get("cs_fundamentals_score", 0))
        final = round((dsa + sd + cs) / 3, 1)

    high_gaps   = [g["gap_name"] for g in gaps if g.get("severity") == "High"]
    medium_gaps = [g["gap_name"] for g in gaps if g.get("severity") == "Medium"]
    no_gaps     = len(gaps) == 0

    # ── Readiness label ──────────────────────────────────────────
    if no_gaps and final >= 60:
        level = "HIGH — All thresholds met; you are well-prepared"
    elif no_gaps:
        level = "MODERATE — Thresholds met; room to improve absolute score"
    elif final >= 70:
        level = "MODERATE — Strong absolute score but some gaps remain"
    elif final >= 50:
        level = "LOW — Gaps detected and absolute score needs improvement"
    else:
        level = "CRITICAL — Major gaps and low absolute readiness"

    # ── Weakness summary ─────────────────────────────────────────
    weakness_str = ""
    if high_gaps:
        weakness_str += f"Critical weaknesses: {', '.join(high_gaps)}. "
    if medium_gaps:
        weakness_str += f"Moderate weaknesses: {', '.join(medium_gaps)}. "
    if no_gaps:
        weakness_str = "No preparation gaps detected against company thresholds. "

    # ── Suggested focus ──────────────────────────────────────────
    high_recs = [r.get("recommended_task", "") for r in recommendations
                 if r.get("priority") == 1]
    focus_str = f"Priority focus: {high_recs[0]}" if high_recs else (
        "Continue strengthening all areas for a higher absolute score." if no_gaps else ""
    )

    return (
        f"Overall Readiness Level: {level} (score: {final:.1f}/100). "
        f"{weakness_str}"
        f"{focus_str}"
    )


# ─────────────────────────────────────────────
#  FUNCTION 9: generate_full_explanation (main)
# ─────────────────────────────────────────────
def generate_full_explanation(
    evaluation_output: dict,
    gaps_list: list,
    decisions_output: dict,
    company_context: dict = None,
) -> dict:
    """
    Main function: calls all sub-functions and returns the full
    structured explainability object.

    Args:
        evaluation_output:  { "scores": {...}, "weights": {...}, "final_score": float }
        gaps_list:          list of gap dicts from Gap Detection Engine
        decisions_output:   { "action_plan": {...}, "decisions": [...] }
        company_context:    { "company_type": str, "focus_areas": [...] }
    """
    scores  = evaluation_output.get("scores", {})
    weights = evaluation_output.get("weights", {})
    # Attach final score so generate_summary can find it
    scores_with_total = {**scores, "final_score": evaluation_output.get("final_score", 0)}

    decisions = decisions_output.get("decisions", []) if decisions_output else []

    # Handle missing inputs gracefully
    if not gaps_list:
        gap_exp  = ["No preparation gaps were detected. Your preparation looks strong!"]
        rec_exp  = []
    else:
        gap_exp  = explain_all_gaps(gaps_list)
        rec_exp  = explain_all_recommendations(gaps_list, decisions)

    if not decisions:
        rec_exp = ["No specific recommendations — you appear well-prepared!"]

    score_explanation       = explain_score_calculation(scores, weights)
    individual_explanations = explain_individual_scores(scores)
    summary                 = generate_summary(scores_with_total, gaps_list, decisions)

    return {
        "score_explanation":          score_explanation,
        "individual_score_explanations": individual_explanations,
        "gap_explanations":           gap_exp,
        "recommendation_explanations": rec_exp,
        "summary":                    summary,
    }
