"""
questions.py — Deterministic Question Selection Engine
- Options are shuffled per-question so correct answer is never always option A
- test_round param gives different questions for periodic tests
"""
import json
from pathlib import Path

DATA_DIR    = Path(__file__).parent / "data"
QUESTIONS_F = DATA_DIR / "questions.json"

QUESTIONS_PER_SECTION = 15

IMPORTANCE_DIFFICULTY = {
    "high":   "hard",
    "medium": "medium",
    "low":    "easy",
    "none":   None,
}


def _load_questions() -> list:
    with open(QUESTIONS_F) as f:
        return json.load(f)


def _deterministic_seed(profile_id: str, test_round: int = 0) -> int:
    h = 0
    for ch in profile_id:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    h = (h ^ (test_round * 2654435761)) & 0xFFFFFFFF
    return h


def _lcg_next(state: int) -> int:
    return (state * 1664525 + 1013904223) & 0xFFFFFFFF


def _deterministic_shuffle(items: list, seed: int) -> list:
    items = list(items)
    state = seed
    for i in range(len(items) - 1, 0, -1):
        state = _lcg_next(state)
        j = state % (i + 1)
        items[i], items[j] = items[j], items[i]
    return items


def _shuffle_options(question: dict, q_seed: int) -> dict:
    """Shuffle options deterministically. correct_answer text is unchanged."""
    q = dict(question)
    q["options"] = _deterministic_shuffle(q["options"], q_seed)
    return q


def _get_pool(questions: list, section: str, difficulty: str) -> list:
    return [q for q in questions
            if q["section"] == section and q["difficulty"] == difficulty]


def select_questions_for_profile(
    profile_id: str,
    sections: list,
    importance_map: dict,
    test_round: int = 0,
) -> dict:
    all_q = _load_questions()
    seed  = _deterministic_seed(profile_id, test_round)
    result = {}

    imp_key = {
        "DSA":             "dsa",
        "CS Fundamentals": "cs",
        "System Design":   "system_design",
    }

    for section in sections:
        imp        = importance_map.get(imp_key.get(section, ""), "medium")
        difficulty = IMPORTANCE_DIFFICULTY.get(imp, "medium")
        if difficulty is None:
            continue

        pool = _get_pool(all_q, section, difficulty)
        if len(pool) < QUESTIONS_PER_SECTION:
            if difficulty == "hard":
                pool += _get_pool(all_q, section, "medium")
            elif difficulty == "easy":
                pool += _get_pool(all_q, section, "medium")
            else:
                pool += _get_pool(all_q, section, "easy")
                pool += _get_pool(all_q, section, "hard")

        seen, unique = set(), []
        for q in pool:
            if q["id"] not in seen:
                seen.add(q["id"])
                unique.append(q)

        shuffled = _deterministic_shuffle(unique, seed ^ (hash(section) & 0xFFFFFFFF))
        selected = shuffled[:QUESTIONS_PER_SECTION]

        # Shuffle each question's options so correct is not always first
        opt_shuffled = []
        for q in selected:
            q_seed = (seed ^ (q["id"] * 2246822519)) & 0xFFFFFFFF
            opt_shuffled.append(_shuffle_options(q, q_seed))

        result[section] = opt_shuffled

    return result


def score_answers(questions_by_section: dict, answers: dict) -> dict:
    section_scores = {}
    details        = {}

    for section, questions in questions_by_section.items():
        correct = 0
        for q in questions:
            qid        = str(q["id"])
            given      = answers.get(qid, "")
            is_correct = (given == q["correct_answer"])
            if is_correct:
                correct += 1
            details[qid] = {
                "correct":        is_correct,
                "correct_answer": q["correct_answer"],
                "given_answer":   given,
                "question":       q["question"],
                "section":        section,
            }
        score = round(correct / len(questions) * 100, 1) if questions else 0.0
        section_scores[section] = score

    included = list(section_scores.values())
    avg      = sum(included) / len(included) if included else 0.0
    level    = "beginner" if avg < 40 else "intermediate" if avg <= 70 else "advanced"

    return {
        "section_scores":      section_scores,
        "dsa_score":           section_scores.get("DSA", 0.0),
        "cs_score":            section_scores.get("CS Fundamentals", 0.0),
        "system_design_score": section_scores.get("System Design", 0.0),
        "level":               level,
        "details":             details,
    }


def get_adaptive_difficulty(score: float) -> dict:
    if score < 40:
        return {"difficulty": "easy",   "volume": "high"}
    elif score <= 70:
        return {"difficulty": "medium", "volume": "medium"}
    else:
        return {"difficulty": "hard",   "volume": "low"}
