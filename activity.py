from typing import List
import random


def deal_cards() -> List[int]:
    """
    Returns a list of 5 integers representing the poker hand dealt to a player.
    Each integer corresponds to a card in a standard deck of 52 cards.
    """
    deck = list(range(52))
    random.shuffle(deck)
    return deck[:5]


def check_hand(hand: List[int]) -> str:
    """
    Returns a string representing the rank of the given poker hand.
    """
    ranks = "23456789TJQKA"
    suits = "CDHS"
    cards = [(ranks[i % 13], suits[i // 13]) for i in hand]
    cards.sort(reverse=True)
    flush = len(set(s for r, s in cards)) == 1
    straight = max(cards)[0] == min(cards)[0] + 4 and len(set(r for r, s in cards)) == 5
    pairs = [(r, sum(r == c[0] for c in cards)) for r in ranks]
    pairs.sort(key=lambda x: (-x[1], ranks.index(x[0])))
    hand_rank = [(1, cards)] if flush and straight else \
                [(2, [(r, s) for r, s in cards if r == x[0]]) + [(r, s) for r, s in cards if r != x[0]] for x in pairs]
    return hand_rank[0][0]


def determine_winner(hands: List[List[int]]) -> int:
    """
    Returns the index of the winning player given a list of poker hands.
    """
    best_hand = None
    winner = None
    for i, hand in enumerate(hands):
        rank = check_hand(hand)
        if not best_hand or rank < best_hand:
            best_hand = rank
            winner = i
    return winner
