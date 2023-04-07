import asyncio
import random
from collections import Counter
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import List, Tuple

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


@dataclass
class Card:
    suit: Suit
    rank: Rank

    def __str__(self):
        return f"{self.rank.name.capitalize() if self.rank.value < 11 else self.rank.name[0]}{self.suit.value}"


@dataclass
class GameState:
    deck: List[Card]
    players: List[List[Card]]


@activity.defn
async def shuffle_deck(deck: List[Card]) -> List[Card]:
    await asyncio.sleep(0.1)
    random.shuffle(deck)
    return deck


async def deal_cards(game_state: GameState, num_cards: int) -> List[Card]:
    new_cards = []
    for _ in range(num_cards):
        card = game_state.deck.pop()
        new_cards.append(card)
    return new_cards


def create_deck() -> List[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]


def rank_hand(hand: List[Card]) -> Tuple[int, List[int]]:
    ranks = sorted([card.rank.value for card in hand], reverse=True)
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4

    if is_straight and is_flush:
        return (9, ranks) if ranks[-1] != 2 else (9, [5, 4, 3, 2, 1])  # Straight flush (ace-low straight flush)
    if 4 in rank_counts.values():
        return (8, [r for r in rank_counts if rank_counts[r] == 4] + [r for r in rank_counts if
                                                                      rank_counts[r] != 4])  # Four of a kind
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return (7, [r for r in rank_counts if rank_counts[r] == 3] + [r for r in rank_counts if
                                                                      rank_counts[r] != 3])  # Full house
    if is_flush:
        return (6, ranks)  # Flush
    if is_straight:
        return (5, ranks) if ranks[-1] != 2 else (5, [5, 4, 3, 2, 1])  # Straight (ace-low straight)
    if 3 in rank_counts.values():
        return (4, [r for r in rank_counts if rank_counts[r] == 3] + sorted(
            [r for r in rank_counts if rank_counts[r] != 3], reverse=True))  # Three of a kind
    if 2 in rank_counts.values():
        pairs = [r for r in rank_counts if rank_counts[r] == 2]
        if len(pairs) == 2:
            return (3, sorted(pairs, reverse=True) + [r for r in rank_counts if rank_counts[r] == 1])  # Two pairs
        else:
            return (2, pairs + sorted([r for r in rank_counts if rank_counts[r] == 1], reverse=True))  # One pair
    return (1, ranks)  # High card

async def draw_cards(game_state: GameState, player_idx: int, discard_indices: List[int]) -> None:
    player_hand = game_state.players[player_idx]
    for index in sorted(discard_indices, reverse=True):
        del player_hand[index]
    new_cards = await deal_cards(game_state, len(discard_indices))
    game_state.players[player_idx] = player_hand + new_cards


@workflow.defn
class PlayGame:
    @workflow.run
    async def run(self) -> None:
        num_players = int(input("Enter the number of players (2-4): "))
        if num_players < 2 or num_players > 4:
            print("Invalid number of players. Please enter a number between 2 and 4.")
            return

        deck = await shuffle_deck(create_deck())
        game_state = GameState(deck=deck, players=[[] for _ in range(num_players)])

        for i in range(num_players):
            game_state.players[i] = await deal_cards(game_state, 5)

        for i, player_hand in enumerate(game_state.players):
            print(f"Player {i + 1}'s hand: {', '.join(str(card) for card in player_hand)}")

        for i in range(num_players):
            discard_indices = input(
                f"Player {i + 1}, enter the indices of the cards to discard (0-4, separated by spaces): ")
            discard_indices = [int(index) for index in discard_indices.split()]
            await draw_cards(game_state, i, discard_indices)

        for i, player_hand in enumerate(game_state.players):
            print(f"Player {i + 1}'s final hand: {', '.join(str(card) for card in player_hand)}")

        hand_ranks = [rank_hand(hand) for hand in game_state.players]
        max_rank = max(hand_ranks)
        winner_idx = hand_ranks.index(max_rank)
        print(
            f"Player {winner_idx + 1} wins with a {', '.join(str(card) for card in game_state.players[winner_idx])}!")


async def main():
    # Start client
    client = await Client.connect("localhost:7233")
    async with Worker(
            client,
            task_queue="poker-activity-task-queue",
            workflows=[PlayGame()],
            activities=[shuffle_deck],
    ):
        result = await client.execute_workflow(
            PlayGame.run,
            id="poker-workflow-id",
            task_queue="poker-task-queue",
        )


if __name__ == "__main__":
    asyncio.run(main())
