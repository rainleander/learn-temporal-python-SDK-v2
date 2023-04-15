import random
from typing import List

from temporalio import workflow, activity

with workflow.unsafe.imports_passed_through():
    from card import Card, Suit, Rank
    from game_state import GameState


def create_deck() -> List[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]


@activity.defn
async def shuffle_deck(deck: List[Card], seed: int) -> List[Card]:
    rng = random.Random(seed)
    rng.shuffle(deck)  # Using random.shuffle with the provided seed
    return deck


async def deal_cards(game_state: GameState, num_cards: int) -> List[Card]:
    new_cards = []
    for _ in range(num_cards):
        card = game_state.deck.pop()
        new_cards.append(card)
    return new_cards
