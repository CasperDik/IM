import numpy as np

def EOQ (D,c,alpha,K):
    return np.sqrt(2 * K * D / (alpha * c))

def C(Q,D,c,alpha,K):
    return Q * c * alpha / 2 + K * D / Q + D * c

def Qapplicable (Q,mn,mx):
    if Q <mn:
        return mn
    elif Q > mx:
        return mx
    return Q

def EOQ_incremental (v,D,c,alpha,K):
    return np.sqrt(2 * (K + v) * D / (alpha * c))

def C_incremental(v,Q,D,c,alpha,K):
    return alpha * v / 2 + alpha * c * Q/2 + (K + v) * D/ Q + c * D

def C02_emmisions(K_C02, c_C02, D, Q):
    return K_C02 * D/Q + c_C02*D

def C02_limit_Q(K_C02, c_C02, D):
    return (K_C02*D)/(3000-c_C02*D)

def EPQ(P, K, D, h):
    return np.sqrt((2*K*D)/(h*(1-D/P)))

def C_EPQ(h, D, P, Q, K):
    return (h*(1-D/P)) * Q/2 + K*D/Q + c*D

# holding cost and demand
# same for all suppliers
h = (1 + 0.004)**31 - 1
D = 1200


# supplier A
K = 11500
c = 29
K_C02 = 1000
c_C02 = 1

print("-"*30, "supplier A", "-"*30)
Q = EOQ(D, c, h, K)
print("EOQ of supplier A: ", Q)
Q_cost = min(2000, Q)
print("Order quantity of supplier A: ", Q_cost)
print("Average cost: ", C(Q_cost, D, c, h, K))
print("Average monthly C02 emissions: ", C02_emmisions(K_C02, c_C02, D, Q_cost))

# supplier B
K = 16000
c = 28
K_C02 = 2900
c_C02 = 1.9

print("\n", "-"*30, "supplier B", "-"*30)
Q = EOQ(D, c, h, K)
print("EOQ of supplier B: ", Q)
Q_cost = max(4500, Q)
print("Order quantity of supplier B: ", Q_cost)
print("Average cost: ", C(Q_cost, D, c, h, K))
print("Average monthly C02 emissions: ", C02_emmisions(K_C02, c_C02, D, Q_cost))
Q_new = C02_limit_Q(K_C02, c_C02, D)
print("New order quantity: ", Q_new)
print("Check new co2 emission: ", C02_emmisions(K_C02, c_C02, D, Q_new))
print("New average Cost: ", C(Q_new, D, c, h, K))

# supplier C
K = 11000
c0 = 33
c1 = c0 * 0.95
c2 = c0 * 0.9

Q1 = 3999
Q2 = 6499

K_C02 = 2600
c_C02 = 2

# STEP 1: COMPUTE EOQ

Qstar1 = EOQ(D,c0,h,K)
Qstar2 = EOQ(D,c1,h,K)
Qstar3 = EOQ(D,c2,h,K)

#STEP 2: IS QSTAR WITHIN THE ALLOWED RANGE?

Qapp1 = Qapplicable(Qstar1,0,Q1)
Qapp2 = Qapplicable(Qstar2,Q1 + 1,Q2)
Qapp3 = Qapplicable(Qstar3,Q2 + 1,999999)

#STEP 3: COMPUTE THE COST OF Q APPLICABLE

Capp1 = C(Qapp1,D,c0,h,K)
Capp2 = C(Qapp2,D,c1,h,K)
Capp3 = C(Qapp3,D,c2,h,K)

print("\n", "-"*30, "supplier C", "-"*30)
print(Capp1, Capp2, Capp3)
print("Order quantity of supplier C: ", Qapp2)
print("Average costs for supplier C: ", Capp2)
print("Average monthly C02 emissions: ", C02_emmisions(K_C02, c_C02, D, Qapp2))
Q_new = C02_limit_Q(K_C02, c_C02, D)
print("New order quantity: ", Q_new)
print("Check new co2 emission: ", C02_emmisions(K_C02, c_C02, D, Q_new))
print("New average Cost: ", C(Q_new, D, c, h, K))

# supplier D

# STEP 1: COMPUTE EOQ
K = 9500
c0 = 30
c1 = c0 * 0.95
c2 = c0 * 0.9

Q1 = 3999
Q2 = 6499

K_C02 = 2500
c_C02 = 1.8

v0 = 0
v1 = v0 + (c0 - c1) * Q1
v2 = v1 + (c1 - c2) * Q2

Qstar1 = EOQ_incremental (v0,D,c0,h,K)
Qstar2 = EOQ_incremental (v1,D,c1,h,K)
Qstar3 = EOQ_incremental (v2,D,c2,h,K)

#STEP 2: IS QSTAR WITHIN THE ALLOWED RANGE?

Qapp1 = Qapplicable (Qstar1,0,Q1)
Qapp2 = Qapplicable (Qstar2,Q1 + 1,Q2)
Qapp3 = Qapplicable (Qstar3,Q2 + 1,999999)

#STEP 3: COMPUTE THE COST OF Q APPLICABLE

Capp1 = C_incremental(v0,Qapp1,D,c0,h,K)
Capp2 = C_incremental(v1,Qapp2,D,c1,h,K)
Capp3 = C_incremental(v2,Qapp3,D,c2,h,K)

print("\n", "-"*30, "supplier D", "-"*30)
print(Capp1, Capp2,Capp3)
print("Order quantity of supplier D: ", Qapp1)
print("Average costs: ", Capp1)
print("Average monthly C02 emissions: ", C02_emmisions(K_C02, c_C02, D, Qapp1))
Q_new = C02_limit_Q(K_C02, c_C02, D)
print("New order quantity: ", Q_new)
print("Check new co2 emission: ", C02_emmisions(K_C02, c_C02, D, Q_new))
print("New average Cost: ", C(Q_new, D, c, h, K))

# supplier E
K = 15000
c = 29

K_C02 = 3000
c_C02 = 1.7

Q = EOQ(D,c,h,K)

print("\n", "-"*30, "supplier E", "-"*30)
print("EOQ of supplier E: ", Q)
print(C(Q//800*800, D, c, h, K), C(((Q//800)+1)*800, D, c, h, K))
print("Average cost: ", min(C(Q//800*800, D, c, h, K), C(((Q//800)+1)*800, D, c, h, K)))
print("Average monthly C02 emissions: ", C02_emmisions(K_C02, c_C02, D, Q))
Q_new = (C02_limit_Q(K_C02, c_C02, D)//800)*800
print("New order quantity: ", Q_new)
print("Check new co2 emission: ", C02_emmisions(K_C02, c_C02, D, Q_new))
Q_new = ((C02_limit_Q(K_C02, c_C02, D)//800)+1)*800
print("New order quantity: ", Q_new)
print("Check new co2 emission: ", C02_emmisions(K_C02, c_C02, D, Q_new))

print("New average Cost: ", C(Q_new, D, c, h, K))

# question 4
# EPQ
P = 1500
c = 35
K = 700
c_C02 = 3.6
max_prod_month = 1500

print("\n", "-"*30, "question 4 - EPQ", "-"*30)
Q = EPQ(P, K, D, h)
print("Optimal production quality: ", Q)
print("Average cost per month:", C_EPQ(h, D, P, Q, K))
print("Average monthly C02 emissions: ", (c_C02*Q)/(Q / max_prod_month))
Q_new = 3000/3.6
print("New production quantity: ", Q_new)
print("Check new co2 emission: ", c_C02*Q_new)

print("Production of optimal production quality exceeds carbon limits and maximum production quantity taking into "
      "account the carbon limit does not meet the demand. Thus production not better than sourcing from suppliers")
