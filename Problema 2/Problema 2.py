import pulp

# Variables continuas no negativas
A1 = pulp.LpVariable('A1', lowBound=0, cat='Continuous')
A2 = pulp.LpVariable('A2', lowBound=0, cat='Continuous')
A3 = pulp.LpVariable('A3', lowBound=0, cat='Continuous')
B1 = pulp.LpVariable('B1', lowBound=0, cat='Continuous')
B2 = pulp.LpVariable('B2', lowBound=0, cat='Continuous')
B3 = pulp.LpVariable('B3', lowBound=0, cat='Continuous')
C1 = pulp.LpVariable('C1', lowBound=0, cat='Continuous')
C2 = pulp.LpVariable('C2', lowBound=0, cat='Continuous')
C3 = pulp.LpVariable('C3', lowBound=0, cat='Continuous')

# Variables binarias
IA = pulp.LpVariable('IA', cat='Binary')
IB = pulp.LpVariable('IB', cat='Binary')
IC = pulp.LpVariable('IC', cat='Binary')

# Definir el problema de minimización
prob = pulp.LpProblem("Problema_de_Minimizacion", pulp.LpMinimize)

# Funcional objetivo
prob += (
    4000 * IA + 3000 * IB + 2000 * IC +
    6 * A1 + 6 * A2 + 6 * A3 +
    5 * B1 + 5 * B2 + 5 * B3 +
    8 * C1 + 8 * C2 + 8 * C3
)

# Restricciones
prob += (A1 + B1 + C1 == 2500, "Demanda_1")
prob += (A2 + B2 + C2 == 1800, "Demanda_2")
prob += (A3 + B3 + C3 == 3500, "Demanda_3")

prob += (A1 <= 2300 * IA, "Cap_A1")
prob += (A2 <= 2300 * IA, "Cap_A2")
prob += (A3 <= 2300 * IA, "Cap_A3")
prob += (B1 <= 2000 * IB, "Cap_B1")
prob += (B2 <= 2000 * IB, "Cap_B2")
prob += (B3 <= 2000 * IB, "Cap_B3")
prob += (C1 <= 3300 * IC, "Cap_C1")
prob += (C2 <= 3300 * IC, "Cap_C2")
prob += (C3 <= 3300 * IC, "Cap_C3")

prob += (A1 >= 400 * IA, "Min_A1")
prob += (A2 >= 400 * IA, "Min_A2")
prob += (A3 >= 400 * IA, "Min_A3")
prob += (B1 >= 300 * IB, "Min_B1")
prob += (B2 >= 300 * IB, "Min_B2")
prob += (B3 >= 300 * IB, "Min_B3")
prob += (C1 >= 500 * IC, "Min_C1")
prob += (C2 >= 500 * IC, "Min_C2")
prob += (C3 >= 500 * IC, "Min_C3")

# Resolver el problema
prob.solve()

# Imprimir el valor del funcional objetivo
print("Valor óptimo de Z:", pulp.value(prob.objective))

# Imprimir el valor de todas las variables
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

