import asyncio
import time
from temporalio.client import Client
from temporalio.worker import Worker
from poker_workflow import PlayGame
from deck_utils import shuffle_deck


async def main():
    # Start client
    client = await Client.connect("localhost:7233")
    seed = int(time.time())

    async with Worker(
            client,
            task_queue="poker-activity-task-queue",
            workflows=[PlayGame],
            activities=[shuffle_deck],
    ):
        result = await client.execute_workflow(
            PlayGame.run,
            args=(seed,),  # Pass the seed as a tuple
            id="poker-pycharm-workflow-id",
            task_queue="poker-activity-task-queue",
        )

if __name__ == "__main__":
    asyncio.run(main())
