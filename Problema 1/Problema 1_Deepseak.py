import pulp
import pandas as pd

# Crear el problema de maximización
prob = pulp.LpProblem("Optimizacion_Alimentos", pulp.LpMaximize)

# Definir variables
y_A = pulp.LpVariable("y_A", lowBound=0)  # kg de Y en A
v_A = pulp.LpVariable("v_A", lowBound=0)  # kg de V en A
w_A = pulp.LpVariable("w_A", lowBound=0)  # kg de W en A

y_B = pulp.LpVariable("y_B", lowBound=0)  # kg de Y en B
v_B = pulp.LpVariable("v_B", lowBound=0)  # kg de V en B
w_B = pulp.LpVariable("w_B", lowBound=0)  # kg de W en B

t_A = pulp.LpVariable("t_A", lowBound=0)  # horas máquina para A
t_B = pulp.LpVariable("t_B", lowBound=0)  # horas máquina para B
t_no_usado = pulp.LpVariable("t_no_usado", lowBound=0)  # horas máquina no usadas

A_fija = pulp.LpVariable("A_fija", lowBound=150, upBound=150)  # kg A demanda fija
A_exc = pulp.LpVariable("A_exc", lowBound=0)  # kg A excedente
B_fija = pulp.LpVariable("B_fija", lowBound=200, upBound=200)  # kg B demanda fija
B_exc = pulp.LpVariable("B_exc", lowBound=0)  # kg B excedente

h_extra = pulp.LpVariable("h_extra", lowBound=0, upBound=30)  # horas mano obra extra

# Función objetivo
# Ingresos: ventas fijas, excedentes, tiempo no usado
ingresos = (35*A_fija + 28*A_exc + 30*B_fija + 24*B_exc + 150*t_no_usado)

# Costos: compuestos, máquina, mano obra normal y extra
costos = (7*(y_A + y_B) + 9*(v_A + v_B) + 5*(w_A + w_B) + 
          100*(t_A + t_B) + 5*150 + 7*h_extra)

prob += ingresos - costos, "Ganancia_Total"

# Restricciones de balance de materiales
prob += y_A + v_A + w_A == A_fija + A_exc, "Balance_A"
prob += y_B + v_B + w_B == B_fija + B_exc, "Balance_B"

# Restricciones de tiempo de máquina
prob += t_A + t_B + t_no_usado == 24, "Tiempo_Maquina_Total"
prob += (A_fija + A_exc) == 15 * t_A, "Produccion_A"
prob += (B_fija + B_exc) == 20 * t_B, "Produccion_B"

# Restricciones de mano de obra
prob += 0.5*(A_fija + A_exc) + 0.4*(B_fija + B_exc) <= 150 + h_extra, "Mano_Obra"

# Restricciones nutricionales para A
prob += 3500*y_A + 3000*v_A + 5000*w_A <= 3900*(A_fija + A_exc), "Valor_Energetico_A_Max"
prob += 45*y_A + 60*v_A + 30*w_A >= 50*(A_fija + A_exc), "Fibra_A_Min"
prob += 30*y_A + 25*v_A + 35*w_A <= 30*(A_fija + A_exc), "Grasas_A_Max"
prob += 0*y_A + 0*v_A + 4*w_A <= 3*(A_fija + A_exc), "Grasas_Sat_A_Max"
prob += 150*y_A + 130*v_A + 50*w_A >= 70*(A_fija + A_exc), "Hidratos_A_Min"
prob += 150*y_A + 130*v_A + 50*w_A <= 130*(A_fija + A_exc), "Hidratos_A_Max"
prob += 40*y_A + 70*v_A + 50*w_A >= 45*(A_fija + A_exc), "Hierro_A_Min"
prob += 5.7*y_A + 3.3*v_A + 4.1*w_A >= 3.7*(A_fija + A_exc), "Calcio_A_Min"
prob += 20*y_A + 30*v_A + 20*w_A >= 22*(A_fija + A_exc), "Vitaminas_A_Min"
prob += 0*y_A + 0*v_A + 12*w_A <= 5*(A_fija + A_exc), "Colesterol_A_Max"
prob += 130*y_A + 180*v_A + 100*w_A >= 140*(A_fija + A_exc), "Proteina_A_Min"

# Restricciones nutricionales para B
prob += 3500*y_B + 3000*v_B + 5000*w_B <= 4500*(B_fija + B_exc), "Valor_Energetico_B_Max"
prob += 45*y_B + 60*v_B + 30*w_B >= 40*(B_fija + B_exc), "Fibra_B_Min"
prob += 30*y_B + 25*v_B + 35*w_B <= 33*(B_fija + B_exc), "Grasas_B_Max"
prob += 0*y_B + 0*v_B + 4*w_B <= 3*(B_fija + B_exc), "Grasas_Sat_B_Max"
prob += 150*y_B + 130*v_B + 50*w_B >= 80*(B_fija + B_exc), "Hidratos_B_Min"
prob += 150*y_B + 130*v_B + 50*w_B <= 140*(B_fija + B_exc), "Hidratos_B_Max"
prob += 40*y_B + 70*v_B + 50*w_B >= 45*(B_fija + B_exc), "Hierro_B_Min"
prob += 5.7*y_B + 3.3*v_B + 4.1*w_B >= 3.5*(B_fija + B_exc), "Calcio_B_Min"
prob += 20*y_B + 30*v_B + 20*w_B >= 22*(B_fija + B_exc), "Vitaminas_B_Min"
prob += 0*y_B + 0*v_B + 12*w_B <= 10*(B_fija + B_exc), "Colesterol_B_Max"
prob += 130*y_B + 180*v_B + 100*w_B >= 120*(B_fija + B_exc), "Proteina_B_Min"

# Resolver el problema
prob.solve()

# Mostrar resultados
print("Estado:", pulp.LpStatus[prob.status])
print("Ganancia total: $", pulp.value(prob.objective))

# Recopilar resultados en un DataFrame
resultados = []
for v in prob.variables():
    resultados.append({
        "Variable": v.name,
        "Valor": v.varValue
    })

df_resultados = pd.DataFrame(resultados)
print("\nVariables de decisión:")
print(df_resultados.to_string(index=False))

# Calcular costos e ingresos
print("\nResumen financiero:")
print(f"Ingresos por ventas fijas: ${35*150 + 30*200:,.2f}")
print(f"Ingresos por ventas excedentes: ${28*df_resultados[df_resultados['Variable']=='A_exc']['Valor'].values[0] + 24*df_resultados[df_resultados['Variable']=='B_exc']['Valor'].values[0]:,.2f}")
print(f"Ingresos por tiempo no usado: ${150*df_resultados[df_resultados['Variable']=='t_no_usado']['Valor'].values[0]:,.2f}")
print(f"Costos de compuestos: ${7*(df_resultados[df_resultados['Variable']=='y_A']['Valor'].values[0] + df_resultados[df_resultados['Variable']=='y_B']['Valor'].values[0]) + 9*(df_resultados[df_resultados['Variable']=='v_A']['Valor'].values[0] + df_resultados[df_resultados['Variable']=='v_B']['Valor'].values[0]) + 5*(df_resultados[df_resultados['Variable']=='w_A']['Valor'].values[0] + df_resultados[df_resultados['Variable']=='w_B']['Valor'].values[0]):,.2f}")
print(f"Costos de máquina: ${100*(df_resultados[df_resultados['Variable']=='t_A']['Valor'].values[0] + df_resultados[df_resultados['Variable']=='t_B']['Valor'].values[0]):,.2f}")
print(f"Costos de mano obra normal: ${5*150:,.2f}")
print(f"Costos de mano obra extra: ${7*df_resultados[df_resultados['Variable']=='h_extra']['Valor'].values[0]:,.2f}")