from pulp import *

# Initialize the model
model = LpProblem("Food_Production_Optimization", LpMaximize)

# Decision variables
x_A = LpVariable("x_A", lowBound=0)  # kg of food A produced
x_B = LpVariable("x_B", lowBound=0)  # kg of food B produced
y_A = LpVariable("y_A", lowBound=0)  # kg of A sold at fixed price
z_A = LpVariable("z_A", lowBound=0)  # kg of A sold at excess price
y_B = LpVariable("y_B", lowBound=0)  # kg of B sold at fixed price
z_B = LpVariable("z_B", lowBound=0)  # kg of B sold at excess price
h = LpVariable("h", lowBound=0)      # extra labor hours

# Objective function
model += (
    55 * y_A + 28 * z_A + 30 * y_B + 24 * z_B
    - (100/15) * x_A - 5 * x_B
    - 1 * x_A - 2 * x_B
    - 2 * h,
    "Profit"
)

# Constraints
model += y_A + z_A == x_A, "Production_A"
model += y_B + z_B == x_B, "Production_B"
model += y_A <= 150, "Fixed_Demand_A"
model += y_B <= 200, "Fixed_Demand_B"
model += (x_A / 15) + (x_B / 20) <= 24, "Machine_Time"
model += 0.2 * x_A + 0.4 * x_B <= 150 + h, "Labor"
model += h <= 30, "Extra_Labor_Limit"

# Solve the problem
model.solve()

# Print results
print("Status:", LpStatus[model.status])
print(f"Food A produced: {x_A.varValue:.2f} kg")
print(f"Food B produced: {x_B.varValue:.2f} kg")
print(f"Food A sold at $55/kg: {y_A.varValue:.2f} kg")
print(f"Food A sold at $28/kg: {z_A.varValue:.2f} kg")
print(f"Food B sold at $30/kg: {y_B.varValue:.2f} kg")
print(f"Food B sold at $24/kg: {z_B.varValue:.2f} kg")
print(f"Extra labor hours: {h.varValue:.2f} hours")
print(f"Total profit: ${value(model.objective):.2f}")

# Calculate resource utilization
machine_time_A = x_A.varValue / 15 if x_A.varValue is not None else 0
machine_time_B = x_B.varValue / 20 if x_B.varValue is not None else 0
total_machine_time = machine_time_A + machine_time_B
labor_hours = 0.2 * x_A.varValue + 0.4 * x_B.varValue if x_A.varValue is not None and x_B.varValue is not None else 0

print(f"Machine time used: {total_machine_time:.2f} hours")
print(f"Labor hours used: {labor_hours:.2f} hours")