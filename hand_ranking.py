from typing import List, Tuple
from collections import Counter
from card import Card
from deck_utils import deal_cards
from game_state import GameState


def rank_hand(hand: List[Card]) -> Tuple[int, List[int]]:
    ranks = sorted([card.rank.value for card in hand], reverse=True)
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4 or (14 in ranks and 2 in ranks and 3 in ranks and 4 in ranks and 5 in ranks))

    if is_straight and is_flush:
        return 9, ranks if ranks[-1] != 2 else [5, 4, 3, 2, 1]  # Straight flush (ace-low straight flush)
    if 4 in rank_counts.values():
        return 8, [r for r in rank_counts if rank_counts[r] == 4] + [r for r in rank_counts if rank_counts[r] != 4]  # Four of a kind
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return 7, [r for r in rank_counts if rank_counts[r] == 3] + [r for r in rank_counts if rank_counts[r] != 3]  # Full house
    if is_flush:
        return 6, ranks  # Flush
    if is_straight:
        return 5, ranks if ranks[-1] != 2 else [5, 4, 3, 2, 1]  # Straight (ace-low straight)
    if 3 in rank_counts.values():
        return 4, [r for r in rank_counts if rank_counts[r] == 3] + sorted([r for r in rank_counts if rank_counts[r] != 3], reverse=True)  # Three of a kind
    if 2 in rank_counts.values():
        pairs = [r for r in rank_counts if rank_counts[r] == 2]
        if len(pairs) == 2:
            return 3, sorted(pairs, reverse=True) + [r for r in rank_counts if rank_counts[r] == 1]  # Two pairs
        else:
            return 2, pairs + sorted([r for r in rank_counts if rank_counts[r] == 1], reverse=True)  # One pair
    return 1, ranks  # High card


async def draw_cards(game_state: GameState, player_idx: int, discard_indices: List[int]) -> None:
    player_hand = game_state.players[player_idx]
    for index in sorted(discard_indices, reverse=True):
        del player_hand[index]
    new_cards = await deal_cards(game_state, len(discard_indices))
    game_state.players[player_idx] = player_hand + new_cards
