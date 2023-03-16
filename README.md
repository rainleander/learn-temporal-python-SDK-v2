# WIP Learn Temporal Python SDK v2
This project is intended to show my process through learning Temporal and is not meant to showcase production-level best practices.

Learn Temporal Python SDK v1 is [over here](https://github.com/rainleander/learn-temporal-pythonSDK)

## AppDev Process
- [ ] split out application into temporal specific functions: worker, workflow, activity [in progress]
- [ ] deck
- [ ] shuffle
- [ ] deal
- [ ] score
- [ ] single player game 
- [ ] [workflow](https://docs.temporal.io/application-development/foundations) 
- [ ] [activities](https://docs.temporal.io/application-development/features) 
- [ ] [child workflows](https://docs.temporal.io/workflows#child-workflow)
- [ ] [signals](https://docs.temporal.io/concepts/what-is-a-signal/)
- [ ] [queries](https://docs.temporal.io/concepts/what-is-a-query/) 
- [ ] add a unit test
- [ ] write v2.0 blog post

### How to Play
~~~
> python3 main.py
You have 100 points

Deck Shuffled
[10♠, J♡, 4♡, A♣, K♢]
Which cards do you want to discard? ( ie. 1, 2, 3 )
*Just hit return to hold all, type exit to quit
3
[10♠, J♡, 3♣, A♣, K♢]

You have 95 points

Deck Shuffled
[A♡, 8♣, Q♣, 5♡, 3♣]
Which cards do you want to discard? ( ie. 1, 2, 3 )
*Just hit return to hold all, type exit to quit
2, 3, 4, 5
[A♡, A♢, 10♡, 10♠, J♠]
Two Pairs!
+10

You have 100 points

Deck Shuffled
[3♠, 10♢, 6♡, 4♠, 8♡]
Which cards do you want to discard? ( ie. 1, 2, 3 )
*Just hit return to hold all, type exit to quit
exit
~~~
