import random

# Define the card suits and values
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in suits for value in values]
        self.shuffle()

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.deal())

    def show_hand(self):
        for card in self.hand:
            print(card)

    def discard(self):
        while True:
            discard_list = input("Enter the numbers of the cards to discard, separated by commas (e.g. 1,3,4): ")
            try:
                discard_list = [int(num) for num in discard_list.split(",")]
                break
            except ValueError:
                print("Invalid input. Please enter the numbers of the cards to discard, separated by commas (e.g. 1,3,4).")
        for index in sorted(discard_list, reverse=True):
            self.hand.pop(index - 1)

def determine_winner(players):
    highest_score = 0
    winners = []
    for player in players:
        score, high_cards = check_hand(player.hand)
        if score > highest_score:
            highest_score = score
            winners = [player]
        elif score == highest_score:
            winners.append(player)
    print("The winner is:")
    for winner in winners:
        print(f"{winner.name} with {score_names[highest_score]}")
        print("Their hand:")
        winner.show_hand()

def check_hand(hand):
    values = [card.value for card in hand]
    suits = [card.suit for card in hand]

    # Check for flush
    if len(set(suits)) == 1:
        if set(values) == {'10', 'Jack', 'Queen', 'King', 'Ace'}:
            return 10, []
        else:
            return 6, sorted(values, reverse=True)

    # Check for straight
    if len(set(values)) == 5:
        values.sort(key=lambda x: values.index(x))
        if values == ['Ace', '2', '3', '4', '5']:
            return 5, []
        elif values == ['10', 'Jack', 'Queen', 'King', 'Ace']:
            return 9, []
        else:
            return 5, [values[-1]]

    # Check for pairs
    pairs = []
    for value in set(values):
        if values.count(value) == 2:
            pairs.append(value)
    if len(pairs) == 2:
        pairs.sort(reverse=True)
        return 8, pairs
    elif len(pairs) == 1:
        high_cards = [value for value in values if value != pairs[0]]
        high_cards.sort(reverse=True)
        return
