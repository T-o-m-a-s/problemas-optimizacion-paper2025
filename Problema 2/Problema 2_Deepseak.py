from pulp import *

# Crear el problema
prob = LpProblem("Problema_Generadores_Electricos", LpMinimize)

# Definir periodos y generadores
periodos = [1, 2, 3]
generadores = ['A', 'B', 'C']

# Costos y parámetros
costos_arranque = {'A': 4000, 'B': 3000, 'C': 2000}
costos_produccion = {'A': 6, 'B': 5, 'C': 8}
capacidad_max = {'A': 2300, 'B': 2000, 'C': 3300}
capacidad_min = {'A': 400, 'B': 300, 'C': 500}
demanda = {1: 2500, 2: 1800, 3: 3500}

# Variables de decisión
x = LpVariable.dicts("Encendido", 
                    [(gen, per) for gen in generadores for per in periodos],
                    cat='Binary')

produccion = LpVariable.dicts("Produccion",
                            [(gen, per) for gen in generadores for per in periodos],
                            lowBound=0)

# Variables auxiliares para costos de arranque
arranque = LpVariable.dicts("Arranque",
                           [(gen, per) for gen in generadores for per in periodos],
                           cat='Binary')

# Función objetivo
prob += lpSum(costos_arranque[gen] * arranque[gen, per] for gen in generadores for per in periodos) + \
        lpSum(costos_produccion[gen] * produccion[gen, t] for gen in generadores for t in periodos)

# Restricciones de demanda
for t in periodos:
    prob += lpSum(produccion[gen, t] for gen in generadores) == demanda[t]

# Restricciones de capacidad y mínimos operativos
for gen in generadores:
    for t in periodos:
        prob += produccion[gen, t] >= capacidad_min[gen] * x[gen, t]
        prob += produccion[gen, t] <= capacidad_max[gen] * x[gen, t]

# Restricciones de consistencia de encendido
for gen in generadores:
    prob += x[gen, 1] >= x[gen, 2]
    prob += x[gen, 2] >= x[gen, 3]

# Restricciones para variables de arranque
for gen in generadores:
    # Primer periodo: arranque si está encendido
    prob += arranque[gen, 1] == x[gen, 1]
    
    # Periodos siguientes: arranque si está encendido ahora pero no antes
    prob += arranque[gen, 2] >= x[gen, 2] - x[gen, 1]
    prob += arranque[gen, 3] >= x[gen, 3] - x[gen, 2]
    
    # Las variables de arranque son binarias (0 o 1)
    prob += arranque[gen, 2] <= 1
    prob += arranque[gen, 3] <= 1

# Resolver el problema
prob.solve()

# Mostrar resultados
print("Estado:", LpStatus[prob.status])
print("Costo Total = $", value(prob.objective))

print("\nPlan de encendido:")
for t in periodos:
    print(f"\nPeriodo {t}:")
    for gen in generadores:
        if value(x[gen, t]) == 1:
            print(f"  Generador {gen}: Producción = {value(produccion[gen, t]):.1f} MW")
        else:
            print(f"  Generador {gen}: Apagado")

print("\nCostos de arranque por generador:")
for gen in generadores:
    total_arranques = sum(value(arranque[gen, per]) for per in periodos)
    if total_arranques > 0:
        print(f"  Generador {gen}: {int(total_arranques)} arranque(s) = ${costos_arranque[gen] * total_arranques}")

print("\nCostos de producción por generador:")
for gen in generadores:
    total_prod = sum(value(produccion[gen, per]) for per in periodos)
    if total_prod > 0:
        print(f"  Generador {gen}: {total_prod:.1f} MW = ${costos_produccion[gen] * total_prod:.2f}")