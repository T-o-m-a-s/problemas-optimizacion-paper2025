import pulp

# Declarar variables continuas no negativas
R1 = pulp.LpVariable('R1', lowBound=0, cat='Continuous')
R2 = pulp.LpVariable('R2', lowBound=0, cat='Continuous')
R3 = pulp.LpVariable('R3', lowBound=0, cat='Continuous')
R4 = pulp.LpVariable('R4', lowBound=0, cat='Continuous')
R5 = pulp.LpVariable('R5', lowBound=0, cat='Continuous')
R6 = pulp.LpVariable('R6', lowBound=0, cat='Continuous')
VA = pulp.LpVariable('VA', lowBound=0, cat='Continuous')
V4 = pulp.LpVariable('V4', lowBound=0, cat='Continuous')
VB = pulp.LpVariable('VB', lowBound=0, cat='Continuous')

# Definir el problema de minimización
problema = pulp.LpProblem("Problema_6", pulp.LpMinimize)

# Funcional objetivo
problema += (16 * R1 + 36 * R2 + 64 * R3 + 324 * R4 + 100 * R5 + 64 * R6),"Funcional_objetivo"

# Restricciones
problema += (VA == 4 * R1), "Restriccion_1"
problema += (VA == 6 * R2), "Restriccion_2"
problema += (VA == 8 * R3), "Restriccion_3"
problema += (V4 == 18 * R4), "Restriccion_4"
problema += (VB == 10 * R5), "Restriccion_5"
problema += (VB == 8 * R6), "Restriccion_6"
problema += (VA <= 10), "Restriccion_7"
problema += (VA >= 2), "Restriccion_8"
problema += (V4 <= 10), "Restriccion_9"
problema += (V4 >= 2), "Restriccion_10"
problema += (VB <= 10), "Restriccion_11"
problema += (VB >= 2), "Restriccion_12"

# Resolver el problema
problema.solve()

# Imprimir el valor del funcional objetivo
print("Valor óptimo de Z:", pulp.value(problema.objective))

# Imprimir el valor de todas las variables
for v in problema.variables():
    print(f"{v.name} = {v.varValue}")