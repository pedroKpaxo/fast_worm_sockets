from pydantic import BaseModel


class InitEvent(BaseModel):
    type: str = "init"
    game: str = None
    player: str = None


class BetEvent(BaseModel):
    type: str = "bet"
    bet_number: int
    bet_amount: int
    player_name: str = None


class ErrorEvent(BaseModel):
    type: str = "error"
    message: str
