import asyncio
from temporal.workflow import workflow_method, WorkflowClient, Workflow

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.hand = []
        self.chips = chips
        self.folded = False

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("Player does not have enough chips")
        self.chips -= amount
        return amount

    def __repr__(self):
        return self.name

class Deck:
    def __init__(self):
        self.cards = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for value in range(2, 15):
                card = Card(value, suit)
                self.cards.append(card)

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class PokerWorkflow:
    @workflow_method
    async def play_poker(cls, num_players, starting_chips):
        async def take_turn(player):
            if player.folded:
                return
            bet = await Workflow.await_input()
            while bet != 0 and bet < current_bet:
                bet = await Workflow.await_input()
            if bet == 0:
                player.folded = True
            else:
                player.bet(bet)
                current_bet = bet
            await asyncio.sleep(0)

        deck = Deck()
        deck.shuffle()

        players = []
        for i in range(num_players):
            players.append(Player(f"Player {i+1}", starting_chips))

        # Deal cards
        for i in range(5):
            for player in players:
                card = deck.deal()
                player.hand.append(card)

        # First round of betting
        current_bet = 0
        for player in players:
            if player.folded:
                continue
            bet = await asyncio.create_task(take_turn(player))
            if bet > current_bet:
                current_bet = bet

        # Discard and draw new cards
        for player in players:
            if player.folded:
                continue
            num_cards_to_discard = await Workflow.await_input()
            for i in range(num_cards_to_discard):
                card_index = await Workflow.await_input()
                player.hand.pop(card_index)
                new_card = deck.deal()
                player.hand.append(new_card)

        # Second round of betting
        for player in players:
            if player.folded:
                continue
            bet = await asyncio.create_task(take_turn(player))

        # Determine winner
        winner = None
        winning_score = 0
        for player in players:
            if player.folded:
                continue
            score, high_cards = check_hand(player.hand)
            if score > winning_score:
                winner = player
                winning_score = score
            elif score == winning_score:
                if high_cards[0].value > winner.hand[0].value:
                    winner = player
        return winner.name


def check_hand(hand):
    values = [card.value for card in hand]
    suits = [card.suit for card in hand]
    score = 0
    high_cards = []

    # Check for a straight flush
    straight_flush = False
    for suit in suits:
        if suits.count(suit) >= 5:
            suit_cards = [card for card in hand if card.suit == suit]
            for i in range(len(suit)):
            values = sorted([card.value for card in suit_cards])
            if values == [10, 11, 12, 13, 14]:
                score = 9
                high_cards = suit_cards
                straight_flush = True
                break
            for i in range(len(values) - 4):
                if values[i+4] == values[i] + 4:
                    score = 9
                    high_cards = suit_cards[i:i+5]
                    straight_flush = True
                    break
        if straight_flush:
            return score, high_cards

    # Check for four of a kind
    for value in set(values):
        if values.count(value) == 4:
            score = 8
            high_cards = [card for card in hand if card.value == value]
            high_cards.append([card for card in hand if card.value != value][0])
            return score, high_cards

    # Check for full house
    three_of_a_kind_value = None
    for value in set(values):
        if values.count(value) == 3:
            three_of_a_kind_value = value
            break
    if three_of_a_kind_value is not None:
        for value in set(values):
            if values.count(value) == 2 and value != three_of_a_kind_value:
                score = 7
                high_cards = [card for card in hand if card.value == three_of_a_kind_value]
                high_cards += [card for card in hand if card.value == value]
                return score, high_cards

    # Check for flush
    for suit in suits:
        if suits.count(suit) >= 5:
            score = 6
            suit_cards = [card for card in hand if card.suit == suit]
            high_cards = sorted(suit_cards, key=lambda x: x.value, reverse=True)[:5]
            return score, high_cards

    # Check for straight
    values = sorted(list(set(values)))
    if values == [2, 3, 4, 5, 14]:
        values = [1, 2, 3, 4, 5]
    for i in range(len(values) - 4):
        if values[i+4] == values[i] + 4:
            score = 5
            high_cards = [card for card in hand if card.value in values[i:i+5]]
            return score, high_cards

    # Check for three of a kind
    for value in set(values):
        if values.count(value) == 3:
            score = 4
            high_cards = [card for card in hand if card.value == value]
            high_cards += sorted([card for card in hand if card.value != value], key=lambda x: x.value, reverse=True)[:2]
            return score, high_cards

    # Check for two pair
    pairs = []
    for value in set(values):
        if values.count(value) == 2:
            pairs.append(value)
    if len(pairs) == 2:
        score = 3
        high_cards = [card for card in hand if card.value == pairs[0]]
        high_cards += [card for card in hand if card.value == pairs[1]]
        high_cards += [card for card in hand if card.value != pairs[0] and card.value != pairs[1]][0:1]
        return score, high_cards

    # Check for pair
    pair_value = None
    for value in set(values):
        if values.count(value) == 2:
            pair_value = value
            break
    if pair_value is not None:
        score = 2
        high_cards = [card for card in hand if card.value == pair_value]
        high_cards += sorted([card for card in hand if card.value != pair_value], key=lambda x: x.value, reverse=True)[:3]
        return score, high_cards

    # If none of the above, score by highest card
    score = 1
    high_cards = sorted(hand, key=lambda x: x.value, reverse=True)[:5]
    return score, high_cards

def determine_winner(players):
    scores = []
    for player in players:
        score, high_cards = check_hand(player.hand)
        scores.append((score, high_cards))
    max_score = max([score for score, high_cards in scores])
    winners = [players[i] for i in range(len(players)) if scores[i][0] == max_score]
    if len(winners) == 1:
        return winners[0].name
    else:
        # Handle ties by comparing high cards
        for i in range(5):
            max_card_value = max([high_cards[i].value for score, high_cards in scores if score == max_score])
            winners = [players[i] for i in range(len(players)) if scores[i][0] == max_score and high_cards[i].value == max_card_value]
            if len(winners) == 1:
                return winners[0].name
        return "Tie"

async def play_game():
    num_players = 2
    deck = Deck()
    deck.shuffle()
    players = []
    for i in range(num_players):
        name = input(f"Enter name for player {i+1}: ")
        players.append(Player(name))
    for i in range(5):
        for player in players:
            player.hand.append(deck.draw())
    for player in players:
        print(f"{player.name}'s hand: {player.hand}")
    winner = determine_winner(players)
    print(f"{winner} wins!")
