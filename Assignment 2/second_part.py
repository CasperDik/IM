import random
import pandas as pd
import numpy as np


def simulation_T_S(fixed_cycle_length, S):
    random.seed(1)

    # inputs
    mean_daily_demand = 10.44
    stdev_daily_demand = 4.28

    horizon = 3 * 365
    T = list(range(1, horizon + 1))
    D = {i: round(random.normalvariate(mean_daily_demand, stdev_daily_demand), 0) for i in T}

    D[0] = 0
    L = 14
    I0 = round(L * mean_daily_demand, 0)
    h = 1
    K = 900
    b = 5

    I = {0: I0}     # inventory
    I_pos = {0: I0}     # positive inventory
    I_neg = {0: 0}  # Backlog
    B = {0: 0}  # Backorders added to Backlog
    P = {0: I0}  # inv. position
    Q_ordered = {0: 0}  # order quantity
    Q_in = {i: 0 for i in range(0, L + 1)}  # arriving order quantity --> no initial pipeline

    for n in T:
        ### Define if a replenishment order is placed based on policy

        if n % fixed_cycle_length == 1:
            Q_ordered[n] = S - P[n - 1]
            if n + L <= horizon:
                Q_in[n + L] = S - P[n - 1]
        else:
            Q_ordered[n] = 0
            if n + L <= horizon:
                Q_in[n + L] = 0

        ### compute inventory level,inv. position and backorders

        I[n] = I[n - 1] + Q_in[n] - D[n]

        I_pos[n] = max(I[n], 0)

        I_neg[n] = max(- I[n], 0)

        B[n] = min(D[n], I_neg[n])

        P[n] = P[n - 1] + Q_ordered[n] - D[n]

    ### Create a data frame

    df_sim = pd.DataFrame(data={'Q_ordered': Q_ordered, 'Q_in': Q_in, 'I': I,
                                'I_pos': I_pos, 'I_neg': I_neg, 'B': B, 'P': P})

    # remove period 0 for KPi computation
    df_sim['D'] = D.values()
    df_sim = df_sim[1:horizon]

    #### compute KPIs
    KPIs = {}
    KPIs['E_I_pos'] = round(df_sim['I_pos'].mean(), 2)
    KPIs['E_I_neg'] = round(df_sim['I_neg'].mean(), 2)
    KPIs['E_B'] = round(df_sim['B'].mean(), 2)
    KPIs['E_D'] = round(df_sim['D'].mean(), 2)

    KPIs['P_Q_ordered'] = sum(df_sim['Q_ordered'] > 0) / horizon
    KPIs['P_B'] = sum(df_sim['B'] > 0) / horizon

    KPIs['cost'] = KPIs['E_I_pos'] * h + KPIs['E_I_neg'] * b + K * KPIs['P_Q_ordered']
    KPIs['alpha'] = 1 - KPIs['P_B']
    KPIs['beta'] = 1 - (KPIs['E_B'] / KPIs['E_D'])

    return df_sim, KPIs

def simulation_s_S(s, S, K):
    random.seed(1)

    # inputs
    mean_daily_demand = 10.44
    stdev_daily_demand = 4.28

    horizon = 3 * 365
    T = list(range(1, horizon + 1))
    D = {i: round(random.normalvariate(mean_daily_demand, stdev_daily_demand), 0) for i in T}

    D[0] = 0
    L = 14
    I0 = round(L * mean_daily_demand, 0)
    h = 1
    b = 5

    I = {0: I0}     # inventory
    I_pos = {0: I0}     # positive inventory
    I_neg = {0: 0}  # Backlog
    B = {0: 0}  # Backorders added to Backlog
    P = {0: I0}  # inv. position
    Q_ordered = {0: 0}  # order quantity
    Q_in = {i: 0 for i in range(0, L + 1)}  # arriving order quantity --> no initial pipeline

    for n in T:
        ### Define if a replenishment order is placed based on policy

        if P[n - 1] < s:
            Q_ordered[n] = S - P[n - 1]
            if n + L <= horizon:
                Q_in[n + L] = S - P[n - 1]
        else:
            Q_ordered[n] = 0
            if n + L <= horizon:
                Q_in[n + L] = 0

        ### compute inventory level,inv. position and backorders

        I[n] = I[n - 1] + Q_in[n] - D[n]

        I_pos[n] = max(I[n], 0)

        I_neg[n] = max(- I[n], 0)

        B[n] = min(D[n], I_neg[n])

        P[n] = P[n - 1] + Q_ordered[n] - D[n]

    ### Create a data frame

    df_sim = pd.DataFrame(data={'Q_ordered': Q_ordered, 'Q_in': Q_in, 'I': I,
                                'I_pos': I_pos, 'I_neg': I_neg, 'B': B, 'P': P})

    # remove period 0 for KPi computation
    df_sim['D'] = D.values()
    df_sim = df_sim[1:horizon]

    #### compute KPIs
    KPIs = {}
    KPIs['E_I_pos'] = round(df_sim['I_pos'].mean(), 2)
    KPIs['E_I_neg'] = round(df_sim['I_neg'].mean(), 2)
    KPIs['E_B'] = round(df_sim['B'].mean(), 2)
    KPIs['E_D'] = round(df_sim['D'].mean(), 2)

    KPIs['P_Q_ordered'] = sum(df_sim['Q_ordered'] > 0) / horizon
    KPIs['P_B'] = sum(df_sim['B'] > 0) / horizon

    KPIs['cost'] = KPIs['E_I_pos'] * h + KPIs['E_I_neg'] * b + K * KPIs['P_Q_ordered']
    KPIs['alpha'] = 1 - KPIs['P_B']
    KPIs['beta'] = 1 - (KPIs['E_B'] / KPIs['E_D'])

    return df_sim, KPIs

def question_6():
    # question 6 --> (T,S)
    # T = 21
    # optimal policy:
    results = {}
    S_range = range(200, 400)
    for S in S_range:
        df_sim, KPIs = simulation_T_S(fixed_cycle_length=21, S=S)
        results[(21, S)] = KPIs['cost']
    print('Best policy:', min(results, key=results.get), 'cost:', round(min(results.values()), 1))


def question_7():
    # question 7 --> (T,S)
    results = {}
    S_range = range(200, 400)
    T_range = range(1, 50)

    for S in S_range:
        for T in T_range:
            df_sim, KPIs = simulation_T_S(fixed_cycle_length=T, S=S)
            results[(T, S)] = KPIs['cost']
    print('Best policy:', min(results, key=results.get), 'cost:', round(min(results.values()), 1))

def question_8():
    # question 8 --> (s,S)
    results = {}
    S_range = range(200, 400)
    s_range = range(50, 250)

    for S in S_range:
        for s in s_range:
            df_sim, KPIs = simulation_s_S(s=s, S=S, K=900)
            results[(s, S)] = KPIs['cost']
    print('Best policy:', min(results, key=results.get), 'cost:', round(min(results.values()), 1))


def question_10():
    results = {}
    S_range = range(200, 400)
    s_range = range(50, 250)

    for S in S_range:
        for s in s_range:
            df_sim, KPIs = simulation_s_S(s=s, S=S, K=0)
            results[(s, S)] = KPIs['cost']
    print('Best policy:', min(results, key=results.get), 'cost:', round(min(results.values()), 1))

    # best policy with K=900:
    # (127, 280) with cost: 129.3
    # premium:
    premium = 129.3 - round(min(results.values()), 1)
    print(premium)

if __name__ == "__main__":
    question_6()
    question_7()
    question_8()
    question_10()

    # todo: questions
    # premium per order?