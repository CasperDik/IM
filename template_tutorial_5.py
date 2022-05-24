# -*- coding: utf-8 -*-
"""
@author: josel
"""
import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt

#########----------------demand dist --------------###########

T_1 = list(range(1,40))

D_1 = [17,	15,	18,	10,	9, 15, 10, 10, 13, 11, 7, 14, 13, 17, 5,	
      14, 13, 10, 8, 9,	5,	12,	14,	12,	13,	10,	11,	14,	16,	11,	
      14, 10, 13, 9, 11, 14, 12, 7,	16]

# Step 1 : plot demand data
plt.plot(D_1)

#step 2: create and plot histogram data
hist_data = [[i, D_1.count(i)] for i in set(D_1)]
df_1 = pd.DataFrame(data=hist_data, columns=["D", "frequency"])
df_1.plot(x="D", y="frequency", kind="bar")

# step 3: transform frequency into empirical probability dist
obs = len(T_1)
df_1["Prob"] = df_1["frequency"]/obs


#########-----------demand dist (forecats errors)--------------###########

T_2 = list(range(1,40))

D_2 = [12,	12,	19,	14,	10,	19,	14,	16,	18,	18,	18,	21,	15,	
       15,	10,	18,	16,	11,	25,	20,	12,	18,	18,	25,	23,	11,	
       17,	17,	22,	21,	25,	30,	16,	20,	17,	16,	32,	21,	17]

F_2 = [12,	8,	22,	10,	10,	17,	16,	16,	15,	23,	18,	21,	16,	
       16,	11,	19,	16,	11,	28,	18,	10,	16,	21,	27,	22,	11,	
       16,	16,	20,	23,	25,	28,	15,	21,	18,	16,	33,	19,	17]


###### ----Step  1 : plot demand data
plt.plot(D_2)

# add trendline

z = np.polyfit(T_2, D_2, 1)
p = np.poly1d(z)
plt.plot(T_2, p(T_2))

#add forecast in plot
plt.plot(F_2)

###### ---- Step 2: compute forecast errors
df_2 = pd.DataFrame(data=D_2, columns=["D_2"])
df_2["F_2"] = F_2
df_2["E"] = df_2["F_2"] - df_2["D_2"]
df_2["T_2"] = T_2

###### ---- Step 3: create and plot histogram data for the errors
E_2 = list(df_2["E"])
obs = len(T_1)

hist_data_2 = [[i, E_2.count(i)] for i in set(E_2)]

df_2b = pd.DataFrame(data=hist_data_2, columns=["E", "frequency"])
df_2b["prob"] = df_2b["frequency"] / obs
df_2b.sort_values("E", inplace=True)
df_2b.plot(x="E", y="prob")
print(statistics.mean(df_2["E"]))

###### ----  step 4: Create demand prob distribution

forecasts_40 = 20       # mean of
df_2b["prob_demand"] = df_2b["E"] + forecasts_40     # error + mean

###################-----------Newsvendor--------------#################

D_3 = list(range(0,11))
Y = D_3
f_d = [0.01, 0.03, 0.05, 0.12, 0.15, 0.28, 0.15, 0.12, 0.05, 0.03, 0.01]
F_d = [0.01, 0.04, 0.09, 0.21, 0.36, 0.64, 0.79, 0.91, 0.96, 0.99, 1]
h = 10  # overage cost
b = 50  # shortage cost

df_3 = pd.DataFrame(data=D_3, columns=["D_3"])
df_3["f_d"] = f_d

#step 1: Plot the demand distribution
df_3.plot(x="D_3", y="f_d")

# step 2: compute expected shortages
df_y = pd.DataFrame(data=Y, columns=["Y"])
exp_shortages = []
for y in Y:
    shortage = [max(d-y, 0) for d in D_3]
    exp_sh = sum(shortage[i] * f_d[i] for i in D_3)
    exp_shortages.append(exp_sh)

df_3["exp_shortage"] = exp_shortages

# step 3: compute expected overage
exp_overage = []
for y in Y:
    overage = [max(y-d, 0) for d in D_3]
    exp_ov = sum(overage[i] * f_d[i] for i in D_3)
    exp_overage.append(exp_ov)

df_3["exp_overage"] = exp_overage

# step 4 compute cost C(y)
df_3["cost"] = df_3["exp_shortage"] * b + df_3["exp_overage"] * h
df_3.plot(x="D_3", y="cost")    # convex --> iterate to find min

###### compute optimal y with delta C
df_3["F_d"] = F_d
ratio = b/(h+b)
# check with F_d --> first that is greater than F_d

##### compute optimal with critical ratio

# check slides or nestor



