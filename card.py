from enum import Enum, IntEnum
from dataclasses import dataclass


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
