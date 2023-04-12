from enum import Enum, IntEnum
from dataclasses import dataclass


class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

    @classmethod
    def from_str(cls, suit_str: str):
        for suit in cls:
            if suit.value == suit_str:
                return suit
        raise ValueError(f"Invalid suit string: {suit_str}")


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

    @property
    def str_value(self):
        if self.value < 11:
            return str(self.value)
        return self.name.capitalize()

    @classmethod
    def from_str(cls, rank_str: str) -> "Rank":
        if rank_str.isdigit():
            value = int(rank_str)
            if 2 <= value <= 10:
                return cls(value)
        elif rank_str in {"J", "Q", "K", "A"}:
            face_cards = {"J": 11, "Q": 12, "K": 13, "A": 14}
            return cls(face_cards[rank_str])
        else:
            for rank in cls:
                if rank.name.lower() == rank_str.lower():
                    return rank

        raise ValueError(f"Invalid rank string: {rank_str}")


@dataclass
class Card:
    suit: Suit
    rank: Rank

    def __str__(self):
        return f"{self.rank.name.capitalize() if self.rank.value < 11 else self.rank.name[0]}{self.suit.value}"

    @classmethod
    def from_str(cls, card_str: str):
        rank_str, suit_str = card_str[:-1], card_str[-1]
        rank = Rank.from_str(rank_str)
        suit = Suit.from_str(suit_str)
        return cls(rank, suit)
