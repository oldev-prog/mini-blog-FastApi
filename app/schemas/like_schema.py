from pydantic import BaseModel, Field
from typing import List

class LikeDTO(BaseModel):
    user_id: int
    post_id: int

