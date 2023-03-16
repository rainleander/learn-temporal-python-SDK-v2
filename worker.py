from temporalio.workflow import WorkflowClient
from workflow import PokerWorkflow, PokerWorkflowQueries, PokerWorkflowSignals
from activities import deal_cards, evaluate_hand

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
