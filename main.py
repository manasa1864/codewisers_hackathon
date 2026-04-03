"""
main.py — CareerForge API
Deterministic Career Intelligence Platform

Endpoints:
  POST /signup, /login, /logout            — Auth
  GET  /profiles                           — List user profiles
  POST /profiles                           — Create new profile
  GET  /profiles/{profile_id}              — Get single profile
  GET  /test/{profile_id}/questions        — Get test questions (deterministic)
  POST /test/{profile_id}/submit           — Submit test answers
  GET  /dashboard/{profile_id}             — Get full dashboard data
  POST /progress/{profile_id}/toggle       — Toggle topic item
  GET  /readiness/{profile_id}             — Full readiness + gap analysis
  GET  /company-map                        — Get company/role hierarchy
"""

import json, hashlib, secrets
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

import profiles as prof_mgr
import questions as q_engine
import readiness as r_engine
import gap_detection
import decision as decision_engine
import explainability

BASE_DIR    = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
USERS_F     = DATA_DIR / "users.json"
CO_MAP_F    = DATA_DIR / "company_map.json"
LC_F        = DATA_DIR / "learning_content.json"

app = FastAPI(title="CareerForge — Career Intelligence Platform", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

security       = HTTPBearer(auto_error=False)
active_sessions: dict[str, str] = {}


# ─── Helpers ──────────────────────────────────────────────────────

def _load_users() -> dict:
    return json.loads(USERS_F.read_text()) if USERS_F.exists() else {}

def _save_users(users: dict):
    USERS_F.parent.mkdir(parents=True, exist_ok=True)
    USERS_F.write_text(json.dumps(users, indent=2))

def _hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def _load_company_map() -> dict:
    return json.loads(CO_MAP_F.read_text())

def _load_learning_content() -> dict:
    return json.loads(LC_F.read_text())


def get_current_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not creds:
        raise HTTPException(401, "Authentication required.")
    username = active_sessions.get(creds.credentials)
    if not username:
        raise HTTPException(401, "Invalid or expired session token.")
    return username


# ─── AUTH ─────────────────────────────────────────────────────────

class AuthReq(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(req: AuthReq):
    users = _load_users()
    if req.username in users:
        raise HTTPException(400, "Username already exists.")
    users[req.username] = _hash_pw(req.password)
    _save_users(users)
    return {"message": "Account created.", "username": req.username}

@app.post("/login")
def login(req: AuthReq):
    users = _load_users()
    if users.get(req.username) != _hash_pw(req.password):
        raise HTTPException(401, "Invalid credentials.")
    token = secrets.token_hex(32)
    active_sessions[token] = req.username
    return {"token": token, "username": req.username}

@app.post("/logout")
def logout(creds: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if creds and creds.credentials in active_sessions:
        del active_sessions[creds.credentials]
    return {"message": "Logged out."}


# ─── COMPANY MAP ──────────────────────────────────────────────────

@app.get("/company-map")
def get_company_map():
    return _load_company_map()


# ─── PROFILES ─────────────────────────────────────────────────────

class CreateProfileReq(BaseModel):
    category: str
    company:  str
    role:     str

@app.get("/profiles")
def list_profiles(username: str = Depends(get_current_user)):
    return {"profiles": prof_mgr.list_profiles(username)}

@app.post("/profiles")
def create_profile(req: CreateProfileReq, username: str = Depends(get_current_user)):
    co_map   = _load_company_map()
    category = req.category
    company  = req.company

    if category not in co_map:
        raise HTTPException(400, f"Unknown category: {category}")
    if company not in co_map[category]:
        raise HTTPException(400, f"Unknown company: {company} in {category}")

    co_info  = co_map[category][company]
    sections = co_info["sections"]

    try:
        profile = prof_mgr.create_profile(
            username=username,
            category=category,
            company=company,
            role=req.role,
            sections=sections,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"profile": profile}

@app.get("/profiles/{profile_id}")
def get_profile(profile_id: str, username: str = Depends(get_current_user)):
    p = prof_mgr.get_profile(profile_id)
    if not p or p["username"] != username:
        raise HTTPException(404, "Profile not found.")
    return {"profile": p}


# ─── TEST ─────────────────────────────────────────────────────────

@app.get("/test/{profile_id}/questions")
def get_test_questions(profile_id: str, round: int = 0, username: str = Depends(get_current_user)):
    p = prof_mgr.get_profile(profile_id)
    if not p or p["username"] != username:
        raise HTTPException(404, "Profile not found.")

    co_map   = _load_company_map()
    category = p["category"]
    company  = p["company"]
    co_info  = co_map.get(category, {}).get(company, {})
    importance = co_info.get("importance", {"dsa":"medium","cs":"medium","system_design":"medium"})

    questions_by_section = q_engine.select_questions_for_profile(
        profile_id=profile_id,
        sections=p["sections"],
        importance_map=importance,
        test_round=round,
    )

    # Strip correct answers before sending to client
    sanitized = {}
    for sec, qs in questions_by_section.items():
        sanitized[sec] = [
            {k: v for k, v in q.items() if k != "correct_answer"}
            for q in qs
        ]

    return {
        "profile_id": profile_id,
        "sections":   list(sanitized.keys()),
        "questions":  sanitized,
        "total":      sum(len(v) for v in sanitized.values()),
        "round":      round,
    }


class SubmitTestReq(BaseModel):
    answers:    dict   # { str(question_id): selected_answer }
    test_round: int = 0

@app.post("/test/{profile_id}/submit")
def submit_test(profile_id: str, req: SubmitTestReq, username: str = Depends(get_current_user)):
    p = prof_mgr.get_profile(profile_id)
    if not p or p["username"] != username:
        raise HTTPException(404, "Profile not found.")

    co_map   = _load_company_map()
    category = p["category"]
    company  = p["company"]
    co_info  = co_map.get(category, {}).get(company, {})
    importance = co_info.get("importance", {})

    # Re-select same questions using same round as GET (same seed = same questions)
    questions_by_section = q_engine.select_questions_for_profile(
        profile_id=profile_id,
        sections=p["sections"],
        importance_map=importance,
        test_round=req.test_round,
    )

    result = q_engine.score_answers(questions_by_section, req.answers)

    # Update profile scores
    scores = {
        "dsa_score":           result["dsa_score"],
        "cs_score":            result["cs_score"],
        "system_design_score": result["system_design_score"],
        "level":               result["level"],
    }
    updated_profile = prof_mgr.update_scores(profile_id, scores)

    # Adaptive learning params
    adaptive = {}
    for sec in p["sections"]:
        key = {"DSA":"dsa_score","CS Fundamentals":"cs_score","System Design":"system_design_score"}.get(sec,"dsa_score")
        adaptive[sec] = q_engine.get_adaptive_difficulty(result["section_scores"].get(sec, 0))

    return {
        "result":   result,
        "profile":  updated_profile,
        "adaptive": adaptive,
    }


# ─── DASHBOARD ────────────────────────────────────────────────────

@app.get("/dashboard/{profile_id}")
def get_dashboard(profile_id: str, username: str = Depends(get_current_user)):
    p = prof_mgr.get_profile(profile_id)
    if not p or p["username"] != username:
        raise HTTPException(404, "Profile not found.")

    lc      = _load_learning_content()
    progress = prof_mgr.get_progress(profile_id)
    completion = prof_mgr.compute_completion(profile_id, lc, p["sections"])

    co_map   = _load_company_map()
    category = p["category"]
    company  = p["company"]
    co_info  = co_map.get(category, {}).get(company, {})
    importance = co_info.get("importance", {})

    # Readiness score
    readiness = r_engine.compute_readiness_score(p["scores"], completion, p["sections"])
    prof_mgr.update_readiness(profile_id, readiness)

    # Targets
    targets = r_engine.compute_target_thresholds(importance)

    # Build section data
    sections_data = {}
    for sec in p["sections"]:
        topics = lc.get(sec, [])
        sec_progress = progress.get(sec, {})
        enriched_topics = []
        for topic in topics:
            tid   = topic["id"]
            tprog = sec_progress.get(tid, {})
            done  = sum(1 for v in tprog.values() if v)
            total = topic["total"]
            problems_with_status = []
            for idx, prob in enumerate(topic.get("problems", [])):
                problems_with_status.append({
                    **prob,
                    "done": tprog.get(str(idx), False),
                    "idx":  idx,
                })
            enriched_topics.append({
                **topic,
                "done":     done,
                "progress": round(done / total * 100, 1) if total else 0.0,
                "problems": problems_with_status,
            })
        sections_data[sec] = enriched_topics

    return {
        "profile":     p,
        "completion":  completion,
        "readiness":   readiness,
        "targets":     targets,
        "importance":  importance,
        "sections":    sections_data,
        "scores":      p["scores"],
    }


# ─── PROGRESS ─────────────────────────────────────────────────────

class ToggleReq(BaseModel):
    section:  str
    topic_id: str
    item_idx: int

@app.post("/progress/{profile_id}/toggle")
def toggle_progress(profile_id: str, req: ToggleReq, username: str = Depends(get_current_user)):
    p = prof_mgr.get_profile(profile_id)
    if not p or p["username"] != username:
        raise HTTPException(404, "Profile not found.")

    updated = prof_mgr.toggle_item(profile_id, req.section, req.topic_id, req.item_idx)

    lc         = _load_learning_content()
    completion = prof_mgr.compute_completion(profile_id, lc, p["sections"])

    # Update readiness with new completion
    readiness = r_engine.compute_readiness_score(p["scores"], completion, p["sections"])
    prof_mgr.update_readiness(profile_id, readiness)

    return {"updated": updated, "completion": completion, "readiness": readiness}


# ─── READINESS / ANALYSIS ─────────────────────────────────────────

@app.get("/readiness/{profile_id}")
def get_readiness(profile_id: str, username: str = Depends(get_current_user)):
    p = prof_mgr.get_profile(profile_id)
    if not p or p["username"] != username:
        raise HTTPException(404, "Profile not found.")

    if not p["test_completed"]:
        raise HTTPException(400, "Complete the initial test first.")

    lc         = _load_learning_content()
    co_map     = _load_company_map()
    category   = p["category"]
    company    = p["company"]
    co_info    = co_map.get(category, {}).get(company, {})
    importance = co_info.get("importance", {})

    completion = prof_mgr.compute_completion(profile_id, lc, p["sections"])
    scores     = p["scores"]
    targets    = r_engine.compute_target_thresholds(importance)
    readiness  = r_engine.compute_readiness_score(scores, completion, p["sections"])
    level_info = r_engine.get_readiness_level(readiness)
    explanation = r_engine.generate_readiness_explanation(readiness, scores, targets, completion)

    # Build gap detection inputs (no calibration)
    threshold_config = r_engine.build_threshold_config_for_gap_detection(company, importance, targets)
    user_data        = r_engine.build_user_data_for_gap_detection(company, p["role"], scores, completion)
    user_data["consistency"] = {"days_active_last_14": 14}  # removed from UI; suppress gap

    try:
        gaps = gap_detection.run_gap_detection(user_data, threshold_config)
    except Exception:
        gaps = []

    # Decision engine
    eval_summary = {
        "final_score": readiness,
        "scores": {
            "dsa":           scores.get("dsa_score", 0),
            "system_design": scores.get("system_design_score", 0),
            "cs":            scores.get("cs_score", 0),
        },
        "weights": {"dsa": 0.4, "system_design": 0.3, "cs": 0.3},
    }
    importance_profile = {
        "dsa":             {"high":0.9,"medium":0.6,"low":0.3,"none":0.1}.get(importance.get("dsa","medium"),0.6),
        "system_design":   {"high":0.9,"medium":0.6,"low":0.3,"none":0.1}.get(importance.get("system_design","medium"),0.6),
        "cs_fundamentals": {"high":0.9,"medium":0.6,"low":0.3,"none":0.1}.get(importance.get("cs","medium"),0.6),
        "math": 0.3, "hr": 0.2,
    }

    try:
        decision_result = decision_engine.run_decision_engine(
            gaps, user_data, eval_summary, importance_profile
        )
    except Exception:
        decision_result = {"action_plan": {"high_priority":[],"medium_priority":[],"low_priority":[]}, "decisions":[]}

    try:
        explanations = explainability.generate_full_explanation(
            evaluation_output={"scores":eval_summary["scores"],"weights":eval_summary["weights"],"final_score":readiness},
            gaps_list=gaps,
            decisions_output=decision_result,
        )
    except Exception:
        explanations = {"summary": explanation}

    return {
        "readiness_score": readiness,
        "level":           level_info,
        "explanation":     explanation,
        "targets":         targets,
        "scores":          scores,
        "completion":      completion,
        "gaps":            gaps,
        "action_plan":     decision_result["action_plan"],
        "decisions":       decision_result["decisions"],
        "explanations":    explanations,
    }


# ─── HEALTH ───────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "system": "CareerForge v2.0"}


# ─── FRONTEND ─────────────────────────────────────────────────────

frontend_dir = BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(str(frontend_dir / "index.html"))
