from typing import List

from temporalio.workflow import workflow_method, WorkflowClient, Workflow
from temporalio.activity_method import activity_method
from temporalio.exceptions import WorkflowExecutionAlreadyStartedError
from temporalio.query import QueryMethod
from temporalio.signal_method import signal_method

from activities import deal_cards, evaluate_hand
from child_workflow import determine_winner


class PokerWorkflow:
    @activity_method(task_queue='poker_activities')
    async def deal(self, num_players: int) -> List[List[str]]:
        pass

    @activity_method(task_queue='poker_activities')
    async def evaluate(self, hands: List[List[str]]) -> List[str]:
        pass

    @workflow_method(task_queue='poker_workflow')
    async def play_poker_workflow(cls, num_players: int):
        winner = ''
        hands = []
        workflow = Workflow.current_workflow()

        try:
            child_workflow = workflow.execute_child_workflow(
                determine_winner, num_players=num_players)
            winner = child_workflow.result()

        except WorkflowExecutionAlreadyStartedError:
            print('WorkflowExecutionAlreadyStartedError: Workflow already running')
            return

        hands = await workflow.execute_activity(deal_cards, num_players)
        scores = await workflow.execute_activity(evaluate_hand, hands)

        if winner:
            await workflow.wait_for_signal('restart_game')
            await workflow.signal_child_workflow(child_workflow.workflow_id, 'send_winner', winner)

        else:
            winner = scores.index(max(scores))
            print(f'Player {winner+1} wins!')
            await workflow.wait_for_signal('restart_game')
            await workflow.signal_child_workflow(child_workflow.workflow_id, 'send_winner', f'Player {winner+1}')


class PokerWorkflowQueries:
    @staticmethod
    @QueryMethod()
    async def get_winner() -> str:
        pass


class PokerWorkflowSignals:
    @staticmethod
    @signal_method()
    async def restart_game():
        pass


class PokerWorkflowWorker:
    def __init__(self):
        self.client = WorkflowClient.new_client(namespace='default')

    def run(self):
        worker = self.client.new_worker(
            task_queue='poker_workflow', 
            activities=[deal_cards, evaluate_hand],
            workflows=[PokerWorkflow.play_poker_workflow],
            queries=[PokerWorkflowQueries.get_winner],
            signals=[PokerWorkflowSignals.restart_game]
        )
        worker.start()
