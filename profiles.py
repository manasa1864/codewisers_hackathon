"""
profiles.py — Multi-Profile Management
Each user can have multiple preparation profiles.
Profile ID = username + category + company + role (slugified, deterministic)
"""
import json, os, re
from datetime import date
from pathlib import Path

DATA_DIR   = Path(__file__).parent / "data"
PROFILES_F = DATA_DIR / "profiles.json"
PROGRESS_F = DATA_DIR / "progress.json"


def _slugify(s: str) -> str:
    """Deterministically convert string to snake_case slug."""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def make_profile_id(username: str, category: str, company: str, role: str) -> str:
    return f"{_slugify(username)}__{_slugify(category)}__{_slugify(company)}__{_slugify(role)}"


def _load_profiles() -> dict:
    if PROFILES_F.exists():
        with open(PROFILES_F) as f:
            return json.load(f)
    return {}


def _save_profiles(profiles: dict):
    PROFILES_F.parent.mkdir(parents=True, exist_ok=True)
    with open(PROFILES_F, "w") as f:
        json.dump(profiles, f, indent=2)


def _load_progress() -> dict:
    if PROGRESS_F.exists():
        with open(PROGRESS_F) as f:
            return json.load(f)
    return {}


def _save_progress(progress: dict):
    PROGRESS_F.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_F, "w") as f:
        json.dump(progress, f, indent=2)


def list_profiles(username: str) -> list:
    """Return all profiles for a given user."""
    profiles = _load_profiles()
    return [p for p in profiles.values() if p["username"] == username]


def get_profile(profile_id: str) -> dict:
    profiles = _load_profiles()
    return profiles.get(profile_id)


def create_profile(
    username: str,
    category: str,
    company: str,
    role: str,
    sections: list,
) -> dict:
    """
    Create a new profile. Returns the created profile dict.
    Raises ValueError if profile already exists.
    """
    pid = make_profile_id(username, category, company, role)
    profiles = _load_profiles()

    if pid in profiles:
        raise ValueError(f"Profile already exists: {pid}")

    profile = {
        "profile_id":     pid,
        "username":       username,
        "category":       category,
        "company":        company,
        "role":           role,
        "sections":       sections,
        "created_at":     str(date.today()),
        "test_completed": False,
        "test_count":     0,      # increments each time test is submitted
        "scores": {
            "dsa_score":           0.0,
            "cs_score":            0.0,
            "system_design_score": 0.0,
            "level":               "beginner",
        },
        "readiness_score": 0.0,
        "test_history":   [],
    }

    profiles[pid] = profile
    _save_profiles(profiles)

    # Initialize empty progress
    progress = _load_progress()
    progress[pid] = {}
    _save_progress(progress)

    return profile


def update_scores(profile_id: str, scores: dict) -> dict:
    """Update profile scores after a test. Returns updated profile."""
    profiles = _load_profiles()
    if profile_id not in profiles:
        raise ValueError(f"Profile not found: {profile_id}")

    p = profiles[profile_id]
    p["scores"].update(scores)
    p["test_completed"] = True
    p.setdefault("test_count", 0)
    p["test_count"] += 1          # advance seed for next test attempt
    p["test_history"].append({
        "date":  str(date.today()),
        "scores": dict(scores),
        "attempt": p["test_count"],
    })

    profiles[profile_id] = p
    _save_profiles(profiles)
    return p


def update_readiness(profile_id: str, readiness_score: float) -> dict:
    profiles = _load_profiles()
    if profile_id not in profiles:
        raise ValueError(f"Profile not found: {profile_id}")
    profiles[profile_id]["readiness_score"] = readiness_score
    _save_profiles(profiles)
    return profiles[profile_id]


# ── Progress Management ────────────────────────────────────────

def get_progress(profile_id: str) -> dict:
    """Get all progress for a profile.
    Returns: { section: { topic_id: { item_idx: bool } } }
    """
    progress = _load_progress()
    return progress.get(profile_id, {})


def toggle_item(profile_id: str, section: str, topic_id: str, item_idx: int) -> dict:
    """Toggle a single learning item complete/incomplete. Returns updated progress."""
    progress = _load_progress()
    p = progress.setdefault(profile_id, {})
    s = p.setdefault(section, {})
    t = s.setdefault(topic_id, {})
    key = str(item_idx)
    t[key] = not t.get(key, False)
    _save_progress(progress)
    return t


def compute_completion(profile_id: str, learning_content: dict, sections: list) -> dict:
    """
    Compute completion percentages per section and overall.
    Returns: { "dsa": float, "cs": float, "system_design": float, "overall": float }
    """
    progress = get_progress(profile_id)

    section_key_map = {
        "DSA":              "DSA",
        "CS Fundamentals":  "CS Fundamentals",
        "System Design":    "System Design",
    }

    result = {}
    total_items = 0
    total_done  = 0

    for sec in sections:
        content_key = sec  # matches learning_content keys
        topics = learning_content.get(content_key, [])
        sec_total = sum(t["total"] for t in topics)
        sec_done  = 0

        sec_progress = progress.get(sec, {})
        for topic in topics:
            tid   = topic["id"]
            tprog = sec_progress.get(tid, {})
            sec_done += sum(1 for v in tprog.values() if v)

        pct = round(sec_done / sec_total * 100, 1) if sec_total else 0.0

        short_key = {
            "DSA": "dsa",
            "CS Fundamentals": "cs",
            "System Design": "system_design",
        }.get(content_key, content_key.lower())

        result[short_key] = pct
        total_items += sec_total
        total_done  += sec_done

    result["overall"] = round(total_done / total_items * 100, 1) if total_items else 0.0
    return result
