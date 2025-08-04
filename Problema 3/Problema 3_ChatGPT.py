
import pulp

# Crear el modelo
model = pulp.LpProblem("Mezcla_de_Whisky", pulp.LpMaximize)

# Variables
tipos = ['A', 'B', 'C']
marcas = ['E', 'K', 'T']  # Escocés, Kilt, Tartan
x = pulp.LpVariable.dicts("x", [(t, m) for t in tipos for m in marcas], lowBound=0)

# Precios de venta por marca
precio_venta = {'E': 6.8, 'K': 5.7, 'T': 4.5}

# Costos por tipo
costo = {'A': 7, 'B': 5, 'C': 4}

# Objetivo: maximizar beneficio
ingresos = pulp.lpSum(precio_venta[m] * pulp.lpSum(x[t, m] for t in tipos) for m in marcas)
costos = pulp.lpSum(costo[t] * pulp.lpSum(x[t, m] for m in marcas) for t in tipos)
model += ingresos - costos

# Restricciones de disponibilidad
model += pulp.lpSum(x['A', m] for m in marcas) <= 2000
model += pulp.lpSum(x['B', m] for m in marcas) <= 2500
model += pulp.lpSum(x['C', m] for m in marcas) <= 1200

# Restricciones de composición

# Escocés
model += 0.4 * x['A', 'E'] - 0.6 * x['B', 'E'] - 0.6 * x['C', 'E'] >= 0
model += -0.2 * x['A', 'E'] - 0.2 * x['B', 'E'] + 0.8 * x['C', 'E'] <= 0

# Kilt
model += 0.85 * x['A', 'K'] - 0.15 * x['B', 'K'] - 0.15 * x['C', 'K'] >= 0
model += -0.6 * x['A', 'K'] - 0.6 * x['B', 'K'] + 0.4 * x['C', 'K'] <= 0

# Tartan
model += -0.5 * x['A', 'T'] - 0.5 * x['B', 'T'] + 0.5 * x['C', 'T'] <= 0

# Resolver
model.solve()

# Mostrar resultados
print(f"Estado de la solución: {pulp.LpStatus[model.status]}")
print(f"Beneficio máximo: ${pulp.value(model.objective):.2f}")
for t in tipos:
    for m in marcas:
        cantidad = x[t, m].varValue
        if cantidad > 0:
            print(f"{t} en {m}: {cantidad:.2f} L")
