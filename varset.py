import random
import sys

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
min_br = br_start 
br_temp = br_start 
broke_count = 0
sum_br = 0
sum_min_br = 0
avg_brok_percent = 0
max_drawdown = 0
sum_drawdown = 0
sum_drawdown_survived = 0
survivors = 0

for j in range(nb_trajectorie):
    drawdown = 0
    peak = br_start
    br_temp = br_start
    min_br = br_start
    broke_status = False
    for i in range(ngame): 
        br_temp += random.normalvariate(valmu, valuesigma) 
        if br_temp > peak: 
            peak = br_temp
        if peak - br_temp > drawdown:
            drawdown = peak - br_temp
        if br_temp < min_br: 
            min_br = br_temp 
        if br_temp < cost:
            broke_status = True
            break
    if broke_status:
        broke_count += 1
    else:
        sum_br += br_temp
        sum_min_br += min_br
        sum_drawdown_survived += drawdown
    if drawdown > max_drawdown:
        max_drawdown = drawdown
    sum_drawdown += drawdown

avg_drawdown_all = sum_drawdown / nb_trajectorie
survivors = nb_trajectorie - broke_count
if broke_count != nb_trajectorie:
    avg_br_survived = sum_br / (nb_trajectorie - broke_count)
    avg_min_br_survived = sum_min_br / (nb_trajectorie - broke_count)
    avg_drawdown_survived = sum_drawdown_survived / (nb_trajectorie - broke_count)
if broke_count > 0:
    avg_brok_percent = broke_count / nb_trajectorie * 100

print("Broke :", avg_brok_percent, "%")
print("Broke count =", broke_count)
print("nb traj = ", nb_trajectorie)
print("max drawdown :", max_drawdown)
print("avg drawdown :", avg_drawdown_all)
if (survivors > 0):
    print("avg drawdown survived :", avg_drawdown_survived)
    print("avg min br :", avg_min_br_survived)
    print("avg br :", avg_br_survived)
print("survivors :", survivors)