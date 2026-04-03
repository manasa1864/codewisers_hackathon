"""
decision.py — Deterministic Decision Engine
Converts identified preparation gaps into structured, prioritized, and
explainable action recommendations.

All logic is strictly rule-based and deterministic.
The engine does NOT modify input gaps, thresholds, or evaluation results.
"""

from typing import Optional

# ─────────────────────────────────────────────
#  PRIORITY CONSTANTS
# ─────────────────────────────────────────────
PRIORITY_MAP = {"High": 1, "Medium": 2, "Low": 3}
PRIORITY_LABEL = {1: "high_priority", 2: "medium_priority", 3: "low_priority"}


# ─────────────────────────────────────────────
#  FUNCTION 1: validate_inputs
# ─────────────────────────────────────────────
def validate_inputs(
    gaps: list,
    user_data: dict,
    evaluation_summary: dict,
    importance_profile: dict,
) -> bool:
    """Ensure all required inputs exist. Raise Exception if invalid."""
    if gaps is None:
        raise Exception("gaps list is required.")
    if not user_data:
        raise Exception("user_data is required.")
    if not evaluation_summary:
        raise Exception("evaluation_summary is required.")
    if "final_score" not in evaluation_summary:
        raise Exception("evaluation_summary must contain 'final_score'.")
    if not importance_profile:
        raise Exception("importance_profile is required.")
    return True


# ─────────────────────────────────────────────
#  FUNCTION 2: calculate_priority
# ─────────────────────────────────────────────
def calculate_priority(severity: str, importance_weight: float) -> int:
    """
    Priority considers BOTH severity and importance.
    Base: High→1, Medium→2, Low→3
    Adjustment: importance > 0.7 → decrease by 1 (min 1)
                importance < 0.3 → increase by 1 (max 3)
    """
    base = PRIORITY_MAP.get(severity, 2)
    if importance_weight > 0.7:
        base = max(1, base - 1)
    elif importance_weight < 0.3:
        base = min(3, base + 1)
    return base


# ─────────────────────────────────────────────
#  FUNCTION 3: map_gap_to_action
# ─────────────────────────────────────────────
def map_gap_to_action(gap: dict) -> dict:
    """
    Deterministically map each gap to an action.
    Dispatches to the appropriate handler.
    """
    gap_name = gap.get("gap_name", "")
    gap_type = gap.get("gap_type", "")

    if gap_type == "system_design" and "Topics" in gap_name:
        return handle_system_design_coverage_gap(gap)
    elif gap_type == "system_design":
        return handle_system_design_gap(gap)
    elif gap_type == "dsa" and "Accuracy" in gap_name:
        return handle_medium_problem_gap(gap)
    elif gap_type == "dsa" and "Problems" in gap_name:
        return handle_practice_volume_gap(gap)
    elif gap_type == "consistency":
        return handle_consistency_gap(gap)
    elif gap_type == "cs_fundamentals":
        return handle_cs_fundamentals_gap(gap)
    elif gap_type == "composite":
        return handle_composite_strategy_gap(gap)
    else:
        # Unknown gap → generic action
        return {
            "action_type":       "general_improvement",
            "recommended_task":  "Review and strengthen the identified weak area systematically.",
            "resource_type":     "self_study",
        }


# ─────────────────────────────────────────────
#  FUNCTION 4: get_importance_for_gap
# ─────────────────────────────────────────────
def get_importance_for_gap(gap_name: str, gap_type: str, importance_profile: dict) -> float:
    """
    Map gap → relevant skill importance weight.
    """
    if gap_type == "system_design":
        return importance_profile.get("system_design", 0.5)
    elif gap_type == "dsa":
        return importance_profile.get("dsa", 0.5)
    elif gap_type == "cs_fundamentals":
        return importance_profile.get("cs_fundamentals", 0.5)
    elif gap_type == "consistency":
        # Consistency is cross-cutting; average of all skills
        vals = list(importance_profile.values())
        return round(sum(vals) / len(vals), 4) if vals else 0.5
    elif gap_type == "composite":
        return importance_profile.get("dsa", 0.5)
    return 0.5


# ─────────────────────────────────────────────
#  FUNCTION 5: generate_decision_reasoning
# ─────────────────────────────────────────────
def generate_decision_reasoning(
    gap: dict,
    action: dict,
    importance_weight: float,
    priority: int,
) -> str:
    """
    Explanation MUST include gap name, current vs required values,
    why the action was chosen, role of importance weight, and priority reasoning.
    """
    gap_name    = gap.get("gap_name", "unknown gap")
    current     = gap.get("current_value", "N/A")
    required    = gap.get("required_value", "N/A")
    task        = action.get("recommended_task", "N/A")
    priority_lbl= {1: "High", 2: "Medium", 3: "Low"}.get(priority, "Medium")

    return (
        f"Gap '{gap_name}': current value is {current}, required is {required}. "
        f"Action chosen: '{task}'. "
        f"This area has an importance weight of {importance_weight:.4f} for the target company. "
        f"Final priority is {priority_lbl} (level {priority}) — "
        f"{'high importance accelerated priority.' if importance_weight > 0.7 else ''}"
        f"{'low importance deferred priority.' if importance_weight < 0.3 else ''}"
        f"{'standard severity-based priority.' if 0.3 <= importance_weight <= 0.7 else ''}"
    )


# ─────────────────────────────────────────────
#  FUNCTION 6: create_decision_object
# ─────────────────────────────────────────────
def create_decision_object(
    gap: dict,
    action: dict,
    priority: int,
    importance_weight: float,
) -> dict:
    reasoning = generate_decision_reasoning(gap, action, importance_weight, priority)
    return {
        "gap_name":         gap.get("gap_name"),
        "action_type":      action.get("action_type"),
        "recommended_task": action.get("recommended_task"),
        "resource_type":    action.get("resource_type"),
        "priority":         priority,
        "importance_weight": importance_weight,
        "reasoning":        reasoning,
    }


# ─────────────────────────────────────────────
#  RULE-BASED HANDLER FUNCTIONS (a – g)
# ─────────────────────────────────────────────

def handle_system_design_gap(gap: dict) -> dict:
    """Handler a: System design score is low."""
    return {
        "action_type":       "study_and_practice",
        "recommended_task":  (
            "Study system design fundamentals (scalability, load balancing, caching, "
            "databases). Practice 2 full case studies daily."
        ),
        "resource_type":     "system_design",
    }


def handle_medium_problem_gap(gap: dict) -> dict:
    """Handler b: DSA medium accuracy is low."""
    return {
        "action_type":       "targeted_dsa_practice",
        "recommended_task":  (
            "Solve 20 medium DSA problems per week. "
            "Focus on core patterns: DP, graphs, sliding window, binary search."
        ),
        "resource_type":     "dsa",
    }


def handle_practice_volume_gap(gap: dict) -> dict:
    """Handler c: Total problems solved is low."""
    return {
        "action_type":       "volume_increase",
        "recommended_task":  (
            "Increase daily problem-solving count. "
            "Follow a structured DSA sheet (e.g., Striver A2Z or NeetCode 150)."
        ),
        "resource_type":     "dsa",
    }


def handle_system_design_coverage_gap(gap: dict) -> dict:
    """Handler d: System design topics_completed is low."""
    return {
        "action_type":       "topic_completion",
        "recommended_task":  (
            "Complete missing system design topics. "
            "Maintain a checklist: cover Load Balancers, CDN, Kafka, SQL vs NoSQL, "
            "Microservices, API Gateway, etc."
        ),
        "resource_type":     "system_design",
    }


def handle_consistency_gap(gap: dict) -> dict:
    """Handler e: Activity days in last 14 days is low."""
    return {
        "action_type":       "consistency_enforcement",
        "recommended_task":  (
            "Enforce a daily preparation schedule. "
            "Target minimum 1–2 hours of focused practice per day. "
            "Use a habit tracker to monitor streaks."
        ),
        "resource_type":     "consistency",
    }


def handle_cs_fundamentals_gap(gap: dict) -> dict:
    """Handler f: CS fundamentals subjects are weak."""
    return {
        "action_type":       "fundamentals_revision",
        "recommended_task":  (
            "Revise OS (processes, scheduling, memory management), "
            "DBMS (normalization, transactions, indexing), and "
            "CN (OSI model, TCP/IP, DNS, HTTP). "
            "Practice interview questions for each subject."
        ),
        "resource_type":     "cs_fundamentals",
    }


def handle_composite_strategy_gap(gap: dict) -> dict:
    """Handler g: Accuracy low but volume is already sufficient."""
    return {
        "action_type":       "quality_over_quantity",
        "recommended_task":  (
            "Stop increasing problem count — volume is already sufficient. "
            "Focus on mistake analysis: revisit all incorrectly solved problems, "
            "identify recurring error patterns, and re-solve them."
        ),
        "resource_type":     "composite",
    }


# ─────────────────────────────────────────────
#  FUNCTION 7: generate_all_decisions
# ─────────────────────────────────────────────
def generate_all_decisions(gaps: list, importance_profile: dict) -> list:
    """
    For each gap: map to action, get importance weight,
    calculate priority, create decision object.
    """
    decisions = []
    for gap in gaps:
        gap_name = gap.get("gap_name", "")
        gap_type = gap.get("gap_type", "")
        severity = gap.get("severity", "Medium")

        try:
            action = map_gap_to_action(gap)
        except Exception:
            action = {
                "action_type": "general_improvement",
                "recommended_task": "Address identified weakness systematically.",
                "resource_type": "self_study",
            }

        importance_weight = get_importance_for_gap(gap_name, gap_type, importance_profile)
        priority          = calculate_priority(severity, importance_weight)
        decision          = create_decision_object(gap, action, priority, importance_weight)
        decisions.append(decision)
    return decisions


# ─────────────────────────────────────────────
#  FUNCTION 8: sort_decisions_by_priority
# ─────────────────────────────────────────────
def sort_decisions_by_priority(decisions: list) -> list:
    """Sort ascending: Priority 1 → 2 → 3."""
    return sorted(decisions, key=lambda d: d.get("priority", 2))


# ─────────────────────────────────────────────
#  FUNCTION 9: build_action_plan
# ─────────────────────────────────────────────
def build_action_plan(decisions: list) -> dict:
    """Group decisions into high / medium / low priority buckets."""
    plan = {"high_priority": [], "medium_priority": [], "low_priority": []}
    for d in decisions:
        label = PRIORITY_LABEL.get(d.get("priority", 2), "medium_priority")
        plan[label].append(d)
    return plan


# ─────────────────────────────────────────────
#  FUNCTION 10: run_decision_engine (main pipeline)
# ─────────────────────────────────────────────
def run_decision_engine(
    gaps: list,
    user_data: dict,
    evaluation_summary: dict,
    importance_profile: dict,
) -> dict:
    """
    Full decision engine pipeline:
    validate → generate decisions → sort → build plan → return output.
    """
    validate_inputs(gaps, user_data, evaluation_summary, importance_profile)

    if not gaps:
        return {
            "action_plan": {"high_priority": [], "medium_priority": [], "low_priority": []},
            "decisions":   [],
        }

    decisions        = generate_all_decisions(gaps, importance_profile)
    sorted_decisions = sort_decisions_by_priority(decisions)
    action_plan      = build_action_plan(sorted_decisions)

    return {
        "action_plan": action_plan,
        "decisions":   sorted_decisions,
    }
