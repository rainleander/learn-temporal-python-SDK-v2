import random
from typing import List

from temporalio import workflow, activity

with workflow.unsafe.imports_passed_through():
    from card import Card, Suit, Rank
    from game_state import GameState


@activity.defn
async def create_and_shuffle_deck(seed: int) -> List[Card]:
    deck = [Card(suit, rank) for suit in Suit for rank in Rank]

    rng = random.Random(seed)
    rng.shuffle(deck)  # Using random.shuffle with the provided seed

    return deck


async def deal_cards(game_state: GameState, num_cards: int) -> List[Card]:
    new_cards = []
    for _ in range(num_cards):
        card = game_state.deck.pop()
        new_cards.append(card)
    return new_cards
