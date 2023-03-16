# WIP Learn Temporal Python SDK v2
This project is intended to show my process through learning Temporal and is not meant to showcase production-level best practices.

The program is a simple implementation of a five card draw poker game using the Temporal Python SDK. It is split into separate files for each component of the program: the main workflow, the game activity, the child workflow for restarting the game, the signal to restart the game, the query to retrieve the game state, and the worker to execute the activities and workflows.

The main workflow handles the game logic, including dealing cards, allowing players to discard and draw new cards, and determining the winner based on hand strength. The game activity is responsible for shuffling the deck and dealing cards to players. The child workflow is used to restart the game, allowing the main workflow to easily reset the game state.

The signal allows players to request a game restart at any time during the game, and the query can be used to retrieve the current game state, such as the number of players and their hands.

Finally, the worker executes the activities and workflows in a separate process, allowing for easy scaling and fault tolerance. Unit tests are included to ensure the program runs as expected.

Learn Temporal Python SDK v1 is [over here](https://github.com/rainleander/learn-temporal-pythonSDK)

## AppDev Process
- [x] deck
- [x] shuffle
- [x] deal
- [x] score
- [x] multiple player game 
- [x] split out application into temporal specific functions: worker, workflow, activity [in progress]
- [x] [workflow](https://docs.temporal.io/application-development/foundations) 
- [x] [activities](https://docs.temporal.io/application-development/features) 
- [x] [child workflows](https://docs.temporal.io/workflows#child-workflow)
- [x] [signals](https://docs.temporal.io/concepts/what-is-a-signal/)
- [x] [queries](https://docs.temporal.io/concepts/what-is-a-query/) 
- [x] add a unit test
- [x] write v2.0 blog post

## Run This Program
1. First, install the `temporalio` library by running `pip install temporalio` in your terminal.
2. Download main.py from this repository.
3. Open two terminals and navigate to the directory where main.py is located.
4. In one terminal, start the Temporal server by running the following command:
```
tctl -n <namespace> namespace register
```
Replace <namespace> with a unique namespace identifier, such as your username.
5. In the same terminal, start the Temporal worker by running the following command:
```
temporal worker --task-queue poker_game
```
This will start a worker that listens on the poker_game task queue, waiting for tasks to execute.
6. In the other terminal, run the poker.py file by running the following command:
```
python3 main.py
```
This will start the workflow by calling the workflow() function.
7. Wait for the workflow to complete. You should see output in both terminals indicating that the workflow is running and that the activity has been executed.
8. Once the workflow completes, the winner will be printed to the console.

Note that you can modify the num_players variable in the play_game() function to change the number of players in the game. You can also modify the task queue names and namespace as needed.
