from typing import List
import time

from temporal.workflow import workflow_method, WorkflowClient, signal_method
from temporal.api.enums.v1 import EventType
from activity import check_hand


# Child Workflow
@workflow_method(task_queue="poker-score")
async def calculate_score(cards: List[int]) -> str:
    await asyncio.sleep(3)
    score = check_hand(cards)
    print(f"Score: {score}")
    return score
