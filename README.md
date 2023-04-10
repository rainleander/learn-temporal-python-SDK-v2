## Demo Feedback Guidelines/Requests
Please give feedback within *5 business days* by 14apr2023 1700 PST<br>
Please use review types:  Grammar or Typo (G), Unclear (U), Technical Accuracy (T), or Other (O)

G: This doesn’t flow, instead, what about this:<br>
U: When I read this I think “xyz”, which is confusing to what you mean, can you help clarify what you meant?<br>
T: This doesn’t reflect the response we should get, instead we should see “xyz”<br>
O: This was mentioned earlier, can we combine?

# WIP Learn Temporal Python SDK v2
This project is intended to show my process through learning Temporal and is not meant to showcase production-level best practices.

The program is a simple implementation of a five card draw poker game using the Temporal Python SDK. It is split into separate files for each component of the program: the main workflow, the shuffle activity, the child workflow for ranking hands, and the worker to execute the activity and workflows.

Learn Temporal Python SDK v1 is [over here](https://github.com/rainleander/learn-temporal-pythonSDK)

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
- [ ] [signals](https://docs.temporal.io/concepts/what-is-a-signal/)
- [ ] [queries](https://docs.temporal.io/concepts/what-is-a-query/) 
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
5. Run the file locally: 
```
python3 main.py
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
