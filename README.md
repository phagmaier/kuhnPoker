# KUHN POKER

## UPDATE
Took time off to explore other projects. After researching more carefuly I realized I was calculating regret incorrectly.
Will remedy this and fix with Kuhn poker. Like in the first version the code is pretty terrible I just want to get the logic
and solution down and after that I will try and make it better. Will keep version once corrected because I believe this is the
simpleset form despite not being very 'elegant' or smart. Will have it finished this week if I didn't also mess this up.
The problem was I was not calculating regret based on the expected results of each action vs the actual results of each action
and defining a new strategy based on that. "actual results" as I define it is the expected value of checking back when check to.
Which in the case of a jack is always -1. But with a new strategy the ev would become percent_player_1_check * percent_player_2_checks * -1.
The regrets are then used to create new strategy for training. Total regrets are then used to create a new strategy based on the normalized regret
meaning if I regret checking 1 and betting 2 the total is 3 so we check and a rate of 1/3 and bet at a rate of 2/3.
## SUMMARY:
Using Counter Factual Regret Minimization and regret matching to try and generate the optimal strategy for kuhn poker whose rules are below.
Currently not sure if the commented part of my cfr functions is the optimal strategy or if the current strategy is optimal should run sims to test.
Also very possible I made a mistake and this is not optimal plus I believe there are an infinite number of optimal strategies for at least player 1
and probably for player 2. Will add sims and then change accordingly.

## RULES OF THE GAME:
Only 2 players in a game.Only 3 cards total can be dealt
meaning each player has a unique card. Can only be dealt
a Jack, a Queen, or a King. The King is the best card and a jack
is the worst card. The player with the best hand at showdown
(when no more actions can be taken) wins the pot (the money wagered).
The First Player to act (Player1) can either bet or check to
start the game. The Second player can either call/fold if bet to or
bet/check if checked to.
If the first player checks and the second player bets player1
can either call or fold.
Each player posts 1 chip before the start of each hand before recieving
their card.
The bet size is limited to one chip meaning the
maximum pot size is 4 chips so the maximum amount one can win/lose
is 2.
With an optimal strategy player2 the second player to act
should lose about 1/18 a chip per hand played with player2
winning that same amount since it is  a 0 sum game

## HOW STRATEGIES ARE REPRESENTED
Player1 and Player2 each have a unique strategy for each of the possible three hands.
This is represented as an array for player1 it is:
[check,bet,fold_when_bet_to_after_check, call_when_bet_to_after_check].
For player one the array is structred as [check_check,bet_check,bet_fold,bet_call].
For both players the first two and last two elements of the array should sum to 100.


## HOW IT WORKS
Go through each possible card for both the first and the second player.
Determine the current value for each action with the current strategies for each player.
Calculate the regret of chosing strategy A rather than strategy b. For example
the regret of player one checking then calling a bet from player2 is calling - folding.
But because each player plays a mixed strategy you must account for the percentage of how often they
bet with certain hands. Which is why we do a cumulative regret for each hand. Because player 2 can have
any of the two other cards when we have a card we must find the regret for both of these conditions
to try and find the optimal strategy for say when we have a jack since they could have either a king or a queen.
Once we have our regrets we update our new strategy to bee each regret / sum of regrets.
Note that we do not include negative regrets we want to increase the percentage that we take actions we
regreted not taking and we can't have a negative percentage so all negative regrets are 0'd.
Once we have done this for x number of iterations tracking all our current strategies
(represented as percentages through decimal points)
we then sum all of these strategies and then didivide by the number of iterations and we do this
for each unique strategy for each unqiue card

## CURRENT PROBLEMS
My current problem is that I do not check for "dominated strategies" That should never be played
at equalibrium something like calling a Jack if bet to. I can also probably prune my searches by
eliminating going through strats that have a 100% or 0% chance of being played.

## NEED TO ADD
Check for dominated strategies that will never be played and that should never be played at equalibrium

## EXTRAS:
Included a solved version of rock paper siccors called rps.py to show an incredibly simplified version of this
algorithm in practice.


## Sources:
https://www.ma.imperial.ac.uk/~dturaev/neller-lanctot.pdf
