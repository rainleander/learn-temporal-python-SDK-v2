from temporalio import workflow
from game_state import GameState
from deck_utils import create_deck, shuffle_deck, deal_cards
from hand_ranking import rank_hand, draw_cards


@workflow.defn
class PlayGame:
    @workflow.run
    async def run(self, seed: int) -> None:
        deck = await shuffle_deck(create_deck(), seed)
        game_state = GameState(deck=deck, players=[[], [], [], []])

        for i in range(4):
            game_state.players[i] = await deal_cards(game_state, 5)

        for i, player_hand in enumerate(game_state.players):
            print(f"Player {i + 1}'s hand: {', '.join(str(card) for card in player_hand)}")

        hand_ranks = [rank_hand(hand) for hand in game_state.players]
        max_rank = max(hand_ranks)
        winner_idx = hand_ranks.index(max_rank)
        print(
            f"Player {winner_idx + 1} wins with a {', '.join(str(card) for card in game_state.players[winner_idx])}!")
