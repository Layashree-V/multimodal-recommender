from pydantic import BaseModel

class InteractionCreate(BaseModel):
    user_id: int
    content_id: int

    clicked: bool = False
    liked: bool = False
    saved: bool = False
    shared: bool = False

    watch_time: int = 0
    read_time: int = 0
    scroll_depth: float = 0