from temporalio import workflow

from deck_utils import create_deck, deal_cards, shuffle_deck
from game_state import GameState
from hand_ranking_workflow import HandRankingInput, HandRankingWorkflow


@workflow.defn
class PokerWorkflow:
    @workflow.run
    async def run(self, seed: int) -> None:
        deck = await shuffle_deck(create_deck(), seed)
        game_state = GameState(deck=deck, players=[[], [], [], []])

        for i in range(4):
            game_state.players[i] = await deal_cards(game_state, 5)

        for i, player_hand in enumerate(game_state.players):
            print(
                f"Player {i + 1}'s hand: {', '.join(str(card) for card in player_hand)}"
            )

        hand_ranks = [
            await workflow.execute_child_workflow(
                HandRankingWorkflow.run,
                HandRankingInput([str(card) for card in hand]),
            )
            for hand in game_state.players
        ]

        max_rank = max([rank[0] for rank in hand_ranks])
        winning_hands = [
            (i, rank) for i, rank in enumerate(hand_ranks) if rank[0] == max_rank
        ]
        winner_idx, winner_rank = max(
            winning_hands, key=lambda x: (x[1][0], x[1][1])
        )

        print(
            f"Player {winner_idx + 1} wins with a {', '.join(str(card) for card in game_state.players[winner_idx])}!"
        )
