import asyncio
import time

from temporalio.client import Client
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from poker_workflow import PokerWorkflow


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    seed = int(time.time())
    results = await client.execute_workflow(
        PokerWorkflow.run,
        seed,
        id="poker-hand-ranking-workflow-id",
        task_queue="poker-hand-ranking-task-queue",
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
