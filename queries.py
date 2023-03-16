from temporal.query import QueryMethod

class PokerWorkflowQueries:
    @staticmethod
    @QueryMethod()
    async def get_winner() -> str:
        pass
