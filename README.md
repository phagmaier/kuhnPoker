# KUHN POKER

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
The way I'm implimenting the algorithm does not seem to be yeilding the optimal results.
Play2 should win about 1/18 chips a hand and player1 should lose about the same but in
my current implimentation playr2 seems to be losing at a margin of about 1/1000 per hand
so the two players are close to equilibrium even though this game does not have a perfectly equal
strategy for both players and as stated earlier player2 should have the advantage.


## Sources:
https://www.ma.imperial.ac.uk/~dturaev/neller-lanctot.pdf
