from pydantic import BaseModel
from typing import Optional


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None