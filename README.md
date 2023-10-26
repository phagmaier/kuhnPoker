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

## Sources:
https://www.ma.imperial.ac.uk/~dturaev/neller-lanctot.pdf
