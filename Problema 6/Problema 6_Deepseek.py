from pulp import LpProblem, LpVariable, LpMinimize, LpStatus, value

# Crear el problema de minimización
prob = LpProblem("Minimizar_Potencia_Total", LpMinimize)

# Definir las variables de decisión (voltajes V1 a V6)
V1 = LpVariable("V1", lowBound=2, upBound=10)
V2 = LpVariable("V2", lowBound=2, upBound=10)
V3 = LpVariable("V3", lowBound=2, upBound=10)
V4 = LpVariable("V4", lowBound=2, upBound=10)
V5 = LpVariable("V5", lowBound=2, upBound=10)
V6 = LpVariable("V6", lowBound=2, upBound=10)

# Definir la función objetivo (potencia total)
prob += 4 * V1 + 6 * V2 + 8 * V3 + 18 * V4 + 10 * V5 + 8 * V6, "Potencia_Total"

# Resolver el problema
prob.solve()

# Imprimir el estado de la solución
print("Estado:", LpStatus[prob.status])

# Imprimir los valores óptimos de las variables
print("Valores óptimos:")
print(f"V1 = {value(V1)} volts")
print(f"V2 = {value(V2)} volts")
print(f"V3 = {value(V3)} volts")
print(f"V4 = {value(V4)} volts")
print(f"V5 = {value(V5)} volts")
print(f"V6 = {value(V6)} volts")

# Imprimir la potencia total mínima
print(f"Potencia total mínima: {value(prob.objective)} watts")