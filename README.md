# WIP Learn Temporal Python SDK v2
This project is intended to show my process through learning [Temporal](http://temporal.io/) and is not meant to showcase production-level best practices.

The program is a simple implementation of a five card draw poker game using the [Temporal Python SDK](https://github.com/temporalio/sdk-python). The main components of the application are:

`starter.py`: Starts the Temporal client, connects to the server, and executes the `PokerWorkflow` with a seed value.

`worker.py`: Initializes a Temporal worker to execute the `PokerWorkflow` and `HandRankingWorkflow` workflows, and connects to the Temporal server. It keeps the worker running for an hour.

`poker_workflow.py`: Defines the `PokerWorkflow`, which simulates a poker game. It creates and shuffles a deck of cards, deals hands to players, and prints their hands. It then evaluates the hands using the `HandRankingWorkflow` and determines the winner.

`hand_ranking.py`: Contains utility functions to rank poker hands and draw cards.

`hand_ranking_workflow.py`: Defines the `HandRankingWorkflow`, which takes a poker hand as input and returns its rank.

`deck_utils.py`: Contains utility functions to create, shuffle, and deal cards from a deck.

`game_state.py`: Defines a `GameState` class that represents the state of the game, including the deck of cards and player hands.

`card.py`: Defines Card, Suit, and Rank classes, which are used to represent playing cards in the application.

Learn Temporal Python SDK v1 is [over here](https://github.com/rainleander/learn-temporal-python-SDK).

## AppDev Process
- [x] deck
- [x] shuffle
- [x] deal
- [x] score
- [x] multiple player game 
- [x] split out application into temporal specific functions: worker, workflow, activity 
- [x] [workflow](https://docs.temporal.io/application-development/foundations) 
- [x] [activities](https://docs.temporal.io/application-development/features) 
- [x] [child workflows](https://docs.temporal.io/workflows#child-workflow)
- [ ] [signals](https://docs.temporal.io/concepts/what-is-a-signal/) [in progress]
- [ ] [queries](https://docs.temporal.io/concepts/what-is-a-query/) [in progress]
- [ ] add a unit test
- [ ] write v2.0 blog post

## Run the App Locally
1. Make sure you have Python 3.7 or later installed on your system. You can check your Python version by running the following command in your terminal:
```
python --version
```
2. Clone the repository to your local machine:
```
git clone https://github.com/rainleander/learn-temporal-python-SDK-v2.git
```
3. Navigate to the directory where the repository was cloned:
```
cd learn-temporal-python-SDK-v2/
```
3. Create and activate a virtual environment:
```
python3 -m venv env
source env/bin/activate
```
4. Install Temporal server locally by [following the instructions](https://docs.temporal.io/docs/server/quick-install) in the Temporal documentation. Ensure that the Temporal server is running before proceeding to the next step.
5. Start the worker: 
```
python3 worker.py
```
6. Open a second tab/window, navigate to the project directory, if needed, and activate the virtual environment, if needed:
```
cd path/to/learn-temporal-python-SDK-v2/
source env/bin/activate
```
7. Run the starter:
```
python3 starter.py
```
The application should now run and display the hands dealt to each of the four players, and eventually, the winner of the game.
```
% python3 main.py
Player 1's hand: Four♠, Six♣, J♦, K♠, K♥
Player 2's hand: Eight♣, Two♦, Two♥, Ten♣, K♣
Player 3's hand: Three♠, Six♦, Five♠, Nine♦, Q♦
Player 4's hand: Six♠, J♣, Ten♠, A♠, Seven♣
Player 1 wins with a Four♠, Six♣, J♦, K♠, K♥!
```
