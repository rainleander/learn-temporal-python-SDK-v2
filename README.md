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
- [ ] split out application into temporal specific functions: worker, workflow, activity 
- [ ] [workflow](https://docs.temporal.io/application-development/foundations) 
- [ ] [activities](https://docs.temporal.io/application-development/features) 
- [ ] [child workflows](https://docs.temporal.io/workflows#child-workflow)
- [ ] [signals](https://docs.temporal.io/concepts/what-is-a-signal/)
- [ ] [queries](https://docs.temporal.io/concepts/what-is-a-query/) 
- [ ] add a unit test
- [ ] write v2.0 blog post

## Run the App Locally
1. Clone the repository to your local machine:
```
git clone https://github.com/rainleander/learn-temporal-python-SDK-v2.git
```
2. Navigate to the directory where the repository was cloned:
```
cd learn-temporal-python-SDK-v2/
```
3. Create and activate a virtual environment:
```
python3 -m venv env
source env/bin/activate
```
4. Run the file locally: 
```
python poker.py
```
5. Follow the prompts to play the game in the terminal.
