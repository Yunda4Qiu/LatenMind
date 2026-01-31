from pydantic import BaseModel
from typing import List


class ActionRequest(BaseModel):
    game_id: str
    action: int  # 0,1,2 or 3(HOLD)


class GameStateResponse(BaseModel):
    game_id: str
    round: int
    symbols: List[int]
    score: float
    stability_index: float
    message: str
