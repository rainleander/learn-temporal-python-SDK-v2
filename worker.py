import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from poker_workflow import PokerWorkflow
    from hand_ranking_workflow import HandRankingWorkflow


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="poker-hand-ranking-task-queue",
        workflows=[PokerWorkflow, HandRankingWorkflow],
    ):
        print("Worker started. Press Ctrl+C to stop.")
        await asyncio.sleep(3600)  # Keep the worker running for an hour


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped.")
