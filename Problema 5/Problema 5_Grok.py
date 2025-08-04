from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value

# Create the LP problem
prob = LpProblem("Refinery_Optimization", LpMaximize)

# Placeholder data (replace with actual data from the problem)
# Crude oil indices: 1 to 6
crudes = range(1, 7)
# Yields for distillation unit: {crude: (Virgin Naphtha, Virgin Diesel Oil, Heavy Gas Oil, Reduced Crude)}
yields_dist = {
    1: (0.2, 0.3, 0.4, 0.1),
    2: (0.25, 0.25, 0.35, 0.15),
    3: (0.3, 0.2, 0.3, 0.2),
    4: (0.15, 0.35, 0.35, 0.15),
    5: (0.2, 0.3, 0.3, 0.2),
    6: (0.25, 0.25, 0.3, 0.2)
}
# Yields for cracking unit: (Catalytic Naphtha, Catalytic Diesel Oil)
yields_crack_go = (0.6, 0.3)  # From Heavy Gas Oil
yields_crack_do = (0.5, 0.4)  # From Virgin Diesel Oil
# Costs and prices ($ per barrel)
crude_costs = {1: 50, 2: 55, 3: 60, 4: 52, 5: 58, 6: 54}  # Cost of crude
product_prices = {'Naphtha': 80, 'Diesel': 90, 'Fuel': 70}  # Selling prices
# Capacities (thousands of barrels per month)
dist_capacity = 1000  # Distillation unit
crack_capacity = 400  # Cracking unit
# Crude availability (thousands of barrels per month)
crude_availability = {1: 300, 2: 250, 3: 200, 4: 150, 5: 180, 6: 220}
# Product demands (thousands of barrels per month)
demands = {'Naphtha': 200, 'Diesel': 150, 'Fuel': 100}

# Variables
x = {i: LpVariable(f"x_{i}", lowBound=0, upBound=crude_availability[i]) for i in crudes}  # Crude processed
y_go = LpVariable("y_go", lowBound=0)  # Heavy Gas Oil to cracking
y_do = LpVariable("y_do", lowBound=0)  # Virgin Diesel Oil to cracking
z_np = LpVariable("z_np", lowBound=0)  # Naphtha produced
z_do = LpVariable("z_do", lowBound=0)  # Diesel Oil produced
z_fo = LpVariable("z_fo", lowBound=0)  # Fuel Oil produced
vn = LpVariable("vn", lowBound=0)  # Virgin Naphtha (not cracked)
vdo = LpVariable("vdo", lowBound=0)  # Virgin Diesel Oil (not cracked)
hgo = LpVariable("hgo", lowBound=0)  # Heavy Gas Oil (not cracked)
rc = LpVariable("rc", lowBound=0)  # Reduced Crude
cn = LpVariable("cn", lowBound=0)  # Catalytic Naphtha
cdo = LpVariable("cdo", lowBound=0)  # Catalytic Diesel Oil

# Objective function: Maximize profit
prob += (
    product_prices['Naphtha'] * z_np + product_prices['Diesel'] * z_do + product_prices['Fuel'] * z_fo -
    lpSum(crude_costs[i] * x[i] for i in crudes),
    "Total_Profit"
)

# Constraints
# Distillation unit capacity
prob += lpSum(x[i] for i in crudes) <= dist_capacity, "Distillation_Capacity"
# Cracking unit capacity
prob += y_go + y_do <= crack_capacity, "Cracking_Capacity"
# Material balances
prob += vn == lpSum(yields_dist[i][0] * x[i] for i in crudes), "Virgin_Naphtha_Balance"
prob += vdo + y_do == lpSum(yields_dist[i][1] * x[i] for i in crudes), "Virgin_Diesel_Balance"
prob += hgo + y_go == lpSum(yields_dist[i][2] * x[i] for i in crudes), "Heavy_Gas_Oil_Balance"
prob += rc == lpSum(yields_dist[i][3] * x[i] for i in crudes), "Reduced_Crude_Balance"
prob += cn == yields_crack_go[0] * y_go + yields_crack_do[0] * y_do, "Catalytic_Naphtha_Balance"
prob += cdo == yields_crack_go[1] * y_go + yields_crack_do[1] * y_do, "Catalytic_Diesel_Balance"
# Blending constraints
prob += z_np == vn + cn, "Naphtha_Blending"
prob += z_do == vdo + cdo, "Diesel_Blending"
prob += z_fo == rc + hgo, "Fuel_Blending"
# Demand constraints
prob += z_np >= demands['Naphtha'], "Naphtha_Demand"
prob += z_do >= demands['Diesel'], "Diesel_Demand"
prob += z_fo >= demands['Fuel'], "Fuel_Demand"

# Solve the problem
prob.solve()

# Print results
print("Status:", prob.status)
print("Optimal Profit:", value(prob.objective))
print("\nCrude Processed (thousands of barrels):")
for i in crudes:
    print(f"Crude {i}: {value(x[i]):.2f}")
print("\nCracking Inputs (thousands of barrels):")
print(f"Heavy Gas Oil: {value(y_go):.2f}")
print(f"Virgin Diesel Oil: {value(y_do):.2f}")
print("\nFinal Products (thousands of barrels):")
print(f"Naphtha: {value(z_np):.2f}")
print(f"Diesel Oil: {value(z_do):.2f}")
print(f"Fuel Oil: {value(z_fo):.2f}")