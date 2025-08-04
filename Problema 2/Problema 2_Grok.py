from pulp import *

# Initialize the linear programming model
model = LpProblem("Generator_Scheduling_Hardcoded", LpMinimize)

# Parameters (as defined in the problem)
# Demands for each period (MW)
D1 = 2500  # Period 1
D2 = 1500  # Period 2
D3 = 3500  # Period 3

# Minimum capacities for each generator (MW)
M_A = 400  # Generator A
M_B = 300  # Generator B
M_C = 500  # Generator C

# Startup costs for each generator ($)
S_A = 1000  # Generator A
S_B = 800   # Generator B
S_C = 1200  # Generator C

# Operational costs for each generator ($/MW)
C_A = 50  # Generator A
C_B = 60  # Generator B
C_C = 40  # Generator C

# Maximum capacity (assumed high to avoid limiting solutions)
MAX_CAP = 5000

# Decision Variables
# Power output (x_it) in MW for each generator in each period (continuous)
x_A1 = LpVariable("Power_A_1", lowBound=0, cat="Continuous")
x_A2 = LpVariable("Power_A_2", lowBound=0, cat="Continuous")
x_A3 = LpVariable("Power_A_3", lowBound=0, cat="Continuous")
x_B1 = LpVariable("Power_B_1", lowBound=0, cat="Continuous")
x_B2 = LpVariable("Power_B_2", lowBound=0, cat="Continuous")
x_B3 = LpVariable("Power_B_3", lowBound=0, cat="Continuous")
x_C1 = LpVariable("Power_C_1", lowBound=0, cat="Continuous")
x_C2 = LpVariable("Power_C_2", lowBound=0, cat="Continuous")
x_C3 = LpVariable("Power_C_3", lowBound=0, cat="Continuous")

# Startup decisions (y_it): 1 if generator starts in period t, 0 otherwise (binary)
y_A1 = LpVariable("Startup_A_1", cat="Binary")
y_A2 = LpVariable("Startup_A_2", cat="Binary")
y_A3 = LpVariable("Startup_A_3", cat="Binary")
y_B1 = LpVariable("Startup_B_1", cat="Binary")
y_B2 = LpVariable("Startup_B_2", cat="Binary")
y_B3 = LpVariable("Startup_B_3", cat="Binary")
y_C1 = LpVariable("Startup_C_1", cat="Binary")
y_C2 = LpVariable("Startup_C_2", cat="Binary")
y_C3 = LpVariable("Startup_C_3", cat="Binary")

# Operating status (z_it): 1 if generator is operating in period t, 0 otherwise (binary)
z_A1 = LpVariable("Operating_A_1", cat="Binary")
z_A2 = LpVariable("Operating_A_2", cat="Binary")
z_A3 = LpVariable("Operating_A_3", cat="Binary")
z_B1 = LpVariable("Operating_B_1", cat="Binary")
z_B2 = LpVariable("Operating_B_2", cat="Binary")
z_B3 = LpVariable("Operating_B_3", cat="Binary")
z_C1 = LpVariable("Operating_C_1", cat="Binary")
z_C2 = LpVariable("Operating_C_2", cat="Binary")
z_C3 = LpVariable("Operating_C_3", cat="Binary")

# Objective Function: Minimize total cost (startup + operational)
model += (
    # Startup costs
    S_A * y_A1 + S_A * y_A2 + S_A * y_A3 +
    S_B * y_B1 + S_B * y_B2 + S_B * y_B3 +
    S_C * y_C1 + S_C * y_C2 + S_C * y_C3 +
    # Operational costs
    C_A * x_A1 + C_A * x_A2 + C_A * x_A3 +
    C_B * x_B1 + C_B * x_B2 + C_B * x_B3 +
    C_C * x_C1 + C_C * x_C2 + C_C * x_C3
), "Total_Cost"

# Constraints
# 1. Demand Satisfaction: Total power output must meet or exceed demand in each period
model += x_A1 + x_B1 + x_C1 >= D1, "Demand_Period_1"
model += x_A2 + x_B2 + x_C2 >= D2, "Demand_Period_2"
model += x_A3 + x_B3 + x_C3 >= D3, "Demand_Period_3"

# 2. Minimum Capacity: If a generator is operating (z_it = 1), it must produce at least its minimum capacity
model += x_A1 >= M_A * z_A1, "Min_Capacity_A_1"
model += x_A2 >= M_A * z_A2, "Min_Capacity_A_2"
model += x_A3 >= M_A * z_A3, "Min_Capacity_A_3"
model += x_B1 >= M_B * z_B1, "Min_Capacity_B_1"
model += x_B2 >= M_B * z_B2, "Min_Capacity_B_2"
model += x_B3 >= M_B * z_B3, "Min_Capacity_B_3"
model += x_C1 >= M_C * z_C1, "Min_Capacity_C_1"
model += x_C2 >= M_C * z_C2, "Min_Capacity_C_2"
model += x_C3 >= M_C * z_C3, "Min_Capacity_C_3"

# 3. Maximum Capacity: If a generator is operating, its output cannot exceed the maximum capacity
model += x_A1 <= MAX_CAP * z_A1, "Max_Capacity_A_1"
model += x_A2 <= MAX_CAP * z_A2, "Max_Capacity_A_2"
model += x_A3 <= MAX_CAP * z_A3, "Max_Capacity_A_3"
model += x_B1 <= MAX_CAP * z_B1, "Max_Capacity_B_1"
model += x_B2 <= MAX_CAP * z_B2, "Max_Capacity_B_2"
model += x_B3 <= MAX_CAP * z_B3, "Max_Capacity_B_3"
model += x_C1 <= MAX_CAP * z_C1, "Max_Capacity_C_1"
model += x_C2 <= MAX_CAP * z_C2, "Max_Capacity_C_2"
model += x_C3 <= MAX_CAP * z_C3, "Max_Capacity_C_3"

# 4. Operating Status: A generator is operating if it starts in the current period
model += z_A1 >= y_A1, "Start_Implies_Operating_A_1"
model += z_A2 >= y_A2, "Start_Implies_Operating_A_2"
model += z_A3 >= y_A3, "Start_Implies_Operating_A_3"
model += z_B1 >= y_B1, "Start_Implies_Operating_B_1"
model += z_B2 >= y_B2, "Start_Implies_Operating_B_2"
model += z_B3 >= y_B3, "Start_Implies_Operating_B_3"
model += z_C1 >= y_C1, "Start_Implies_Operating_C_1"
model += z_C2 >= y_C2, "Start_Implies_Operating_C_2"
model += z_C3 >= y_C3, "Start_Implies_Operating_C_3"

# 5. Operating Status: A generator operates in period t if it was started in any period k <= t
model += z_A1 <= y_A1, "Operating_Requires_Start_A_1"
model += z_A2 <= y_A1 + y_A2, "Operating_Requires_Start_A_2"
model += z_A3 <= y_A1 + y_A2 + y_A3, "Operating_Requires_Start_A_3"
model += z_B1 <= y_B1, "Operating_Requires_Start_B_1"
model += z_B2 <= y_B1 + y_B2, "Operating_Requires_Start_B_2"
model += z_B3 <= y_B1 + y_B2 + y_B3, "Operating_Requires_Start_B_3"
model += z_C1 <= y_C1, "Operating_Requires_Start_C_1"
model += z_C2 <= y_C1 + y_C2, "Operating_Requires_Start_C_2"
model += z_C3 <= y_C1 + y_C2 + y_C3, "Operating_Requires_Start_C_3"

# Solve the model
model.solve()

# Output results
print("Status:", LpStatus[model.status])
print("Total Cost: $", round(value(model.objective), 2))
print("\nGenerator Schedule:")
print("Period 1 (Demand: 2500 MW):")
for gen, x, y, z in [("A", x_A1, y_A1, z_A1), ("B", x_B1, y_B1, z_B1), ("C", x_C1, y_C1, z_C1)]:
    if value(z) > 0.5:
        print(f"  Generator {gen}: {round(value(x), 2)} MW (Operating)")
        if value(y) > 0.5:
            print(f"    Started in Period 1")
print("Period 2 (Demand: 1500 MW):")
for gen, x, y, z in [("A", x_A2, y_A2, z_A2), ("B", x_B2, y_B2, z_B2), ("C", x_C2, y_C2, z_C2)]:
    if value(z) > 0.5:
        print(f"  Generator {gen}: {round(value(x), 2)} MW (Operating)")
        if value(y) > 0.5:
            print(f"    Started in Period 2")
print("Period 3 (Demand: 3500 MW):")
for gen, x, y, z in [("A", x_A3, y_A3, z_A3), ("B", x_B3, y_B3, z_B3), ("C", x_C3, y_C3, z_C3)]:
    if value(z) > 0.5:
        print(f"  Generator {gen}: {round(value(x), 2)} MW (Operating)")
        if value(y) > 0.5:
            print(f"    Started in Period 3")