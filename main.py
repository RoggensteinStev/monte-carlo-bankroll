from ui import input_cfg, print_stats
from montecarlo import MonteCarloSimulator

def main():

    """ Main function to execute the Monte Carlo simulation. 
    It prompts the user for input values, runs the simulation, and prints the results. 
    """
    try:
        cfg = input_cfg()
        simulator = MonteCarloSimulator(cfg)
        stats = simulator.run_monte_carlo()
        print_stats(stats)
    except ValueError as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()