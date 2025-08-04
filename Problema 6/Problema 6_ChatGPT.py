

import pulp

# Crear el problema
model = pulp.LpProblem("Minimizar_Potencia_Total", pulp.LpMinimize)

# Variables de decisión: caídas de tensión
V = [pulp.LpVariable(f"V{i+1}", lowBound=2, upBound=10) for i in range(6)]

# Coeficientes de corriente
I = [4, 6, 8, 18, 10, 8]

# Función objetivo: minimizar la suma de I[i] * V[i]
model += pulp.lpSum([I[i] * V[i] for i in range(6)]), "Potencia_Total"

# Resolver el problema
model.solve()

# Resultados
print("Estado:", pulp.LpStatus[model.status])
for i in range(6):
    print(f"V{i+1} = {V[i].varValue:.2f} V")
print(f"Potencia total disipada: {pulp.value(model.objective):.2f} W")
