from dataclasses import dataclass
from typing import List
from card import Card


@dataclass
class GameState:
    deck: List[Card]
    players: List[List[Card]]
