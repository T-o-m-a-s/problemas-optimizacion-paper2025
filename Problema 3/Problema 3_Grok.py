from pulp import LpProblem, LpMaximize, LpVariable, value

# Create the LP problem
prob = LpProblem("Whisky_Blending", LpMaximize)

# Decision variables (quantity of each liquor in each whisky)
x_AE = LpVariable("x_AE", lowBound=0)  # Liquor A in Escocés
x_BE = LpVariable("x_BE", lowBound=0)  # Liquor B in Escocés
x_CE = LpVariable("x_CE", lowBound=0)  # Liquor C in Escocés
x_AK = LpVariable("x_AK", lowBound=0)  # Liquor A in Kil
x_BK = LpVariable("x_BK", lowBound=0)  # Liquor B in Kil
x_CK = LpVariable("x_CK", lowBound=0)  # Liquor C in Kil
x_AT = LpVariable("x_AT", lowBound=0)  # Liquor A in Tartian
x_BT = LpVariable("x_BT", lowBound=0)  # Liquor B in Tartian
x_CT = LpVariable("x_CT", lowBound=0)  # Liquor C in Tartian

# Objective function: Maximize profit
# Revenue: 30 * (x_AE + x_BE + x_CE) + 25 * (x_AK + x_BK + x_CK) + 35 * (x_AT + x_BT + x_CT)
# Cost: 10 * (x_AE + x_AK + x_AT) + 15 * (x_BE + x_BK + x_BT) + 20 * (x_CE + x_CK + x_CT)
prob += (
    30 * (x_AE + x_BE + x_CE) + 25 * (x_AK + x_BK + x_CK) + 35 * (x_AT + x_BT + x_CT)
    - (10 * (x_AE + x_AK + x_AT) + 15 * (x_BE + x_BK + x_BT) + 20 * (x_CE + x_CK + x_CT))
)

# Availability constraints
prob += x_AE + x_AK + x_AT <= 1000, "Availability_A"
prob += x_BE + x_BK + x_BT <= 800, "Availability_B"
prob += x_CE + x_CK + x_CT <= 600, "Availability_C"

# Blending ratio constraints
# Escocés: 50% A, 30% B, 20% C
total_E = x_AE + x_BE + x_CE
prob += x_AE == 0.5 * total_E, "Ratio_A_Escoces"
prob += x_BE == 0.3 * total_E, "Ratio_B_Escoces"
prob += x_CE == 0.2 * total_E, "Ratio_C_Escoces"

# Kil: 40% A, 40% B, 20% C
total_K = x_AK + x_BK + x_CK
prob += x_AK == 0.4 * total_K, "Ratio_A_Kil"
prob += x_BK == 0.4 * total_K, "Ratio_B_Kil"
prob += x_CK == 0.2 * total_K, "Ratio_C_Kil"

# Tartian: 20% A, 20% B, 60% C
total_T = x_AT + x_BT + x_CT
prob += x_AT == 0.2 * total_T, "Ratio_A_Tartian"
prob += x_BT == 0.2 * total_T, "Ratio_B_Tartian"
prob += x_CT == 0.6 * total_T, "Ratio_C_Tartian"

# Solve the problem
prob.solve()

# Print results
print("Status:", prob.status)
print("Total Profit:", value(prob.objective))
print("\nEscocés:")
print(f"  Total Quantity: {value(x_AE + x_BE + x_CE):.2f}")
print(f"  Liquor A: {value(x_AE):.2f}")
print(f"  Liquor B: {value(x_BE):.2f}")
print(f"  Liquor C: {value(x_CE):.2f}")
print("\nKil:")
print(f"  Total Quantity: {value(x_AK + x_BK + x_CK):.2f}")
print(f"  Liquor A: {value(x_AK):.2f}")
print(f"  Liquor B: {value(x_BK):.2f}")
print(f"  Liquor C: {value(x_CK):.2f}")
print("\nTartian:")
print(f"  Total Quantity: {value(x_AT + x_BT + x_CT):.2f}")
print(f"  Liquor A: {value(x_AT):.2f}")
print(f"  Liquor B: {value(x_BT):.2f}")
print(f"  Liquor C: {value(x_CT):.2f}")