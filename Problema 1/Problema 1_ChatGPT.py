import pulp as pl

# Crear problema
prob = pl.LpProblem("Produccion_optima", pl.LpMaximize)

# ======================
# VARIABLES DE DECISIÓN
# ======================

# Cantidades absolutas (kg) de cada compuesto en cada alimento
qyA = pl.LpVariable("qyA", lowBound=0)
qvA = pl.LpVariable("qvA", lowBound=0)
qwA = pl.LpVariable("qwA", lowBound=0)

qyB = pl.LpVariable("qyB", lowBound=0)
qvB = pl.LpVariable("qvB", lowBound=0)
qwB = pl.LpVariable("qwB", lowBound=0)

# Producción total de A y B
xA = qyA + qvA + qwA
xB = qyB + qvB + qwB

# Ventas normales y excedentes
xA1 = pl.LpVariable("xA1", lowBound=0)
xA2 = pl.LpVariable("xA2", lowBound=0)
xB1 = pl.LpVariable("xB1", lowBound=0)
xB2 = pl.LpVariable("xB2", lowBound=0)

# Mano de obra
h_normal = pl.LpVariable("horas_normales", lowBound=0, upBound=150)
h_extra = pl.LpVariable("horas_extras", lowBound=0, upBound=30)

# ======================
# PARÁMETROS
# ======================

# Valores nutricionales por kg de compuesto (orden: Y, V, W)
energia = [3500, 3000, 5000]
fibra = [45, 60, 30]
grasas = [30, 25, 35]
saturadas = [0, 0, 4]
carbohidratos = [150, 130, 50]
hierro = [40, 70, 50]
calcio = [5.7, 3.3, 4.1]
vitaminas = [20, 30, 20]
colesterol = [0, 0, 12]
proteina = [130, 180, 100]

# Costo por kg
costos = {'y': 7, 'v': 9, 'w': 5}

# ======================
# RESTRICCIONES
# ======================

# RESTRICCIONES DE MEZCLA NUTRICIONAL PARA A

# Energía ≤ 3900 * xA
prob += 3500*qyA + 3000*qvA + 5000*qwA <= 3900 * xA

# Fibra ≥ 50 * xA
prob += 45*qyA + 60*qvA + 30*qwA >= 50 * xA

# Grasas ≤ 30 * xA
prob += 30*qyA + 25*qvA + 35*qwA <= 30 * xA

# Grasas saturadas ≤ 3 * xA
prob += 0*qyA + 0*qvA + 4*qwA <= 3 * xA

# Carbohidratos entre 70 y 130
prob += 150*qyA + 130*qvA + 50*qwA >= 70 * xA
prob += 150*qyA + 130*qvA + 50*qwA <= 130 * xA

# Hierro ≥ 45 * xA
prob += 40*qyA + 70*qvA + 50*qwA >= 45 * xA

# Calcio ≥ 3.7 * xA
prob += 5.7*qyA + 3.3*qvA + 4.1*qwA >= 3.7 * xA

# Vitaminas ≥ 22 * xA
prob += 20*qyA + 30*qvA + 20*qwA >= 22 * xA

# Colesterol ≤ 5 * xA
prob += 0*qyA + 0*qvA + 12*qwA <= 5 * xA

# Proteína ≥ 140 * xA
prob += 130*qyA + 180*qvA + 100*qwA >= 140 * xA

# RESTRICCIONES DE MEZCLA NUTRICIONAL PARA B

# Energía ≤ 4500 * xB
prob += 3500*qyB + 3000*qvB + 5000*qwB <= 4500 * xB

# Fibra ≥ 40 * xB
prob += 45*qyB + 60*qvB + 30*qwB >= 40 * xB

# Grasas ≤ 33 * xB
prob += 30*qyB + 25*qvB + 35*qwB <= 33 * xB

# Grasas saturadas ≤ 3 * xB
prob += 0*qyB + 0*qvB + 4*qwB <= 3 * xB

# Carbohidratos entre 80 y 140
prob += 150*qyB + 130*qvB + 50*qwB >= 80 * xB
prob += 150*qyB + 130*qvB + 50*qwB <= 140 * xB

# Hierro ≥ 45 * xB
prob += 40*qyB + 70*qvB + 50*qwB >= 45 * xB

# Calcio ≥ 3.5 * xB
prob += 5.7*qyB + 3.3*qvB + 4.1*qwB >= 3.5 * xB

# Vitaminas ≥ 22 * xB
prob += 20*qyB + 30*qvB + 20*qwB >= 22 * xB

# Colesterol ≤ 10 * xB
prob += 0*qyB + 0*qvB + 12*qwB <= 10 * xB

# Proteína ≥ 120 * xB
prob += 130*qyB + 180*qvB + 100*qwB >= 120 * xB

# VENTAS: normales y excedentes
prob += xA1 + xA2 == xA
prob += xA1 <= 150

prob += xB1 + xB2 == xB
prob += xB1 <= 200

# MANO DE OBRA
prob += h_normal + h_extra == 0.5 * xA + 0.4 * xB

# TIEMPO DE MÁQUINA (máx 24 hs)
t_uso = xA / 15 + xB / 20
prob += t_uso <= 24

# ======================
# FUNCIÓN OBJETIVO
# ======================

ingresos = (
    35 * xA1 + 28 * xA2 +
    30 * xB1 + 24 * xB2 +
    150 * (24 - t_uso)
)

costos = (
    qyA * 7 + qvA * 9 + qwA * 5 +
    qyB * 7 + qvB * 9 + qwB * 5 +
    100 * t_uso +
    5 * h_normal + 7 * h_extra
)

prob += ingresos - costos

# ======================
# RESOLUCIÓN
# ======================
prob.solve()
print("Estado:", pl.LpStatus[prob.status])
for v in prob.variables():
    if v.varValue > 0.001:
        print(f"{v.name}: {v.varValue:.2f}")
print(f"Ganancia máxima: ${pl.value(prob.objective):.2f}")
