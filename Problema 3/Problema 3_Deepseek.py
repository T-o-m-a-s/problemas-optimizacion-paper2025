from pulp import *

# Crear el problema de maximización
prob = LpProblem("Maximizar_Beneficio_Whisky", LpMaximize)

# Definir las variables
E_A = LpVariable("E_A", lowBound=0)
E_B = LpVariable("E_B", lowBound=0)
E_C = LpVariable("E_C", lowBound=0)

K_A = LpVariable("K_A", lowBound=0)
K_B = LpVariable("K_B", lowBound=0)
K_C = LpVariable("K_C", lowBound=0)

T_A = LpVariable("T_A", lowBound=0)
T_B = LpVariable("T_B", lowBound=0)
T_C = LpVariable("T_C", lowBound=0)

# Función objetivo
prob += (-0.2*E_A + 1.8*E_B + 2.8*E_C - 1.3*K_A + 0.7*K_B + 1.7*K_C - 2.5*T_A - 0.5*T_B + 0.5*T_C, 
         "Beneficio_Total")

# Restricciones de disponibilidad
prob += E_A + K_A + T_A <= 2000, "Disponibilidad_A"
prob += E_B + K_B + T_B <= 2500, "Disponibilidad_B"
prob += E_C + K_C + T_C <= 1200, "Disponibilidad_C"

# Restricciones de especificación para Escocés
prob += 0.4*E_A - 0.6*E_B - 0.6*E_C >= 0, "Escoces_min_A"
prob += -0.2*E_A - 0.2*E_B + 0.8*E_C <= 0, "Escoces_max_C"

# Restricciones de especificación para Kilt
prob += 0.85*K_A - 0.15*K_B - 0.15*K_C >= 0, "Kilt_min_A"
prob += -0.6*K_A - 0.6*K_B + 0.4*K_C <= 0, "Kilt_max_C"

# Restricciones de especificación para Tartan
prob += -0.5*T_A - 0.5*T_B + 0.5*T_C <= 0, "Tartan_max_C"

# Resolver el problema
prob.solve()

# Imprimir resultados
print("Estado:", LpStatus[prob.status])
print("Beneficio máximo: $", value(prob.objective))

print("\nMezclas óptimas:")
print(f"Escocés: A={value(E_A):.2f}L, B={value(E_B):.2f}L, C={value(E_C):.2f}L - Total={value(E_A + E_B + E_C):.2f}L")
print(f"Kilt:    A={value(K_A):.2f}L, B={value(K_B):.2f}L, C={value(K_C):.2f}L - Total={value(K_A + K_B + K_C):.2f}L")
print(f"Tartan:  A={value(T_A):.2f}L, B={value(T_B):.2f}L, C={value(T_C):.2f}L - Total={value(T_A + T_B + T_C):.2f}L")

print("\nLicores utilizados:")
print(f"A: {value(E_A + K_A + T_A):.2f}L de 2000L disponibles")
print(f"B: {value(E_B + K_B + T_B):.2f}L de 2500L disponibles")
print(f"C: {value(E_C + K_C + T_C):.2f}L de 1200L disponibles")