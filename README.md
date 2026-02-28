Monte Carlo Bankroll Simulator

Python-based Monte Carlo simulation engine to model bankroll variance and risk of ruin.

The project is structured with a clear separation between:

Simulation engine (montecarlo.py)

User interface (CLI) (ui.py)

Entry point (main.py)

Features

Monte Carlo simulation of bankroll trajectories

Risk of ruin estimation

Maximum and average drawdown

Survivor statistics

Histogram of final bankroll distribution

Config validation with proper exception handling

Local RNG instance (no global random state pollution)

Usage

Run the simulator from the project root:

python main.py

You will be prompted to enter:

mu (mean gain per game)

sigma (standard deviation per game)

number of games

starting bankroll

number of trajectories

cost threshold

optional random seed

Architecture
main.py        -> program entry point
ui.py          -> CLI input/output
montecarlo.py  -> simulation engine

The simulation engine is reusable and independent from the CLI.

Roadmap

Discrete payout model (realistic Spin & Go simulation)

Percentile tracking (P5 / P50 / P95)

CSV export

Graph visualization