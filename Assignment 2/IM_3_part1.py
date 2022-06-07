import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
from scipy.stats import norm

# Demand distribution
T_1 = list(range(1,25))

D_1 = [216,	225, 249, 224, 217, 206, 237, 221, 199, 233, 194, 181, 
       247, 184, 262, 216, 217, 219, 241, 197, 229, 213, 225, 211]

# Step 1 : plot demand data
plt.plot(D_1)
plt.title('Demand')
plt.xlabel('Collection interval')
plt.ylabel('Accumulated demand')
plt.show()

"""Explanation:

Question 2
"""

mean = np.mean(D_1)
stdev = np.std(D_1)

print('The mean is:', mean)
print('The standard deviation is:', stdev)

"""Question 3"""

hist_dat = [[i,D_1.count(i)] for i in set(D_1)]
df_1 = pd.DataFrame(data = hist_dat, columns = ['D', 'frequency'])
df_1.sort_values(by=["D"], inplace=True)
df_1.plot(x = 'D', y = 'frequency', kind = 'bar')
plt.show()

# step 3: transform frequency into empirical probability dist
obs = len(T_1)
df_1 ['prob'] = df_1['frequency']/obs
df_1.plot (x = 'D', y = 'prob', kind = 'bar')
plt.show()

sum(df_1 ['prob'])

"""Comment:

Question 4
"""

df_1["cum"] = df_1["prob"].cumsum()
plt.plot(df_1["D"], df_1["cum"])
plt.show()

# part 2 question 4

# Plot the histogram.
plt.hist(D_1, bins=10, density=True)

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mean, stdev)
plt.plot(x, p, 'k', linewidth=2)

plt.show()

"""
Question 5
"""
collection_period = 21

mean_daily_demand = mean/collection_period
stdev_daily_demand = stdev/np.sqrt(collection_period)
print('The daily mean is:', mean_daily_demand)
print('The daily standard deviation is:', stdev_daily_demand)
