from gurobipy import Model, GRB, quicksum
import numpy as np
import pandas as pd
from itertools import product


def question_5(substances: list, D: dict, c: dict, M: dict, K, I0, T):
    # empty dict to store results
    output = {}

    # gurobi inputs
    T += 1
    big_M = 10000000000
    I = np.linspace(0, T-1, T, dtype=int)

    for substance in substances:
        m = Model("inventory system")

        # decision variables
        y = m.addVars(I, vtype=GRB.BINARY, name="y")
        Q = m.addVars(I, vtype=GRB.CONTINUOUS, name="Q", lb=0)
        I = m.addVars(I, vtype=GRB.CONTINUOUS, name="I", lb=0)

        # inventory level
        m.addConstr(I[0] == I0)
        m.addConstrs(I[n-1] + Q[n] - D[substance][n] == I[n] for n in range(1, T))

        # capacity constraint
        m.addConstrs(I[n-1] + Q[n] <= M[substance] for n in range(1, T))

        # big M
        m.addConstrs(Q[n] <= big_M * y[n] for n in range(1, T))

        # objective function
        m.setObjective(quicksum((K*y[n] + c[substance]*0.1*I[n]) for n in range(1, T)), GRB.MINIMIZE)
        m.optimize()

        # retrieve results
        print("Total cost of Inventory Policy of substance ", substance, " : %g" % m.objVal)

        # print results
        Q_output = []
        I_output = []

        for v in m.getVars():
            if v.varName[0] == "Q":
                Q_output.append(v.x)
            if v.varName[0] == "I":
                I_output.append(v.x)

        cost = np.where(np.array(Q_output) > 0.001, 1, 0) * K + c[substance] * 0.1 * np.array(I_output) + np.array(Q_output) * c[substance]

        output[substance] = {}
        output[substance]["Q"] = Q_output
        output[substance]["I"] = I_output
        output[substance]["Cost"] = cost
        m.write("model.lp")

    A_table = pd.DataFrame(output["A"])
    B_table = pd.DataFrame(output["B"])
    C_table = pd.DataFrame(output["C"])
    A_table.to_excel("data/Question_5_A_table.xlsx")
    B_table.to_excel("data/Question_5_B_table.xlsx")
    C_table.to_excel("data/Question_5_C_table.xlsx")

    print("-"*10, "Table for substance A", "-"*10)
    print(A_table.head(T))
    print("-"*10, "Table for substance B", "-"*10)
    print(B_table.head(T))
    print("-"*10, "Table for substance C", "-"*10)
    print(C_table.head(T))


def question_6(substances: list, D: dict, c: dict, M: dict, K, I0, T):
    # gurobi inputs
    T = T + 1
    i_n = list(product(range(len(substances)), range(T)))
    big_M = 10000000000

    m = Model("inventory system")

    # decision variables
    y = m.addVars(i_n, vtype=GRB.BINARY, name="y")
    Q = m.addVars(i_n, vtype=GRB.CONTINUOUS, name="Q", lb=0)
    I = m.addVars(i_n, vtype=GRB.CONTINUOUS, name="I", lb=0)

    # inventory constraints
    m.addConstrs(I[i, 0] == I0 for i in range(len(substances)))
    m.addConstrs(I[i, n - 1] + Q[i, n] - D[substances[i]][n] == I[i, n] for n in range(1, T) for i in
                 range(len(substances)))

    # Capacity constrains
    m.addConstrs(I[i, n - 1] + Q[i, n] <= M[substances[i]] for i in range(len(substances)) for n in range(1, T))

    # link y to Q
    m.addConstrs(Q[i, n] <= big_M * y[i, n] for i in range(len(substances)) for n in range(T))

    # only order one substance per period
    m.addConstrs(quicksum(y[i, n] for i in range(len(substances))) <= 1 for n in range(2, T))

    # objective function
    m.setObjective(quicksum(
        (K * y[i, n] + c[substances[i]] * 0.1 * I[i, n]) for n in range(T) for i in range(len(substances))),
                   GRB.MINIMIZE)
    m.optimize()

    for i in range(len(substances)):
        Q_output = []
        I_output = []
        for v in m.getVars():
            if v.varName[0] == "Q" and v.varName[2] == str(i):
                 Q_output.append(v.x)
            if v.varName[0] == "I" and v.varName[2] == str(i):
                 I_output.append(v.x)
        cost = np.where(np.array(Q_output) > 0.001, 1, 0) * K + list(c.values())[i] * 0.1 * np.array(I_output) + np.array(
            Q_output) * list(c.values())[i]

        output = pd.DataFrame({"Q[n]": Q_output,
                               "I[n]": I_output,
                               "cost": cost})

        output.to_excel("data/Question_6_" + "substance_" + substances[i] + ".xlsx")
        print("-" * 10, "Table for Substance ", substances[i],"-" * 10)
        print(output.head(T))

    print("Total cost of Inventory Policy: %g" % m.objVal)


def question_7(substances: list, D: dict, c: dict, M: dict, K, I0, T):
    # gurobi inputs
    T = T + 1
    i_n = list(product(range(len(substances)), range(T)))
    i_j = list(product(range(len(substances)), range(len(M))))
    big_M = 100000000

    m = Model("inventory system")

    # decision variables
    y = m.addVars(i_n, vtype=GRB.BINARY, name="y")
    Q = m.addVars(i_n, vtype=GRB.CONTINUOUS, name="Q", lb=0)
    I = m.addVars(i_n, vtype=GRB.CONTINUOUS, name="I", lb=0)
    X = m.addVars(i_j, vtype=GRB.BINARY, name="X")

    # inventory constraints
    m.addConstrs(I[i, 0] == I0 for i in range(len(substances)))
    m.addConstrs(I[i, n - 1] + Q[i, n] - D[substances[i]][n] == I[i, n] for n in range(1, T) for i in
                 range(len(substances)))

    # Capacity constrains
    m.addConstrs(X[i, j] * (I[i, n-1] + Q[i, n]) <= list(M.values())[j] for i in range(len(substances)) for n in range(1, T) for j in range(len(M)))

    # link y to Q
    m.addConstrs(Q[i, n] <= big_M * y[i, n] for i in range(len(substances)) for n in range(T))

    # max one tank per substance
    m.addConstrs(quicksum(X[i, j] for j in range(len(M))) == 1 for i in range(len(substances)))
    # max one substance per tank
    m.addConstrs(quicksum(X[i, j] for i in range(len(substances))) == 1 for j in range(len(M)))

    # objective function
    m.setObjective(quicksum(
        (K * y[i, n] + c[substances[i]] * 0.1 * I[i, n]) for n in range(T) for i in range(len(substances))),
                   GRB.MINIMIZE)
    m.optimize()

    for i in range(len(substances)):
        Q_output = []
        I_output = []
        for v in m.getVars():
            if v.varName[0] == "Q" and v.varName[2] == str(i):
                 Q_output.append(v.x)
            if v.varName[0] == "I" and v.varName[2] == str(i):
                 I_output.append(v.x)
        cost = np.where(np.array(Q_output) > 0.001, 1, 0) * K + list(c.values())[i] * 0.1 * np.array(I_output) + np.array(
            Q_output) * list(c.values())[i]

        output = pd.DataFrame({"Q[n]": Q_output,
                               "I[n]": I_output,
                               "cost": cost})

        output.to_excel("data/Question_7_" + "substance_" + substances[i] + ".xlsx")
        print("-" * 10, "Table for Substance ", substances[i],"-" * 10)
        print(output.head(T))

    print("\nTotal cost of Inventory Policy: %g" % m.objVal)

    for v in m.getVars():
        if v.varName[0] == "X" and v.x == 1:
            print("substance ", substances[int(v.varName[2])], "uses the tank with capacity: ", list(M.values())[int(v.varName[-2])])


def question_8_supplier_X(D, capacity, c, h, K, I0, T):
    # gurobi inputs
    T += 1
    big_M = 10000000000
    I = np.linspace(0, T-1, T, dtype=int)

    m = Model("inventory system")

    # decision variables
    y = m.addVars(I, vtype=GRB.BINARY, name="y")
    Q = m.addVars(I, vtype=GRB.CONTINUOUS, name="Q", lb=0)
    I = m.addVars(I, vtype=GRB.CONTINUOUS, name="I", lb=0)

    # inventory level
    m.addConstr(I[0] == I0)
    m.addConstr(I[1] == I0 + Q[1] - D[1])
    m.addConstrs(I[n] == Q[n-1] - D[n-1] + Q[n] - D[n] for n in range(2, T))

    # capacity constraint
    m.addConstrs(I[n - 1] + Q[n] <= capacity for n in range(1, T))

    # big M
    m.addConstrs(Q[n] <= big_M * y[n] for n in range(1, T))

    # objective function
    m.setObjective(quicksum((K * y[n] + h * I[n]) for n in range(1, T)), GRB.MINIMIZE)
    m.optimize()

    # retrieve results
    print("Total cost of Inventory Policy of substance D: %g" % m.objVal)

    # print results
    Q_output = []
    I_output = []

    for v in m.getVars():
        if v.varName[0] == "Q":
            Q_output.append(v.x)
        if v.varName[0] == "I":
            I_output.append(v.x)

    cost = np.where(np.array(Q_output) > 0.001, 1, 0) * K + h * np.array(I_output) + np.array(Q_output) * c


    Supplier_X = pd.DataFrame({"Q[n]": Q_output,
                               "I[n]": I_output,
                               "Cost": cost})
    Supplier_X.to_excel("data/Question_8_Supplier_X.xlsx")

    print("-"*10, "Table for Supplier X", "-"*10)
    print(Supplier_X.head(T))


def question_8_supplier_Y(D, capacity, c, h, K, I0, T):
    # gurobi inputs
    T += 1
    big_M = 10000000000
    I = np.linspace(0, T-1, T, dtype=int)

    m = Model("inventory system")

    # decision variables
    y = m.addVars(I, vtype=GRB.BINARY, name="y")
    Q = m.addVars(I, vtype=GRB.CONTINUOUS, name="Q", lb=0)
    I = m.addVars(I, vtype=GRB.CONTINUOUS, name="I", lb=0)

    # inventory level
    m.addConstr(I[0] == I0)
    m.addConstrs(I[n] == Q[n] - D[n] for n in range(1, T))

    # capacity constraint
    m.addConstrs(I[n - 1] + Q[n] <= capacity for n in range(1, T))

    # big M
    m.addConstrs(Q[n] <= big_M * y[n] for n in range(1, T))

    # objective function
    m.setObjective(quicksum((K * y[n] + h * I[n]) for n in range(1, T)), GRB.MINIMIZE)
    m.optimize()

    # retrieve results
    print("Total cost of Inventory Policy of substance D: %g" % m.objVal)

    # print results
    Q_output = []
    I_output = []

    for v in m.getVars():
        if v.varName[0] == "Q":
            Q_output.append(v.x)
        if v.varName[0] == "I":
            I_output.append(v.x)

    cost = np.where(np.array(Q_output) > 0.001, 1, 0) * K + h * np.array(I_output) + np.array(Q_output) * c


    Supplier_Y = pd.DataFrame({"Q[n]": Q_output,
                               "I[n]": I_output,
                               "Cost": cost})
    Supplier_Y.to_excel("data/Question_8_Supplier_Y.xlsx")

    print("-"*10, "Table for Supplier Y", "-"*10)
    print(Supplier_Y.head(T))


if __name__=="__main__":
    # inputs
    substances = ["A", "B", "C"]
    D_a = np.array([0, 60, 115, 90, 80, 110, 200, 40, 20])
    D = {"A": D_a, "B": D_a / 3, "C": D_a * 2}
    c = {"A": 5, "B": 8, "C": 7}
    M = {"A": 400, "B": 700, "C": 500}
    K = 200
    I0 = 0
    T = 8

    question_5(substances, D, c, M, K, I0, T)
    # question_6(substances, D, c, M, K, I0, T)
    # question_7(substances, D, c, M, K, I0, T)
    #
    # question_8_supplier_X(D=D_a, capacity=350, c=5, h=0.5, K=500, I0=I0, T=T)
    # question_8_supplier_Y(D=D_a, capacity=350, c=5, h=0.5, K=400, I0=I0, T=T)
