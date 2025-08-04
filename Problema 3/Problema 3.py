import pulp

# Declarar variables continuas no negativas
A = pulp.LpVariable('A', lowBound=0, cat='Continuous')
B = pulp.LpVariable('B', lowBound=0, cat='Continuous')
C = pulp.LpVariable('C', lowBound=0, cat='Continuous')
E = pulp.LpVariable('E', lowBound=0, cat='Continuous')
K = pulp.LpVariable('K', lowBound=0, cat='Continuous')
T = pulp.LpVariable('T', lowBound=0, cat='Continuous')
AE = pulp.LpVariable('AE', lowBound=0, cat='Continuous')
AK = pulp.LpVariable('AK', lowBound=0, cat='Continuous')
AT = pulp.LpVariable('AT', lowBound=0, cat='Continuous')
BE = pulp.LpVariable('BE', lowBound=0, cat='Continuous')
BK = pulp.LpVariable('BK', lowBound=0, cat='Continuous')
BT = pulp.LpVariable('BT', lowBound=0, cat='Continuous')
CE = pulp.LpVariable('CE', lowBound=0, cat='Continuous')
CK = pulp.LpVariable('CK', lowBound=0, cat='Continuous')
CT = pulp.LpVariable('CT', lowBound=0, cat='Continuous')

# Declarar el problema
problema = pulp.LpProblem('Problema', pulp.LpMaximize)

# Función objetivo
problema += 6.8 * E + 5.7 * K + 4.5 * T - 7 * A - 5 * B - 4 * C, 'Beneficio_total'

# Restricciones
problema += A <= 2000, 'Restriccion_1'
problema += B <= 2500, 'Restriccion_2'
problema += C <= 1200, 'Restriccion_3'
problema += AE + AK + AT == A, 'Restriccion_4'
problema += BE + BK + BT == B, 'Restriccion_5'
problema += CE + CK + CT == C, 'Restriccion_6'
problema += AE + BE + CE == E, 'Restriccion_7'
problema += AK + BK + CK == K, 'Restriccion_8'
problema += AT + BT + CT == T, 'Restriccion_9'
problema += 0.6 * E <= AE, 'Restriccion_10'
problema += CE <= 0.2 * E, 'Restriccion_11'
problema += 0.15 * K <= AK, 'Restriccion_12'
problema += CK <= 0.6 * K, 'Restriccion_13'
problema += CT <= 0.5 * T, 'Restriccion_14'

# Resolver el problema
problema.solve()

# Imprimir resultados
print("Estado:", pulp.LpStatus[problema.status])
print("Beneficio total:", pulp.value(problema.objective))
for variable in problema.variables():
    print(f"{variable.name} = {variable.varValue}")