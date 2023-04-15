from dataclasses import dataclass
from typing import List

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from card import Card
    from hand_ranking import rank_hand


@dataclass
class HandRankingInput:
    hand: List[str]


@workflow.defn
class HandRankingWorkflow:
    @workflow.run
    async def run(self, input: HandRankingInput) -> str:
        hand = [Card.from_str(card_str) for card_str in input.hand]
        return str(rank_hand(hand))
