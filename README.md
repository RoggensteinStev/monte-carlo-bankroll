Monte Carlo Bankroll Simulator

Python-based Monte Carlo simulation engine to model bankroll variance,
risk of ruin, and distribution of outcomes using a discrete Spin & Go model.

The project is structured with a clear separation between:

- Simulation engine (montecarlo.py)
- User interface (CLI) (ui.py)
- Entry point (main.py)

Features

- Discrete Spin simulation (winner-take-all model)
- CEV-based win probability
- Prize pool grid simulation (realistic multiplier distribution)
- Monte Carlo simulation of bankroll trajectories
- Risk of ruin estimation
- Maximum and average drawdown
- Survivor statistics
- Histogram of final bankroll distribution
- Percentile tracking (P0 / P5 / P30 / P50 / P70 / P95 / P100)
- Config validation with proper exception handling
- Local RNG instance (no global random state pollution)

Usage

Run the simulator from the project root:

    python main.py

You will be prompted to enter:

- CEV (between -500 and 500)
- Number of games per trajectory
- Starting bankroll
- Number of trajectories
- Cost threshold (broke limit)
- Optional random seed

Architecture

main.py        -> program entry point
ui.py          -> CLI input/output
montecarlo.py  -> simulation engine

The simulation engine is reusable and independent from the CLI.

Roadmap

- Full 3-position payout model (1st / 2nd / 3rd)
- CSV export
- Graph visualization (matplotlib)
- Multi-scenario batch simulation