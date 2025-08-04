from pulp import LpMaximize, LpProblem, LpVariable

# Create the linear programming problem
prob = LpProblem("Automotive_Production", LpMaximize)

# Define decision variables
x = LpVariable("Cars", lowBound=0, cat="Continuous")  # Number of cars
y = LpVariable("Trucks", lowBound=0, cat="Continuous")  # Number of trucks

# Objective function: Maximize profit
prob += 15000 * x + 12500 * y, "Total_Profit"

# Constraints
# Stamping department
prob += 0.00004 * x + 0.000025 * y <= 1, "Stamping_Capacity"

# Engine assembly department
prob += 0.00003 * x + 0.00006 * y <= 1, "Engine_Assembly_Capacity"

# Car assembly line
prob += x <= 25000, "Car_Assembly_Capacity"

# Truck assembly line
prob += y <= 15000, "Truck_Assembly_Capacity"

# Minimum production requirements
prob += x >= 12000, "Min_Cars"
prob += y >= 8000, "Min_Trucks"

# Maximum demand for cars
prob += x <= 15000, "Max_Cars_Demand"

# Solve the problem
prob.solve()

# Output results
print("Status:", prob.status)
print("Optimal number of cars:", x.varValue)
print("Optimal number of trucks:", y.varValue)
print("Maximum profit ($):", prob.objective.value())