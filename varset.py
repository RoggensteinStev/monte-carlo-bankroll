import random
import sys

def print_stats(stats):

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

def inputval() -> tuple[float, float, int, float, int, float]:
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
    broke_count = 0
    sum_br = 0
    sum_min_br = 0
    max_drawdown = 0
    sum_drawdown = 0
    sum_drawdown_survived = 0
    for j in range(nb_trajectorie):
        broke, br_temp, min_br, drawdown = simulate_trajectory(mu, sigma, ngame, br_start, cost)
        if broke:
            broke_count += 1
        else:
            sum_br += br_temp
            sum_min_br += min_br
            sum_drawdown_survived += drawdown
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
    "sum_drawdown": sum_drawdown
    }

def main():
    mu, sigma, ngame, br_start, nb_trajectorie, cost = inputval()
    stats = run_monte_carlo(mu, sigma, ngame, br_start, cost, nb_trajectorie)
    print_stats(stats)

if __name__ == "__main__":
    main()