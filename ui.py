from montecarlo import Infos

def input_cfg() -> Infos:
    
    """
    Prompt the user for input values to configure the Monte Carlo simulation.
    The function collects the following parameters from the user:
    - mu: The mean change in bankroll per game.
    - sigma: The standard deviation of the change in bankroll per game.
    - ngame: The number of games to simulate in each trajectory.
    - br_start: The starting bankroll for each trajectory.
    - nb_trajectorie: The number of trajectories to simulate.
    - cost: The cost threshold for going broke.
    - seed: An optional seed for random number generation to ensure reproducibility.
    Returns:
        Infos: An instance of the Infos dataclass containing the collected configuration parameters.
    """
    try:
        mu = float(input("Enter the mean change in bankroll per game (mu): "))
        sigma = float(input("Enter the standard deviation of the change in bankroll per game (sigma): "))
        ngame = int(input("Enter the number of games to simulate in each trajectory (ngame): "))
        br_start = float(input("Enter the starting bankroll for each trajectory (br_start): "))
        nb_trajectorie = int(input("Enter the number of trajectories to simulate (nb_trajectorie): "))
        cost = float(input("Enter the cost threshold for going broke (cost): "))
        seed_input = input("Enter an optional seed for random number generation (or leave blank for no seed): ")
        seed = int(seed_input) if seed_input else None
        return Infos(mu, sigma, ngame, br_start, nb_trajectorie, cost, seed)
    except ValueError:
        raise ValueError("Invalid input. Please enter numeric values for all parameters.")

def print_stats(stats):

    """Print the results of the Monte Carlo simulation. 
    Calculates and displays the average drawdown, average bankroll for survivors, 
    and other relevant statistics. 
    Args: stats (dict): A dictionary containing the results of the Monte Carlo simulation, 
    including counts of broke trajectories, sums of final bankrolls, 
    minimum bankrolls, drawdowns, and the number of trajectories. 
    """

    avg_drawdown_all = stats["sum_drawdown"] / stats["nb_trajectorie"]
    survivors = stats["nb_trajectorie"] - stats["broke_count"]
    avg_brok_percent = stats["broke_count"] / stats["nb_trajectorie"] * 100
    if survivors > 0:
        avg_br_survived = stats["sum_br"] / survivors
        avg_min_br_survived = stats["sum_min_br"] / survivors
        avg_drawdown_survived = stats["sum_drawdown_survived"] / survivors
    
    print("************************************************")
    print("Monte Carlo Simulation Results:")
    print("Stats :")
    print("Broke :", f"{avg_brok_percent:.2f}", "%")
    print("Broke count =", stats["broke_count"])
    print("nb traj = ", stats["nb_trajectorie"])
    print("max drawdown :", f"{stats['max_drawdown']:.2f}")
    print("avg drawdown :", f"{avg_drawdown_all:.2f}")
    if survivors > 0:
        print("avg drawdown survived :", f"{avg_drawdown_survived:.2f}")
        print("avg min br :", f"{avg_min_br_survived:.2f}")
        print("avg br :", f"{avg_br_survived:.2f}")
    print("survivors :", survivors)
    print_histogram(stats["final_survived"])
    print("************************************************")

def print_histogram(values, bins=10):
    
    """
    Print a histogram of the final bankrolls for the surviving trajectories.
    Args:
        values (list): A list of final bankrolls for the surviving trajectories.
        bins (int, optional): The number of bins to use in the histogram. If None,
        it will be calculated based on the number of values.
    """

    if not values:
        print("No survivors to display.")
        return
    min_value = min(values)
    max_value = max(values)
    if min_value == max_value:
        print("Histogram of final bankrolls:")
        print(f"{min_value:.2f}: {'#' * len(values)} ({len(values)})")
        return
    bin_size = (max_value - min_value) / bins
    histogram = [0] * bins
    for value in values:
        if value == max_value:
            histogram[-1] += 1
        else:
            index = int((value - min_value) / bin_size)
            histogram[index] += 1
    print("Histogram of final bankrolls:")
    for i in range(bins):
        lower_bound = min_value + i * bin_size
        upper_bound = lower_bound + bin_size
        print(f"{lower_bound:.2f} - {upper_bound:.2f}: {'#' * histogram[i]} ({histogram[i]})")