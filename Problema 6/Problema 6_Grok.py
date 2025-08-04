from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

# Crear el problema de optimización
prob = LpProblem("Minimize_Power", LpMinimize)

# Definir las variables de decisión (V_i: voltajes)
V = [LpVariable(f"V{i+1}", lowBound=2, upBound=10) for i in range(6)]

# Corrientes dadas
I = [4, 6, 8, 18, 10, 6]

# Función objetivo: minimizar la potencia total
prob += lpSum(I[i] * V[i] for i in range(6)), "Total_Power"

# Resolver el problema
prob.solve()

# Imprimir resultados
print("Estado de la solución:", prob.status)
print("Potencia total mínima:", value(prob.objective), "watts")
for i in range(6):
    print(f"V{i+1} = {value(V[i]):.2f} volts")