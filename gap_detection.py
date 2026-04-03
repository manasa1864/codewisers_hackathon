"""
gap_detection.py — Deterministic Gap Detection Engine
Evaluates user preparation data against thresholds and identifies all gaps.

Rules:
- Strictly deterministic (no ML, no randomness)
- Thresholds are read-only inputs
- Each rule is a separate function
- Missing fields → skip that specific rule
"""

from typing import Optional

# ─────────────────────────────────────────────
#  SEVERITY THRESHOLDS
# ─────────────────────────────────────────────
def calculate_severity(current_value: float, required_value: float) -> str:
    """
    Function 3: Compute severity of a gap.
    difference = required_value - current_value
    Returns: "High", "Medium", or "Low"
    """
    difference = required_value - current_value
    if difference >= 20:
        return "High"
    elif difference >= 10:
        return "Medium"
    else:
        return "Low"


# ─────────────────────────────────────────────
#  EXPLANATION GENERATOR
# ─────────────────────────────────────────────
def generate_explanation(
    gap_name: str,
    current: float,
    required: float,
    rule: str,
    source: str,
    version: str,
) -> str:
    """
    Function 4: Generate a human-readable explanation for a detected gap.
    Must include: current value, required value, rule, threshold source, version.
    """
    return (
        f"Your {gap_name} is {current}, which is below the required {required}. "
        f"This triggered the rule: '{rule}'. "
        f"The threshold is derived from a {source} configuration (version {version})."
    )


# ─────────────────────────────────────────────
#  GAP OBJECT FACTORY
# ─────────────────────────────────────────────
def create_gap_object(
    gap_type: str,
    gap_name: str,
    current_value: float,
    required_value: float,
    rule_triggered: str,
    threshold_source: str,
    threshold_version: str,
) -> dict:
    """
    Function 5: Build a structured gap dictionary.
    Internally calls calculate_severity and generate_explanation.
    """
    severity = calculate_severity(current_value, required_value)
    explanation = generate_explanation(
        gap_name, current_value, required_value,
        rule_triggered, threshold_source, threshold_version
    )
    return {
        "gap_type":          gap_type,
        "gap_name":          gap_name,
        "current_value":     current_value,
        "required_value":    required_value,
        "severity":          severity,
        "rule_triggered":    rule_triggered,
        "threshold_source":  threshold_source,
        "threshold_version": threshold_version,
        "explanation":       explanation,
    }


# ─────────────────────────────────────────────
#  VALIDATION
# ─────────────────────────────────────────────
def validate_inputs(user_data: dict, threshold_config: dict) -> bool:
    """
    Function 1: Validate presence of required fields.
    Raises Exception if threshold_config is missing.
    """
    if not threshold_config:
        raise Exception("threshold_config is required and cannot be None or empty.")
    if "thresholds" not in threshold_config:
        raise Exception("threshold_config must contain a 'thresholds' key.")
    if not user_data:
        raise Exception("user_data is required and cannot be None or empty.")
    required_top = ["target_company", "role", "dsa", "system_design",
                    "cs_fundamentals", "consistency"]
    for field in required_top:
        if field not in user_data:
            raise Exception(f"user_data is missing required field: '{field}'.")
    return True


# ─────────────────────────────────────────────
#  THRESHOLD EXTRACTION
# ─────────────────────────────────────────────
def get_company_thresholds(user_data: dict, threshold_config: dict) -> tuple:
    """
    Function 2: Extract thresholds for user_data["target_company"].
    Returns: (thresholds_dict, threshold_source, threshold_version)
    """
    company = user_data.get("target_company", "Service")
    all_thresholds = threshold_config.get("thresholds", {})
    thresholds = all_thresholds.get(company, all_thresholds.get("Service", {}))
    source  = threshold_config.get("source",  "static")
    version = threshold_config.get("version", "v1.0")
    return thresholds, source, version


# ─────────────────────────────────────────────
#  RULE FUNCTIONS  (6a – 6g)
# ─────────────────────────────────────────────

def check_system_design_gap(
    user_data: dict, thresholds: dict, source: str, version: str
) -> Optional[dict]:
    """Rule 6a: IF system_design.score < system_design_min"""
    try:
        current  = float(user_data["system_design"]["score"])
        required = float(thresholds["system_design_min"])
    except (KeyError, TypeError, ValueError):
        return None   # missing field → skip rule
    if current < required:
        return create_gap_object(
            gap_type="system_design",
            gap_name="System Design Score",
            current_value=current,
            required_value=required,
            rule_triggered="system_design.score < system_design_min",
            threshold_source=source,
            threshold_version=version,
        )
    return None


def check_medium_problem_gap(
    user_data: dict, thresholds: dict, source: str, version: str
) -> Optional[dict]:
    """Rule 6b: IF dsa.medium_accuracy < medium_accuracy_min"""
    try:
        current  = float(user_data["dsa"]["medium_accuracy"])
        required = float(thresholds["medium_accuracy_min"])
    except (KeyError, TypeError, ValueError):
        return None
    if current < required:
        return create_gap_object(
            gap_type="dsa",
            gap_name="DSA Medium Accuracy",
            current_value=current,
            required_value=required,
            rule_triggered="dsa.medium_accuracy < medium_accuracy_min",
            threshold_source=source,
            threshold_version=version,
        )
    return None


def check_practice_volume_gap(
    user_data: dict, thresholds: dict, source: str, version: str
) -> Optional[dict]:
    """Rule 6c: IF dsa.total_problems < total_problems_min"""
    try:
        current  = float(user_data["dsa"]["total_problems"])
        required = float(thresholds["total_problems_min"])
    except (KeyError, TypeError, ValueError):
        return None
    if current < required:
        return create_gap_object(
            gap_type="dsa",
            gap_name="Total Problems Solved",
            current_value=current,
            required_value=required,
            rule_triggered="dsa.total_problems < total_problems_min",
            threshold_source=source,
            threshold_version=version,
        )
    return None


def check_system_design_coverage_gap(
    user_data: dict, thresholds: dict, source: str, version: str
) -> Optional[dict]:
    """Rule 6d: IF system_design.topics_completed < system_design_topics_min"""
    try:
        current  = float(user_data["system_design"]["topics_completed"])
        required = float(thresholds["system_design_topics_min"])
    except (KeyError, TypeError, ValueError):
        return None
    if current < required:
        return create_gap_object(
            gap_type="system_design",
            gap_name="System Design Topics Completed",
            current_value=current,
            required_value=required,
            rule_triggered="system_design.topics_completed < system_design_topics_min",
            threshold_source=source,
            threshold_version=version,
        )
    return None


def check_consistency_gap(
    user_data: dict, thresholds: dict, source: str, version: str
) -> Optional[dict]:
    """Rule 6e: IF consistency.days_active_last_14 < consistency_min"""
    try:
        current  = float(user_data["consistency"]["days_active_last_14"])
        required = float(thresholds["consistency_min"])
    except (KeyError, TypeError, ValueError):
        return None
    if current < required:
        return create_gap_object(
            gap_type="consistency",
            gap_name="Active Days (Last 14)",
            current_value=current,
            required_value=required,
            rule_triggered="consistency.days_active_last_14 < consistency_min",
            threshold_source=source,
            threshold_version=version,
        )
    return None


def check_cs_fundamentals_gap(
    user_data: dict, thresholds: dict, source: str, version: str
) -> Optional[dict]:
    """Rule 6f: IF any(cs_fundamentals subject < cs_min)"""
    try:
        cs_min    = float(thresholds["cs_min"])
        cs_scores = user_data["cs_fundamentals"]
    except (KeyError, TypeError, ValueError):
        return None

    weak_subjects = []
    lowest_val = None
    for subj, val in cs_scores.items():
        try:
            v = float(val)
        except (TypeError, ValueError):
            continue
        if v < cs_min:
            weak_subjects.append(f"{subj}={v}")
            if lowest_val is None or v < lowest_val:
                lowest_val = v

    if weak_subjects:
        current = lowest_val
        return create_gap_object(
            gap_type="cs_fundamentals",
            gap_name=f"CS Fundamentals ({', '.join(weak_subjects)})",
            current_value=current,
            required_value=cs_min,
            rule_triggered="any(cs_fundamentals subject) < cs_min",
            threshold_source=source,
            threshold_version=version,
        )
    return None


def check_composite_strategy_gap(
    user_data: dict, thresholds: dict, source: str, version: str
) -> Optional[dict]:
    """
    Rule 6g: IF (medium_accuracy < threshold) AND (total_problems > threshold)
    Composite rule — accuracy low but volume is sufficient.
    """
    try:
        medium_accuracy = float(user_data["dsa"]["medium_accuracy"])
        total_problems  = float(user_data["dsa"]["total_problems"])
        accuracy_min    = float(thresholds["medium_accuracy_min"])
        problems_min    = float(thresholds["total_problems_min"])
    except (KeyError, TypeError, ValueError):
        return None

    if medium_accuracy < accuracy_min and total_problems > problems_min:
        return create_gap_object(
            gap_type="composite",
            gap_name="Strategy Gap (Low Accuracy Despite High Volume)",
            current_value=medium_accuracy,
            required_value=accuracy_min,
            rule_triggered=(
                "dsa.medium_accuracy < medium_accuracy_min "
                "AND dsa.total_problems > total_problems_min"
            ),
            threshold_source=source,
            threshold_version=version,
        )
    return None


# ─────────────────────────────────────────────
#  ALL-GAPS EVALUATOR
# ─────────────────────────────────────────────

def evaluate_all_gaps(
    user_data: dict, thresholds: dict, source: str, version: str
) -> list:
    """
    Function 7: Call all rule functions and collect non-null gaps.
    """
    rule_functions = [
        check_system_design_gap,
        check_medium_problem_gap,
        check_practice_volume_gap,
        check_system_design_coverage_gap,
        check_consistency_gap,
        check_cs_fundamentals_gap,
        check_composite_strategy_gap,
    ]
    gaps = []
    for rule_fn in rule_functions:
        result = rule_fn(user_data, thresholds, source, version)
        if result is not None:
            gaps.append(result)
    return gaps


# ─────────────────────────────────────────────
#  SORT BY SEVERITY
# ─────────────────────────────────────────────

SEVERITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

def sort_gaps_by_severity(gaps: list) -> list:
    """
    Function 8: Sort gaps descending by severity.
    Order: High → Medium → Low
    """
    return sorted(gaps, key=lambda g: SEVERITY_ORDER.get(g.get("severity", "Low"), 2))


# ─────────────────────────────────────────────
#  MAIN PIPELINE FUNCTION
# ─────────────────────────────────────────────

def run_gap_detection(user_data: dict, threshold_config: dict) -> list:
    """
    Function 9 (main): Full gap detection pipeline.
    validate_inputs → get_company_thresholds → evaluate_all_gaps → sort_gaps_by_severity
    Returns sorted list of gap objects.
    """
    validate_inputs(user_data, threshold_config)
    thresholds, source, version = get_company_thresholds(user_data, threshold_config)
    gaps = evaluate_all_gaps(user_data, thresholds, source, version)
    return sort_gaps_by_severity(gaps)
