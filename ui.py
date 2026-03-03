from montecarlo import Infos, prizepool
import matplotlib.pyplot as plt

def input_cfg() -> Infos: 
    
    """
    Prompt the user for input values to configure the Monte Carlo simulation.
    This function collects various parameters from the user, 
    including the expected value of the game (cev),
    the number of games to simulate, the starting bankroll, 
    the number of trajectories, the cost threshold for going broke, 
    and an optional seed for random number generation.
    Returns:
        Infos: An instance of the Infos dataclass containing the collected configuration parameters for the simulation.
    Raises:
        ValueError: If any of the input values are invalid (e.g., non-numeric values, cev out of range).
    """

    try:
        cev = float(input("Enter the expected value (cev) of the game: "))
        ngame = int(input("Enter the number of games to simulate in each trajectory (ngame): "))
        br_start = float(input("Enter the starting bankroll for each trajectory (br_start): "))
        nb_trajectorie = int(input("Enter the number of trajectories to simulate (nb_trajectorie): "))
        cost = float(input("Enter the cost threshold for going broke (cost): "))
        seed_input = input("Enter an optional seed for random number generation (or leave blank for no seed): ")
        seed = int(seed_input) if seed_input else None
    except ValueError:
        raise ValueError("Invalid input. Please enter numeric values for all parameters.")
    if cev < -500 or cev > 500:
            raise ValueError("Cev must be between -500 and 500.")
    grid = grid_import()
    cev_percent = round((cev + 500) / 1500 * 100, 2)
    return Infos(cev_percent, ngame, br_start, nb_trajectorie, cost, seed, grid)

def plot_histogram(data: list[float], bins=10) -> None:
    
    """Plot a histogram of the final bankrolls for the surviving trajectories using matplotlib.
    Args:
        data (list): A list of final bankrolls for the surviving trajectories.
        bins (int, optional): The number of bins to use in the
        histogram. Defaults to 10.
    """
    if not data:
        print("No survivors to display.")
        return
    plt.hist(data, bins=bins, edgecolor='black')
    plt.title('Histogram of Final Bankrolls for Survivors')
    plt.xlabel('Final Bankroll')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def grid_import() -> list[prizepool]:
    
    """
    Import the prize pool grid for the Monte Carlo simulation.
    This function creates and returns a list of prizepool instances representing the different prize levels based on predefined thresholds.
    Returns:
        list[prizepool]: A list of prizepool instances representing the prize levels for the simulation.
    """

    grid = [prizepool(1, 5938688, 2), prizepool(5938689, 8612896, 3), prizepool(8612897, 9437896, 5), prizepool(9437897, 9837896, 10), prizepool(9837897, 9997896, 50), prizepool(9997897, 9999896, 100), prizepool(9999897, 9999996, 1000), prizepool(9999997, 10000000, 100000)]
    return grid


def print_stats(stats):

    """
    Print the statistics of the Monte Carlo simulation results, including the percentage of trajectories that went broke,
the average drawdown, the average final bankroll for survivors, and a histogram of the final bankrolls for survivors.
    Args:
    stats (dict): A dictionary containing the statistics of the Monte Carlo simulation results, including:
        - broke_count: The number of trajectories that went broke.
        - sum_br: The sum of final bankrolls for all trajectories.
        - max_drawdown: The maximum drawdown observed across all trajectories.
        - sum_drawdown: The sum of drawdowns across all trajectories.
        - final_survived: A list of final bankrolls for the surviving trajectories.
        - nb_trajectorie: The total number of trajectories simulated.
        - percentiles: A list of percentiles for the final bankrolls of survivors (if available).
    Raises:
        ValueError: If the stats dictionary is missing required keys or contains invalid values.
    Note: The function calculates and prints various statistics based on the input stats dictionary, including the percentage of broke trajectories
    and the average drawdown. It also generates a histogram of the final bankrolls for survivors and prints percentiles if available.
    """

    avg_drawdown_all = stats["sum_drawdown"] / stats["nb_trajectorie"]
    survivors = stats["nb_trajectorie"] - stats["broke_count"]
    avg_brok_percent = stats["broke_count"] / stats["nb_trajectorie"] * 100
    labels = [0, 5, 30, 50, 70, 95, 100]
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
    if stats["percentiles"] is not None:
        print("Percentiles of final bankrolls for survivors:")
        for label, value in zip(labels, stats["percentiles"]):
            print(f"{label}th percentile: {value:.2f}")
    print("************************************************")
    plot_histogram(stats["final_survived"])

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