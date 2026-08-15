from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.database.connection import get_db
from app.models.interaction import Interaction
from app.models.user import User


router = APIRouter(
    prefix="/interaction",
    tags=["Interactions"]
)


# ---------------------------------------------------------
# Request schema
# ---------------------------------------------------------

class InteractionCreate(BaseModel):

    user_id: int
    content_id: int

    clicked: bool = False
    liked: bool = False
    saved: bool = False
    shared: bool = False

    watch_time: float = 0
    read_time: float = 0
    scroll_depth: float = 0


# ---------------------------------------------------------
# CREATE INTERACTION
# ---------------------------------------------------------

@router.post("")
def create_interaction(
    request: InteractionCreate,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == request.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    interaction = Interaction(
        user_id=request.user_id,
        content_id=request.content_id,
        clicked=request.clicked,
        liked=request.liked,
        saved=request.saved,
        shared=request.shared,
        watch_time=request.watch_time,
        read_time=request.read_time,
        scroll_depth=request.scroll_depth
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return {
        "message": "Interaction created",
        "interaction_id": interaction.id
    }


# ---------------------------------------------------------
# UPDATE INTERACTION
# ---------------------------------------------------------

@router.put("/{interaction_id}")
def update_interaction(
    interaction_id: int,
    watch_time: float = 0,
    read_time: float = 0,
    scroll_depth: float = 0,
    liked: bool = False,
    saved: bool = False,
    shared: bool = False,
    db: Session = Depends(get_db)
):

    interaction = (
        db.query(Interaction)
        .filter(
            Interaction.id == interaction_id
        )
        .first()
    )

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Interaction not found"
        )

    interaction.watch_time = watch_time
    interaction.read_time = read_time
    interaction.scroll_depth = scroll_depth
    interaction.liked = liked
    interaction.saved = saved
    interaction.shared = shared

    db.commit()
    db.refresh(interaction)

    return {
        "message": "Interaction updated",
        "interaction_id": interaction.id
    }