import asyncio
import time

from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from hand_ranking_workflow import HandRankingWorkflow
    from poker_workflow import PokerWorkflow


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="poker-hand-ranking-task-queue",
        workflows=[PokerWorkflow, HandRankingWorkflow],
    ):
        seed = int(time.time())
        await client.execute_workflow(
            PokerWorkflow.run,
            seed,
            id="poker-hand-ranking-workflow-id",
            task_queue="poker-hand-ranking-task-queue",
        )


if __name__ == "__main__":
    asyncio.run(main())
