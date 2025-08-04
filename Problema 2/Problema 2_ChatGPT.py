import pulp

# Crear el problema
prob = pulp.LpProblem("Generacion_Electrica", pulp.LpMinimize)

# Variables continuas: cantidad de MW que genera cada generador en cada periodo
x_A1 = pulp.LpVariable("x_A1", lowBound=0)
x_A2 = pulp.LpVariable("x_A2", lowBound=0)
x_A3 = pulp.LpVariable("x_A3", lowBound=0)

x_B1 = pulp.LpVariable("x_B1", lowBound=0)
x_B2 = pulp.LpVariable("x_B2", lowBound=0)
x_B3 = pulp.LpVariable("x_B3", lowBound=0)

x_C1 = pulp.LpVariable("x_C1", lowBound=0)
x_C2 = pulp.LpVariable("x_C2", lowBound=0)
x_C3 = pulp.LpVariable("x_C3", lowBound=0)

# Variables binarias: si el generador está funcionando en un periodo
y_A1 = pulp.LpVariable("y_A1", cat='Binary')
y_A2 = pulp.LpVariable("y_A2", cat='Binary')
y_A3 = pulp.LpVariable("y_A3", cat='Binary')

y_B1 = pulp.LpVariable("y_B1", cat='Binary')
y_B2 = pulp.LpVariable("y_B2", cat='Binary')
y_B3 = pulp.LpVariable("y_B3", cat='Binary')

y_C1 = pulp.LpVariable("y_C1", cat='Binary')
y_C2 = pulp.LpVariable("y_C2", cat='Binary')
y_C3 = pulp.LpVariable("y_C3", cat='Binary')

# Variables binarias: si el generador se arrancó en algún momento
z_A = pulp.LpVariable("z_A", cat='Binary')
z_B = pulp.LpVariable("z_B", cat='Binary')
z_C = pulp.LpVariable("z_C", cat='Binary')

# -------- FUNCIÓN OBJETIVO --------
prob += (
    4000 * z_A + 3000 * z_B + 2000 * z_C +  # Costos de arranque
    6 * (x_A1 + x_A2 + x_A3) +
    5 * (x_B1 + x_B2 + x_B3) +
    8 * (x_C1 + x_C2 + x_C3)
)

# -------- RESTRICCIONES --------

# Demanda por período
prob += x_A1 + x_B1 + x_C1 == 2500, "Demanda_P1"
prob += x_A2 + x_B2 + x_C2 == 1800, "Demanda_P2"
prob += x_A3 + x_B3 + x_C3 == 3500, "Demanda_P3"

# Capacidad máxima por generador y período
prob += x_A1 <= 2300 * y_A1
prob += x_A2 <= 2300 * y_A2
prob += x_A3 <= 2300 * y_A3

prob += x_B1 <= 2000 * y_B1
prob += x_B2 <= 2000 * y_B2
prob += x_B3 <= 2000 * y_B3

prob += x_C1 <= 3300 * y_C1
prob += x_C2 <= 3300 * y_C2
prob += x_C3 <= 3300 * y_C3

# Mínimo requerido si está encendido
prob += x_A1 >= 400 * y_A1
prob += x_A2 >= 400 * y_A2
prob += x_A3 >= 400 * y_A3

prob += x_B1 >= 300 * y_B1
prob += x_B2 >= 300 * y_B2
prob += x_B3 >= 300 * y_B3

prob += x_C1 >= 500 * y_C1
prob += x_C2 >= 500 * y_C2
prob += x_C3 >= 500 * y_C3

# Arranque si se usó en algún periodo
prob += z_A >= y_A1
prob += z_A >= y_A2
prob += z_A >= y_A3

prob += z_B >= y_B1
prob += z_B >= y_B2
prob += z_B >= y_B3

prob += z_C >= y_C1
prob += z_C >= y_C2
prob += z_C >= y_C3

# -------- RESOLVER --------
prob.solve()

# -------- RESULTADOS --------
print(f"Estado: {pulp.LpStatus[prob.status]}")
print(f"Costo total: ${pulp.value(prob.objective):,.2f}")

# Mostrar resultados
for var in prob.variables():
    print(f"{var.name}: {var.varValue}")
