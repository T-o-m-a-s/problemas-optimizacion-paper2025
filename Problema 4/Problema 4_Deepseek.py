from pulp import *

# Crear el problema de maximización
prob = LpProblem("Maximizar_beneficio_automotriz", LpMaximize)

# Definir variables de decisión
x = LpVariable("Automoviles", lowBound=12000, upBound=18000, cat='Integer')
y = LpVariable("Camiones", lowBound=8000, upBound=15000, cat='Integer')

# Función objetivo
prob += 15000*x + 12500*y, "Beneficio_total"

# Restricciones
prob += (1/25000)*x + (1/40000)*y <= 1, "Restriccion_estampado"
prob += (1/33333)*x + (1/16667)*y <= 1, "Restriccion_montaje_motores"
prob += x <= 22500, "Restriccion_linea_automoviles"
prob += y <= 15000, "Restriccion_linea_camiones"

# Resolver el problema
prob.solve()

# Imprimir resultados
print(f"Estado: {LpStatus[prob.status]}")
print(f"Automóviles a producir: {int(value(x))} unidades")
print(f"Camiones a producir: {int(value(y))} unidades")
print(f"Beneficio total máximo: ${value(prob.objective):,.2f}")

# Análisis de sensibilidad (precios sombra)
print("\nAnálisis de sensibilidad:")
for name, c in prob.constraints.items():
    print(f"{name}: Precio sombra = {c.pi}, Holgura = {c.slack}")