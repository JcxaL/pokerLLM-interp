from pydantic import BaseModel
from typing import List, Optional

class Card(BaseModel):
    rank: str
    suit: str

class Action(BaseModel):
    position: str
    action: str
    bet_size: Optional[float] = None

class ActionOption(BaseModel):
    action: str
    frequency: float

class PokerHand(BaseModel):
    actions_until_now: List[Action]
    board_cards: List[Card]
    player_hand: List[Card]
    current_user_position: str
    current_action_options: List[ActionOption]

class PokerHandResponse(BaseModel):
    success: bool
    data: Optional[PokerHand] = None
    error: Optional[str] = None 