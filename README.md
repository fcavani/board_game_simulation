# Board Game Simulation

This is a property buy and rent simulation (discrete events simulation).

Run it:

```bash
./simulation.py
```

The tests are implemented using pytest (you need to install it).

To run the tests just:
```bash
PYTHONPATH=. pytest -vv
```

## Initial state

- All players starts with $300.00.
- The properties and rent prices are draw from a normal distribution. The mean and sigma values impact directly on the simulations results.
- The dice number are draw from a uniform distribution.
- The seed are fixed at 42.

## If you want to play

- Change the mean and sigma of the price and rent values.
- You can try to use three distributions one for chip, other for not so chip and another for the expensive properties.
- Try to draw from a distribution that are a mixture of normals.
- You can change the behavior of the players.
- Try to change the random number generator seed at each game. Run a lot of simulations and see what happens.
