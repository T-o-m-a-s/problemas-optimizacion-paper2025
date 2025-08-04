
import pulp

# Declaración de variables continuas no negativas
A1 = pulp.LpVariable('A1', lowBound=0, cat='Continuous')
B1 = pulp.LpVariable('B1', lowBound=0, cat='Continuous')
A2 = pulp.LpVariable('A2', lowBound=0, cat='Continuous')
B2 = pulp.LpVariable('B2', lowBound=0, cat='Continuous')
SM = pulp.LpVariable('SM', lowBound=0, cat='Continuous')
Y = pulp.LpVariable('Y', lowBound=0, cat='Continuous')
V = pulp.LpVariable('V', lowBound=0, cat='Continuous')
W = pulp.LpVariable('W', lowBound=0, cat='Continuous')
HMU = pulp.LpVariable('HMU', lowBound=0, cat='Continuous')
HN = pulp.LpVariable('HN', lowBound=0, cat='Continuous')
HE = pulp.LpVariable('HE', lowBound=0, cat='Continuous')
YA = pulp.LpVariable('YA', lowBound=0, cat='Continuous')
YB = pulp.LpVariable('YB', lowBound=0, cat='Continuous')
VA = pulp.LpVariable('VA', lowBound=0, cat='Continuous')
VB = pulp.LpVariable('VB', lowBound=0, cat='Continuous')
WA = pulp.LpVariable('WA', lowBound=0, cat='Continuous')
WB = pulp.LpVariable('WB', lowBound=0, cat='Continuous')
A = pulp.LpVariable('A', lowBound=0, cat='Continuous')
B = pulp.LpVariable('B', lowBound=0, cat='Continuous')

# Definir el problema de maximización
prob = pulp.LpProblem('Problema_Maximizacion', pulp.LpMaximize)

# Definir la función objetivo
prob += 35*A1 + 30*B1 + 28*A2 + 24*B2 + 150*SM - 7*Y - 9*V - 5*W - 100*HMU - 5*HN - 7*HE, 'Z'

# Restricciones
prob += YA + YB == Y, 'restriccion_Y'
prob += VA + VB == V, 'restriccion_V'
prob += WA + WB == W, 'restriccion_W'
prob += YA + VA + WA == A, 'restriccion_A'
prob += YB + VB + WB == B, 'restriccion_B'

# Restricciones adicionales
prob += 3500*YA + 300*VA + 500*WA <= 3900*A, 'restriccion_capacidad_A'
prob += 3500*YB + 300*VB + 500*WB <= 4500*B, 'restriccion_capacidad_B'

# Restricciones de demanda mínima
prob += 45*YA + 60*VA + 30*WA >= 50*A, 'restriccion_demanda_A'
prob += 45*YB + 60*VB + 30*WB >= 40*B, 'restriccion_demanda_B'

# Restricciones adicionales de recursos
prob += 30*YA + 25*VA + 35*WA <= 30*A, 'restriccion_recurso_A'
prob += 30*YB + 25*VB + 35*WB <= 33*B, 'restriccion_recurso_B'

# Restricciones adicionales solicitadas
prob += 4*WA <= 3*A, 'restriccion_WA_A'
prob += 4*WB <= 3*B, 'restriccion_WB_B'
prob += 150*YA + 130*VA + 50*WA >= 70*A, 'restriccion_minima_A'
prob += 150*YB + 130*VB + 50*WB >= 80*B, 'restriccion_minima_B'

# Más restricciones solicitadas
prob += 150*YA + 130*VA + 50*WA <= 130*A, 'restriccion_maxima_A'
prob += 150*YB + 130*VB + 50*WB <= 140*B, 'restriccion_maxima_B'
prob += 40*YA + 70*VA + 50*WA >= 45*A, 'restriccion_minima2_A'
prob += 40*YB + 70*VB + 50*WB >= 45*B, 'restriccion_minima2_B'

# Más restricciones solicitadas
prob += 5.7*YA + 3.3*VA + 4.1*WA >= 3.7*A, 'restriccion_minima3_A'
prob += 5.7*YB + 3.3*VB + 4.1*WB >= 3.5*B, 'restriccion_minima3_B'
prob += 20*YA + 30*VA + 20*WA >= 22*A, 'restriccion_minima4_A'
prob += 20*YB + 30*VB + 20*WB >= 22*B, 'restriccion_minima4_B'

# Más restricciones solicitadas
prob += 12*WA <= 5*A, 'restriccion_WA_A_2'
prob += 12*WB <= 10*B, 'restriccion_WB_B_2'
prob += 130*YA + 180*VA + 100*WA >= 140*A, 'restriccion_minima5_A'
prob += 130*YB + 180*VB + 100*WB >= 120*B, 'restriccion_minima5_B'

# Restricciones para HMU, SM, HN y HE
prob += 0.0667*A + 0.05*B == HMU, 'restriccion_HMU'
prob += HMU + SM == 24, 'restriccion_HMU_SM'
prob += 0.5*A + 0.4*B == HN + HE, 'restriccion_HN_HE'
prob += HN <= 150, 'restriccion_HN_max'
prob += HE <= 30, 'restriccion_HE_max'

# Restricciones finales
prob += A1 + A2 == A, 'restriccion_A1_A2_A'
prob += B1 + B2 == B, 'restriccion_B1_B2_B'
prob += A1 == 150, 'restriccion_A1_fijo'
prob += B1 == 200, 'restriccion_B1_fijo'

# Resolver el modelo
prob.solve()

# Imprimir el valor óptimo de la función objetivo
print('Valor óptimo de Z:', pulp.value(prob.objective))

# Imprimir los valores de las variables en el orden declarado
variables = [A1, B1, A2, B2, SM, Y, V, W, HMU, HN, HE, YA, YB, VA, VB, WA, WB, A, B]
for var in variables:
    print(f'{var.name} =', var.varValue)


