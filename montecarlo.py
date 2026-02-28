import random
import sys

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
            br_temp += self.rng.normalvariate(self.cfg.mu, self.cfg.sigma) 
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
    
    def validate_cfg(self):
        
        """
        Validate the configuration parameters for the Monte Carlo simulation.
        This method checks that all parameters are within acceptable ranges and prints error messages if any issues are
        found. If any parameter is invalid, the program will exit with an error message.
        """

        if self.cfg.sigma < 0:
            raise ValueError("Sigma must be non-negative.")
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
        Run the Monte Carlo simulation for a specified number of trajectories.
        Simulates multiple trajectories of bankroll changes and collects statistics on the outcomes,
        including counts of broke trajectories, sums of final bankrolls, minimum bankrolls, drawdowns, and the number of trajectories.
        Returns:
            dict: A dictionary containing the results of the Monte Carlo simulation, including:
            - "broke_count": The number of trajectories that went broke.
            - "sum_br": The sum of final bankrolls for surviving trajectories.
            - "sum_min_br": The sum of minimum bankrolls for surviving trajectories.
            - "sum_drawdown_survived": The sum of drawdowns for surviving trajectories.
            - "max_drawdown": The maximum drawdown observed across all trajectories.
            - "sum_drawdown": The sum of drawdowns across all trajectories.
            - "final_survived": A list of final bankrolls for surviving trajectories.
            - "nb_trajectorie": The total number of trajectories simulated.
        """
        self.validate_cfg()
        broke_count = 0
        sum_br = 0
        sum_min_br = 0
        max_drawdown = 0
        sum_drawdown = 0
        final_survived = []
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
        return {
        "broke_count": broke_count,
        "sum_br": sum_br,
        "sum_min_br": sum_min_br,
        "sum_drawdown_survived": sum_drawdown_survived,
        "max_drawdown": max_drawdown,
        "sum_drawdown": sum_drawdown,
        "final_survived": final_survived,
        "nb_trajectorie": self.cfg.nb_trajectorie
        }

@dataclass
class Infos:
    mu: float
    sigma: float
    ngame: int
    br_start: float
    nb_trajectorie: int
    cost: float
    seed: int | None = None
    