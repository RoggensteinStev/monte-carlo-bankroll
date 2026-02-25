import random
import sys

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
    avg_brok_percent = 0
    if stats["broke_count"] != stats["nb_trajectorie"]:
        avg_br_survived = stats["sum_br"] / (stats["nb_trajectorie"] - stats["broke_count"])
        avg_min_br_survived = stats["sum_min_br"] / (stats["nb_trajectorie"] - stats["broke_count"])
        avg_drawdown_survived = stats["sum_drawdown_survived"] / (stats["nb_trajectorie"] - stats["broke_count"])
    if stats["broke_count"] > 0:
        avg_brok_percent = stats["broke_count"] / stats["nb_trajectorie"] * 100
    
    print("************************************************")
    print("Monte Carlo Simulation Results:")
    print("Stats :")
    print("Broke :", f"{avg_brok_percent:.2f}", "%")
    print("Broke count =", stats["broke_count"])
    print("nb traj = ", stats["nb_trajectorie"])
    print("max drawdown :", f"{stats['max_drawdown']:.2f}")
    print("avg drawdown :", f"{avg_drawdown_all:.2f}")
    if (survivors > 0):
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

def inputval() -> tuple[float, float, int, float, int, float]:
    
    """
    Prompt the user for input values required for the Monte Carlo simulation.
    Returns:
            tuple: A tuple containing the input values in the following order:
            (mu, sigma, ngame, br_start, nb_trajectorie, cost)
    """

    valmu = (float)(input("Enter mu :")) 
    valuesigma = (float)(input("Enter sigma :"))
    ngame = (int)(input("Nb games :"))
    br_start = (float)(input("Br start : "))
    nb_trajectorie = (int)(input("nb trajectorie :"))
    cost = (float)(input("cost : "))
    if nb_trajectorie <= 0:
        print("Error, nb trajectorie must be > 0")
        sys.exit(1)
    if ngame <= 0:
        print("Error, nb game must be > 0")
        sys.exit(1)
    if cost <= 0:
        print("Error, cost must be > 0")
        sys.exit(1)
    return valmu, valuesigma, ngame, br_start, nb_trajectorie, cost

def simulate_trajectory(mu, sigma, ngame, br_start, cost) -> tuple[bool, float, float, float]:
    
    """
    Simulate a single trajectory of bankroll changes over a specified number of games.
    Args:
        mu (float): The mean of the normal distribution for bankroll changes.
        sigma (float): The standard deviation of the normal distribution for bankroll changes.
        ngame (int): The number of games to simulate in the trajectory.
        br_start (float): The starting bankroll for the trajectory.
        cost (float): The cost threshold below which the bankroll is considered broke.
    Returns:
        tuple: A tuple containing the following values:
        - broke (bool): Whether the bankroll went broke (True if it fell below the cost).
        - final_br (float): The final bankroll at the end of the trajectory.
        - min_br (float): The minimum bankroll observed during the trajectory.
        - drawdown (float): The maximum drawdown observed during the trajectory.
    """

    br_temp = br_start
    min_br = br_start
    drawdown = 0
    peak = br_start
    broke = False
    for i in range(ngame): 
        br_temp += random.normalvariate(mu, sigma) 
        if br_temp > peak: 
            peak = br_temp
        if peak - br_temp > drawdown:
            drawdown = peak - br_temp
        if br_temp < min_br: 
            min_br = br_temp 
        if br_temp < cost:
            broke = True
            break
    return broke, br_temp, min_br, drawdown


def run_monte_carlo(mu, sigma, ngame, br_start, cost, nb_trajectorie) -> dict:
    
    """
    Run the Monte Carlo simulation for a specified number of trajectories.
    Simulates multiple trajectories of bankroll changes and collects statistics on the outcomes,
    including counts of broke trajectories, sums of final bankrolls, minimum bankrolls, drawdowns, and the number of trajectories.
    Args:
        mu (float): The mean of the normal distribution for bankroll changes.
        sigma (float): The standard deviation of the normal distribution for bankroll changes.
        ngame (int): The number of games to simulate in each trajectory.
        br_start (float): The starting bankroll for each trajectory.
        cost (float): The cost threshold below which the bankroll is considered broke.
        nb_trajectorie (int): The number of trajectories to simulate.
    Returns:
        dict: A dictionary containing the results of the Monte Carlo simulation, including:
        - "broke_count": The number of trajectories that went broke.
        - "sum_br": The sum of final bankrolls for surviving trajectories.
        - "sum_min_br": The sum of minimum bankrolls for surviving trajectories.
        - "sum_drawdown_survived": The sum of drawdowns for surviving trajectories.
        - "max_drawdown": The maximum drawdown observed across all trajectories.
        - "nb_trajectorie": The total number of trajectories simulated.
        - "sum_drawdown": The sum of drawdowns across all trajectories.
        - "final_survived": A list of final bankrolls for surviving trajectories.
    """

    broke_count = 0
    sum_br = 0
    sum_min_br = 0
    max_drawdown = 0
    sum_drawdown = 0
    final_survived = []
    sum_drawdown_survived = 0
    for j in range(nb_trajectorie):
        broke, br_temp, min_br, drawdown = simulate_trajectory(mu, sigma, ngame, br_start, cost)
        if broke:
            broke_count += 1
        else:
            sum_br += br_temp
            sum_min_br += min_br
            sum_drawdown_survived += drawdown
            final_survived.append(br_temp)
        if drawdown > max_drawdown:
            max_drawdown = drawdown
        sum_drawdown += drawdown
    return {
    "broke_count": broke_count,
    "sum_br": sum_br,
    "sum_min_br": sum_min_br,
    "sum_drawdown_survived": sum_drawdown_survived,
    "max_drawdown": max_drawdown,
    "nb_trajectorie": nb_trajectorie,
    "sum_drawdown": sum_drawdown,
    "final_survived": final_survived
    }

def main():

    """ Main function to execute the Monte Carlo simulation. 
    It prompts the user for input values, runs the simulation, and prints the results. 
    """
    
    mu, sigma, ngame, br_start, nb_trajectorie, cost = inputval()
    stats = run_monte_carlo(mu, sigma, ngame, br_start, cost, nb_trajectorie)
    print_stats(stats)

if __name__ == "__main__":
    main()