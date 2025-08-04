import pulp

problem = pulp.LpProblem("Problema_4", pulp.LpMaximize)

XA = pulp.LpVariable("XA", lowBound=0, cat='Continuous')
XC = pulp.LpVariable("XB", lowBound=0, cat='Continuous')

problem += 15000 * XA + 12500 * XC, "Objetivo"

problem += (1/25000) * XA + (1/40000) * XC <= 1, "Restriccion_1"
problem += (1/33333) * XA + (1/16667) * XC <= 1, "Restriccion_2"
problem +=  XA <= 22500, "Restriccion_3"
problem +=  XC <= 15000, "Restriccion_4"
problem += XA >= 12000, "Restriccion_5"
problem += XC >= 8000, "Restriccion_6"
problem += XA <= 18000, "Restriccion_7"

# Resolver el problema
problem.solve()

# Imprimir el valor del funcional objetivo
print("Valor óptimo de Z:", pulp.value(problem.objective))

# Imprimir el valor de todas las variables
for v in problem.variables():
    print(f"{v.name} = {v.varValue}")
