import random
from temporal.activity_method import activity_method

# Define the activity interface
class PokerActivity:
    @activity_method()
    async def evaluate_hand(cls, hand: list) -> int:
        # Code for evaluating a hand goes here
        pass

# Define the function for evaluating a hand
async def evaluate_hand(hand: list) -> int:
    # Code for evaluating a hand goes here
    pass

# Define the function for drawing cards
async def draw_cards(num_cards: int) -> list:
    # Code for drawing cards goes here
    pass
