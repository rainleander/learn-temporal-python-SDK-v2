from datetime import timedelta
from typing import Optional

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from deck_utils import create_and_shuffle_deck, deal_cards
    from game_state import GameState
    from hand_ranking_workflow import HandRankingInput, HandRankingWorkflow


@workflow.defn
class PokerWorkflow:
    @workflow.run
    async def run(self, seed: int) -> Optional[str]:
        deck = await workflow.execute_activity(
            create_and_shuffle_deck,
            seed,
            start_to_close_timeout=timedelta(seconds=5)
        )

        game_state = GameState(deck=deck, players=[[], [], [], []])

        for i in range(4):
            game_state.players[i] = await deal_cards(game_state, 5)

        player_hands_str = []
        for i, player_hand in enumerate(game_state.players):
            player_hands_str.append(f"Player {i + 1}'s hand: {', '.join(str(card) for card in player_hand)}")

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

        return '\n'.join(player_hands_str) + f"\nPlayer {winner_idx + 1} wins with a {', '.join(str(card) for card in game_state.players[winner_idx])}!"
