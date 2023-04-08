import asyncio
import random
from typing import List
from temporalio import activity
from card import Card, Suit, Rank
from game_state import GameState


def create_deck() -> List[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]


@activity.defn
async def shuffle_deck(deck: List[Card], seed: int) -> List[Card]:
    await asyncio.sleep(0.1)
    return await shuffle_deck_sync(deck, seed)


async def shuffle_deck_sync(deck: List[Card], seed: int) -> List[Card]:
    await asyncio.sleep(0)
    rng = random.Random(seed)
    shuffled_deck = []

    while deck:
        idx = rng.randint(0, len(deck) - 1)
        card = deck.pop(idx)
        shuffled_deck.append(card)

    return shuffled_deck


async def deal_cards(game_state: GameState, num_cards: int) -> List[Card]:
    new_cards = []
    for _ in range(num_cards):
        card = game_state.deck.pop()
        new_cards.append(card)
    return new_cards
