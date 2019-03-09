# Kalaha
<i>Alpha-Beta Pruning and Minimax (Python)</i>

## Files
1) Kalaha.py: Initialise environment, agents and gamestyle
2) KalahaEnv.py: Defines the Kalaha environment/game/board
3) KalahaAgent.py: Defines a Kalaha agent/player with a given strategy

## Gamestyles
1) Human vs Human
2) Human vs Agent
3) Agent vs Agent (not rendered)

## Agent strategies
1) random: moves randomly within legal options
2) front: picks non-empty pit closest to target
3) back: picks non-empty pit furthest from target
4) back: picks non-empty pit furthest from target
5) max_balls: picks pit with most balls cloest to target

//TODO
MINIMAX: uses minimax algorithm to choose next move
ABPRUNE: uses alpha-beta pruning algorithm to choose next move
NYG316: most optimal player using ab-pruning

## To play
1) Define gamestyle
2) Define agent strategies

```bash
python kalaha.py
```