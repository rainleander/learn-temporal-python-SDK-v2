from temporal.workerfactory import WorkerFactory
from temporal.activity_method import ActivityOptions

from poker_activity import PokerActivity, draw_cards, evaluate_hand

# Set up the worker factory
factory = WorkerFactory("poker", activities=[PokerActivity])

# Register the activity methods
factory.register_activity_implementation(draw_cards)
factory.register_activity_implementation(evaluate_hand)

# Start the worker
worker = factory.new_worker(task_queue="poker_game")
worker.start()
