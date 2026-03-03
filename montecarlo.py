import random


from dataclasses import dataclass

class MonteCarloSimulator:
    
    """
    A class to perform Monte Carlo simulations of bankroll changes over a series of games.
    It includes methods for simulating trajectories, running the simulation, and printing results.
    """

    def __init__(self, cfg):
        
        """
        Initialize the Monte Carlo Simulator with the given configuration.
        Args:
            cfg (Infos): An instance of the Infos dataclass containing the configuration parameters for the simulation.
        
        The constructor sets the configuration and initializes the random seed if provided.
        """
        self.rng = random.Random()
        self.cfg = cfg
        if self.cfg.seed is not None:
            self.rng.seed(self.cfg.seed)

    def simulate_trajectory(self) -> tuple[bool, float, float, float]:
           
        """
        Simulate a single trajectory of bankroll changes over a specified number of games.
        Returns:
            tuple: A tuple containing the following values:
            - broke (bool): Whether the bankroll went broke (True if it fell below the cost).
            - final_br (float): The final bankroll at the end of the trajectory.
            - min_br (float): The minimum bankroll observed during the trajectory.
            - drawdown (float): The maximum drawdown observed during the trajectory.
        """

        br_temp = self.cfg.br_start
        min_br = self.cfg.br_start
        drawdown = 0
        peak = self.cfg.br_start
        broke = False
        for i in range(self.cfg.ngame): 
            br_temp += self.simulate_result() 
            if br_temp > peak: 
                peak = br_temp
            if peak - br_temp > drawdown:
                drawdown = peak - br_temp
            if br_temp < min_br: 
                min_br = br_temp 
            if br_temp < self.cfg.cost:
                broke = True
                break
        return (broke, br_temp, min_br, drawdown)
    
    def simulate_result(self) -> int:
        
        """
        Simulate the result of a single game based on the expected value percentage (cevpercent) and the prize pool grid.
        This method determines whether the outcome is a victory or a loss and calculates the resulting bankroll change accordingly.
        Returns:
            int: The change in bankroll based on the simulated game outcome. Positive for victories, negative for losses.
        """

        if self.simulate_victory():
            return self.simulate_grid()
        else:
            return -1

    def simulate_grid(self) -> int:
       
        """
        Simulate a grid outcome based on the defined prize pool and return the prize amount.
        The method generates a random number and checks it against the defined prize pool to determine the prize
        amount. The prize is calculated as the prize value from the grid minus 1.
        Returns:
            int: The prize amount based on the simulated grid outcome.
        """

        n = self.rng.randint(1, 10000000)
        prize = None
        for p in self.cfg.grid:
            if p.totalgamemin <= n <= p.totalgamemax:
                prize = p.prize
                break
        if prize is None:
            raise ValueError("grid coverage error")
        return prize - 1

    def simulate_victory(self) -> bool:
        
        """
        Simulate a victory based on the expected value percentage (cevpercent) provided in the configuration.
        Returns:
            bool: True if the simulated outcome is a victory, False otherwise.
        """

        n = self.rng.randint(1, 10000)
        if n <= self.cfg.cevpercent * 100:
            return True
        else:
            return False
        
    def validate_cfg(self):
        
        """
        Validate the configuration parameters for the Monte Carlo simulation.
        This method checks that all parameters are within acceptable ranges and prints error messages if any issues are
        found. If any parameter is invalid, the program will exit with an error message.
        """

        if not self.cfg.grid: 
            raise ValueError("Grid is missing/empty")
        if not (0 <= self.cfg.cevpercent <= 100):
            raise ValueError("Expected value percentage (cevpercent) must be between 0 and 100.")
        if self.cfg.ngame <= 0:
            raise ValueError("Number of games (ngame) must be greater than 0.")
        if self.cfg.br_start <= 0:
            raise ValueError("Starting bankroll (br_start) must be greater than 0.")
        if self.cfg.nb_trajectorie <= 0:
            raise ValueError("Number of trajectories (nb_trajectorie) must be greater than 0.")
        if self.cfg.cost < 0:
            raise ValueError("Cost threshold (cost) must be non-negative.")
        if self.cfg.br_start <= self.cfg.cost:
            raise ValueError("Starting bankroll (br_start) must be greater than cost threshold (cost).")
    
    def run_monte_carlo(self) -> dict:
        
        """
        Run the Monte Carlo simulation for a specified number of trajectories and collect statistics on the outcomes.
        This method simulates multiple trajectories of bankroll changes, counts how many went broke, sums the
        final bankrolls of survivors, calculates drawdowns, and collects final bankrolls for survivors. It returns a
        dictionary containing all the collected statistics, including the percentage of trajectories that went broke, 
        average drawdown, and percentiles of final bankrolls for survivors.
        Returns:
            dict: A dictionary containing the statistics of the Monte Carlo simulation results, including:
            - broke_count (int): The number of trajectories that went broke.
            - sum_br (float): The sum of final bankrolls for all surviving trajectories.
            - sum_min_br (float): The sum of minimum bankrolls observed across all trajectories.
            - sum_drawdown_survived (float): The sum of drawdowns for surviving trajectories.
            - max_drawdown (float): The maximum drawdown observed across all trajectories.
            - sum_drawdown (float): The total sum of drawdowns across all trajectories.
            - final_survived (list): A list of final bankrolls for the surviving trajectories.
            - nb_trajectorie (int): The total number of trajectories simulated.
            - percentiles (list or None): A list of percentiles for the final bankrolls of survivors, or None if there are no survivors.
        """

        self.validate_cfg()
        broke_count = 0
        sum_br = 0
        sum_min_br = 0
        max_drawdown = 0
        sum_drawdown = 0
        final_survived = []
        percentiles = None
        sum_drawdown_survived = 0
        for j in range(self.cfg.nb_trajectorie):
            broke, br_temp, min_br, drawdown = self.simulate_trajectory()
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
        if final_survived:
            percentiles = self.percentiles(final_survived)
        return {
        "broke_count": broke_count,
        "sum_br": sum_br,
        "sum_min_br": sum_min_br,
        "sum_drawdown_survived": sum_drawdown_survived,
        "max_drawdown": max_drawdown,
        "sum_drawdown": sum_drawdown,
        "final_survived": final_survived,
        "nb_trajectorie": self.cfg.nb_trajectorie,
        "percentiles": percentiles
        }

    def percentiles(self, values) -> list[float]:

        """
        Calculate specific percentiles from a list of values.
        This function calculates the 0th, 5th, 30th, 50th, 70th, 95th, and 100th percentiles from a list of values.
        Args:
            values (list): A list of numeric values from which to calculate the percentiles.
        Returns:
            list[float]: A list containing the calculated percentiles in the following order: [0th, 5th, 30th, 50th, 70th, 95th, 100th].
        Raises:
            ValueError: If the input list is empty, a ValueError is raised indicating that percentile calculation cannot be performed on an empty list.
        """

        if not values:
            raise ValueError("Empty values list for percentile calculation")
        sorted_values = sorted(values)
        n = len(sorted_values)
        p0 = sorted_values[0]
        p5 = sorted_values[int(0.05 * (n - 1))]
        p30 = sorted_values[int(0.30 * (n - 1))]
        p50 = sorted_values[int(0.5 * (n - 1))]
        p70 = sorted_values[int(0.70 * (n - 1))]
        p95 = sorted_values[int(0.95 * (n - 1))]
        p100 = sorted_values[-1]
        return [p0, p5, p30, p50, p70, p95, p100]

@dataclass
class prizepool:
    totalgamemin: int
    totalgamemax: int
    prize: int

@dataclass
class Infos:
    cev : float
    ngame: int
    br_start: float
    nb_trajectorie: int
    cost: float
    seed: int | None = None
    cevpercent : float = 0.0
    grid: list[prizepool] = None