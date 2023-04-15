from dataclasses import dataclass
from typing import List

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from card import Card


@dataclass
class GameState:
    deck: List[Card]
    players: List[List[Card]]
