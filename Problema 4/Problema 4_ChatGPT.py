
import pulp

# Definir el problema
model = pulp.LpProblem("Produccion_Automoviles_Camiones", pulp.LpMaximize)

# Variables
x = pulp.LpVariable('Automoviles', lowBound=0)
y = pulp.LpVariable('Camiones', lowBound=0)

# Función objetivo
model += 15000 * x + 12500 * y, "Beneficio_Total"

# Restricciones
model += (x / 25000) + (y / 40000) <= 1, "Estampado"
model += (x / 33333) + (y / 16667) <= 1, "Montaje_Motores"
model += x <= 22500, "Linea_Automoviles"
model += y <= 15000, "Linea_Camiones"
model += x >= 12000, "Demanda_Min_Autos"
model += x <= 18000, "Demanda_Max_Autos"
model += y >= 8000, "Demanda_Min_Camiones"

# Resolver
model.solve()

# Mostrar resultados
print(f"Estado de la solución: {pulp.LpStatus[model.status]}")
print(f"Automóviles a producir: {x.varValue:.0f}")
print(f"Camiones a producir: {y.varValue:.0f}")
print(f"Beneficio total: ${pulp.value(model.objective):,.2f}")
