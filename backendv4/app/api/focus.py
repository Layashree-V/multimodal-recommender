import json
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.focus_session import FocusSession
from app.models.content import Content


router = APIRouter(prefix="/focus", tags=["Focus Sessions"])


class FocusSessionStart(BaseModel):
    user_id: int
    duration_minutes: float = Field(default=20, ge=1, le=240)
    goal: str = Field(default="General learning", max_length=500)
    content_ids: List[int] = Field(default_factory=list)


class FocusSessionFinish(BaseModel):
    elapsed_seconds: float = Field(default=0, ge=0)
    goal: Optional[str] = Field(default=None, max_length=500)
    content_ids: Optional[List[int]] = None


def _content_payload(db: Session, content_ids: List[int]):
    if not content_ids:
        return []
    rows = db.query(Content).filter(Content.id.in_(content_ids)).all()
    by_id = {row.id: row for row in rows}
    result = []
    for cid in content_ids:
        row = by_id.get(cid)
        if row:
            result.append({
                "id": row.id,
                "title": row.title,
                "category": row.category,
                "content_type": row.content_type,
                "source": row.source,
                "url": row.url,
                "thumbnail": row.thumbnail,
            })
    return result


def _payload(db: Session, session: FocusSession):
    try:
        ids = json.loads(session.content_ids or "[]")
    except (TypeError, ValueError):
        ids = []

    return {
        "id": session.id,
        "user_id": session.user_id,
        "goal": session.goal,
        "duration_minutes": session.duration_minutes,
        "elapsed_seconds": session.elapsed_seconds,
        "status": session.status,
        "content_ids": ids,
        "content": _content_payload(db, ids),
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
    }


@router.post("/sessions")
def start_focus_session(payload: FocusSessionStart, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Close stale active sessions from this user so the history cannot
    # accumulate multiple unfinished sessions.
    active = db.query(FocusSession).filter(
        FocusSession.user_id == payload.user_id,
        FocusSession.status == "active"
    ).all()
    for old in active:
        old.status = "abandoned"
        old.completed_at = datetime.now(timezone.utc)

    content_ids = list(dict.fromkeys(int(x) for x in payload.content_ids if int(x) > 0))

    session = FocusSession(
        user_id=payload.user_id,
        goal=(payload.goal or "General learning").strip() or "General learning",
        duration_minutes=payload.duration_minutes,
        elapsed_seconds=0,
        status="active",
        content_ids=json.dumps(content_ids),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return _payload(db, session)


@router.post("/sessions/{session_id}/complete")
def complete_focus_session(
    session_id: int,
    payload: FocusSessionFinish,
    db: Session = Depends(get_db),
):
    session = db.query(FocusSession).filter(FocusSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Focus session not found")

    if session.status == "completed":
        return _payload(db, session)

    if session.status == "abandoned":
        raise HTTPException(status_code=409, detail="Focus session was already abandoned")

    session.elapsed_seconds = min(
        float(payload.elapsed_seconds or 0),
        float(session.duration_minutes or 0) * 60
    )

    if payload.goal is not None:
        session.goal = payload.goal.strip() or session.goal

    if payload.content_ids is not None:
        ids = list(dict.fromkeys(int(x) for x in payload.content_ids if int(x) > 0))
        session.content_ids = json.dumps(ids)

    session.status = "completed"
    session.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(session)
    return _payload(db, session)


@router.post("/sessions/{session_id}/abandon")
def abandon_focus_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(FocusSession).filter(FocusSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Focus session not found")

    if session.status == "completed":
        return _payload(db, session)

    session.status = "abandoned"
    session.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    return _payload(db, session)


@router.get("/sessions/{user_id}")
def get_focus_sessions(
    user_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    limit = max(1, min(limit, 100))
    sessions = (
        db.query(FocusSession)
        .filter(
            FocusSession.user_id == user_id,
            FocusSession.status == "completed",
        )
        .order_by(FocusSession.started_at.desc())
        .limit(limit)
        .all()
    )
    return {"sessions": [_payload(db, item) for item in sessions]}


@router.get("/stats/{user_id}")
def get_focus_stats(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sessions = db.query(FocusSession).filter(
        FocusSession.user_id == user_id,
        FocusSession.status == "completed",
    ).all()

    total_seconds = sum(float(item.elapsed_seconds or 0) for item in sessions)
    return {
        "user_id": user_id,
        "completed_sessions": len(sessions),
        "total_focus_seconds": total_seconds,
        "total_focus_minutes": round(total_seconds / 60, 1),
    }
