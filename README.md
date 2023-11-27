# KUHN POKER

## SUMMARY:
Using Counter Factual Regret Minimization and regret matching to try and generate the optimal strategy.
## RULES OF THE GAME:
Only 2 players in a game.Only 3 cards total can be dealt
meaning each player has a unique card. Can only be dealt
a Jack, a Queen, or a King. The King is the best card and a jack
is the worst card. The player with the best hand at showdown
(when no more actions can be taken) wins the pot (the money wagered).
The First Player to act (Player1) can either bet or check to
start the game. The Second player can either call/fold if bet to or
bet/check if checked to. A bet is when a player volentarily puts an additional
chip into the pot and a check is when a player choses not to bet and lets the next player act.
A check is only a valid option if you are the first player to act in a hand or if the player before you also checked.
A fold is when a player gives up the hand meaning the other player wins the hand.
If the first player checks and the second player bets player1
can either call or fold.
Each player posts 1 chip before the start of each hand before recieving
their card.
The bet size is limited to one chip meaning the
maximum pot size is 4 chips so the maximum amount one can win/lose
is 2.
With an optimal strategy player2 the second player to act
should win about 1/18 chips per hand and player 1 should lose at the same
rate since this is a 0 sum game.
## HOW STRATEGIES ARE REPRESENTED
Player1 and Player2 each have a unique strategy for each of the possible three hands.
This is represented as an matrix.
A row represents a strategy for a particular card.
Row index 0 is the strategy for a jack index 1 the queen index 3 the king
Each column represents a percentage that each strategy should be taken for player1
the columns represent the following:
[check,bet,fold_when_bet_to_after_check, call_when_bet_to_after_check].
For player2 the array is structred as:
[check_check,bet_check,bet_fold,bet_call].
For both players the first two and last two elements of the array should sum to 1
since each column in a row is a decimal representing the probability it will take each action.


## HOW IT WORKS
Go through each possible card for both the first and the second player.
Determine how much money Player1 and Player2 is winning/losing at their current strategies.
For each column in the matrix of strategies set 1 of the possible decision nodes to 100% meaning
play that particular action 100% of the time. This as well as the expected value we recieve at our current
strategy is how we calculate regret. We take the total ev of if we played one particular strategy 100% of the time
subtracted the expected value at our current strategy. This is done in order to see if we should play this strategy more frequently.
For example lets say at our current strategy against our opponents strategy we have an expected value of 1 chip a hand.
Now to calculate the regret of say Checking. We essentially switch the percentage of the time we play bet to 0 and keep everything else
the same including our opponents strategy. We then again calculate the expected value at this modified strategy which we will call ms for modified strategy.
We then do ms - ev (our expected value at current strategy). This then becomes the regret for the specific action. Note that
only positive regrets are taken into account and any negative regrets are set to 0.
The next time we go through our training loop our strategy will be our normalized regrets so if I regreted betting -1 and checking .25.
Then the for the next iteration i'll play betting at max(0,-1)/(max(0,-1) + max(0,.25))
and i'll do the same equation for checking so my next strategy will be bet: 0 check: 1.
The reason behind this is to not be exploited by our opponent.
Our final strategy is then the average of our normalized regrets.
Note also that if the regrets sum to 0 we then chose a uniform probability for our next strategy.
Also it should be noted that only strategies on the same level of the decision tree should be normalized.
For example for player one the first decision node is bet or check. While calling a bet if player 1 checks and player 2 bets is
also a strategy the strategy for calling a bet if i check and then am bet in to or fold if bet in to is on a different level or branch
of the game tree so only the intial check or fold will be normalized and the choice to call or fold when i check and am bet in to
is its own probability that should be normalized. In summary any decision that can be made at a particular point should be normalized.

## UPDATE
Strategies are now selected at each stages based on normalized total regret

## FILES
### main.py gives the accurate results and selects the next strategy based on the normalized total regret based on all iterations.
### kuhn.py gives almost accurate results but selects next strategy based soley on the regrets from the previous iterations and the
final strategy is the average across all training iterations.
#### thesis_submission.pdf: a paper that breaks down counter factual regret minimization CFRM in a very simple easy to understand language

## Sources
[Good clear PDF on CFRM](thesis_submission.pdf)
