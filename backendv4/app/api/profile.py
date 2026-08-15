from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.interaction import Interaction
from app.models.content import Content
from app.models.focus_session import FocusSession


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


class ProfileUpdate(BaseModel):
    name: str


def content_payload(article: Content) -> dict:
    return {
        "id": article.id,
        "title": article.title,
        "category": article.category,
        "source": article.source,
        "url": article.url,
        "description": article.description,
        "content_text": article.content_text,
        "content_type": article.content_type,
        "thumbnail": article.thumbnail,
    }


@router.get("/{user_id}")
def get_profile(
    user_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------
    # Find user
    # -----------------------------------------

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # -----------------------------------------
    # Get all interactions
    # -----------------------------------------

    interactions = (
        db.query(Interaction)
        .filter(
            Interaction.user_id == user_id
        )
        .order_by(
            Interaction.interaction_time.desc()
        )
        .all()
    )

    # -----------------------------------------
    # Saved content IDs
    # -----------------------------------------

    saved_ids = list(
        dict.fromkeys(
            i.content_id
            for i in interactions
            if i.saved
        )
    )

    # -----------------------------------------
    # Liked content IDs
    # -----------------------------------------

    liked_ids = list(
        dict.fromkeys(
            i.content_id
            for i in interactions
            if i.liked
        )
    )

    # -----------------------------------------
    # Viewed content
    # -----------------------------------------

    viewed = [
        i
        for i in interactions
        if (
            i.clicked
            or (i.read_time or 0) > 0
            or (i.watch_time or 0) > 0
        )
    ]

    viewed_ids = list(
        dict.fromkeys(
            i.content_id
            for i in viewed
        )
    )

    # -----------------------------------------
    # Build history
    # -----------------------------------------

    history = []

    for content_id in viewed_ids[:50]:

        article = (
            db.query(Content)
            .filter(Content.id == content_id)
            .first()
        )

        if article:
            history.append(
                content_payload(article)
            )

    # -----------------------------------------
    # Build saved list
    # -----------------------------------------

    saved = []

    for content_id in saved_ids[:100]:

        article = (
            db.query(Content)
            .filter(Content.id == content_id)
            .first()
        )

        if article:
            saved.append(
                content_payload(article)
            )

    # -----------------------------------------
    # Calculate interests
    # -----------------------------------------

    category_counter = Counter()

    for interaction in interactions:

        if not (
            interaction.clicked
            or interaction.liked
            or interaction.saved
        ):
            continue

        category = (
            db.query(Content.category)
            .filter(
                Content.id == interaction.content_id
            )
            .scalar()
        )

        category_counter[
            category or "General"
        ] += 1

    top_interests = [
        {
            "category": category,
            "count": count
        }
        for category, count
        in category_counter.most_common(5)
    ]

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    total_read_time = sum(
        i.read_time or 0
        for i in interactions
    )

    total_watch_time = sum(
        i.watch_time or 0
        for i in interactions
    )

    shared_count = sum(
        1
        for i in interactions
        if i.shared
    )

    liked_count = sum(
        1
        for i in interactions
        if i.liked
    )

    saved_count = sum(
        1
        for i in interactions
        if i.saved
    )

    # -----------------------------------------
    # Focus sessions
    # -----------------------------------------

    focus_sessions = (
        db.query(FocusSession)
        .filter(
            FocusSession.user_id == user_id,
            FocusSession.status == "completed",
        )
        .count()
    )

    # -----------------------------------------
    # Return profile
    # -----------------------------------------

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,

        "saved_count": saved_count,
        "viewed_count": len(viewed_ids),
        "liked_count": liked_count,
        "shared_count": shared_count,

        "focus_sessions": focus_sessions,

        "total_read_time": total_read_time,
        "total_watch_time": total_watch_time,

        "liked_ids": liked_ids,
        "saved_ids": saved_ids,

        "history": history,
        "saved": saved,

        "top_interests": top_interests,
    }


@router.put("/{user_id}")
def update_profile(
    user_id: int,
    payload: ProfileUpdate,
    db: Session = Depends(get_db)
):

    name = payload.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = name

    db.commit()
    db.refresh(user)

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }