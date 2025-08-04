from pulp import *

# Crear el problema de maximización
prob = LpProblem("Refineria_Petroleo", LpMaximize)

# Definir los crudos
crudos = ['SAC', 'TDF', 'CHU', 'SAL', 'NEU']

# Variables de decisión: cantidad de cada crudo procesado
x = LpVariable.dicts("Crudo", crudos, lowBound=0)

# Variables para flujos a CC
y_DOV = LpVariable("DOV_a_CC", lowBound=0)
z_GOP = LpVariable("GOP_a_CC", lowBound=0)

# Parámetros del problema
# Capacidades
cap_PS = 500
cap_CC = 395

# Disponibilidad de crudos
disponibilidad = {'SAC': 120, 'TDF': 120, 'CHU': 150, 'SAL': 110, 'NEU': 150}

# Costos de crudos ($/b)
costo_crudo = {'SAC': 27, 'TDF': 25, 'CHU': 23, 'SAL': 22, 'NEU': 20}

# Costos operativos ($/b)
costo_PS = 0.40
costo_CC = 0.25

# Rendimientos de la Pipe Still
rend_NFV = {'SAC': 0.22, 'TDF': 0.20, 'CHU': 0.15, 'SAL': 0.08, 'NEU': 0.03}
rend_DOV = {'SAC': 0.28, 'TDF': 0.26, 'CHU': 0.30, 'SAL': 0.26, 'NEU': 0.28}
rend_GOP = {'SAC': 0.40, 'TDF': 0.37, 'CHU': 0.35, 'SAL': 0.30, 'NEU': 0.32}
rend_CRR = {'SAC': 0.08, 'TDF': 0.15, 'CHU': 0.18, 'SAL': 0.24, 'NEU': 0.35}

# Rendimientos del Cracking Catalítico
rend_NCC_DOV = 0.25
rend_DCC_DOV = 0.85
rend_NCC_GOP = 0.55
rend_DCC_GOP = 0.60

# Precios de venta ($/b)
precio_NF = 35
precio_DO = 30
precio_FO = 24

# Requerimientos de productos
min_NF = 150
max_NF = 350
min_DO = 150
max_DO = 350
max_FO = 400

# Especificaciones de calidad
octano_NFV = 59
octano_NCC = 98
min_octano_NF = 80

visc_CRR = 14
visc_DOV = 42
visc_DCC = 52
visc_NFV = 60
min_visc_FO = 21

# Función objetivo: Maximizar ganancia
# Ingresos = NF*35 + DO*30 + FO*24
# Costos = Costo crudos + costos operativos PS y CC
prob += (
    # Ingresos por ventas
    (lpSum([rend_NFV[i] * x[i] for i in crudos]) + 
    rend_NCC_DOV * y_DOV + rend_NCC_GOP * z_GOP
    ) * precio_NF + (
    lpSum([rend_DOV[i] * x[i] for i in crudos]) - y_DOV + 
    rend_DCC_DOV * y_DOV + rend_DCC_GOP * z_GOP
    ) * precio_DO + (
    lpSum([rend_CRR[i] * x[i] for i in crudos]) + 
    (lpSum([rend_NFV[i] * x[i] for i in crudos]) + 
    (lpSum([rend_DOV[i] * x[i] for i in crudos]) - y_DOV + 
    rend_DCC_DOV * y_DOV + rend_DCC_GOP * z_GOP
    ) * precio_FO - (
    lpSum([x[i] * costo_crudo[i] for i in crudos]) -  # Costo crudos
    lpSum(x.values()) * costo_PS -  # Costo operativo PS
    (y_DOV + z_GOP) * costo_CC  # Costo operativo CC
    ), "Ganancia_total"

# Restricciones
# 1. Capacidad de plantas
prob += lpSum(x.values()) <= cap_PS, "Capacidad_PS"
prob += y_DOV + z_GOP <= cap_CC, "Capacidad_CC"

# 2. Disponibilidad de crudos
for i in crudos:
    prob += x[i] <= disponibilidad[i], f"Disponibilidad_{i}"

# 3. Balance de materiales
# Nafta Virgen total
NFV_total = lpSum([rend_NFV[i] * x[i] for i in crudos])
# Diesel Oil Virgen total
DOV_total = lpSum([rend_DOV[i] * x[i] for i in crudos])
# Gas Oil Pesado total
GOP_total = lpSum([rend_GOP[i] * x[i] for i in crudos])
# Crudo Reducido total
CRR_total = lpSum([rend_CRR[i] * x[i] for i in crudos])

# 4. Flujos a CC no pueden exceder lo producido
prob += y_DOV <= DOV_total, "Max_DOV_a_CC"
prob += z_GOP <= GOP_total, "Max_GOP_a_CC"

# 5. Requerimientos de productos finales
# Nafta Final = NFV + NCC
NF = NFV_total + rend_NCC_DOV * y_DOV + rend_NCC_GOP * z_GOP
prob += NF >= min_NF, "Min_Nafta"
prob += NF <= max_NF, "Max_Nafta"

# Diesel Oil Final = DOV no enviado a CC + DCC
DO = DOV_total - y_DOV + rend_DCC_DOV * y_DOV + rend_DCC_GOP * z_GOP
prob += DO >= min_DO, "Min_Diesel"
prob += DO <= max_DO, "Max_Diesel"

# Fuel Oil = CRR + excedentes (simplificado)
FO = CRR_total  # Esta es una simplificación, podría incluir otros componentes
prob += FO <= max_FO, "Max_FuelOil"

# 6. Especificaciones de calidad
# Octanaje nafta: (NFV*59 + NCC*98)/(NFV+NCC) >= 80
prob += (NFV_total * octano_NFV + (rend_NCC_DOV * y_DOV + rend_NCC_GOP * z_GOP) * octano_NCC) >= \
        min_octano_NF * (NFV_total + rend_NCC_DOV * y_DOV + rend_NCC_GOP * z_GOP), "Octanaje_Nafta"

# Viscosidad fuel oil: simplificado (asumiendo solo CRR)
# En realidad debería ser una mezcla ponderada >= 21
prob += CRR_total * visc_CRR >= min_visc_FO * CRR_total, "Viscosidad_FO"

# 7. Restricción de mezcla para Diesel Oil: máximo 10% NCC
prob += (rend_NCC_DOV * y_DOV + rend_NCC_GOP * z_GOP) <= 0.1 * DO, "Max_NCC_en_DO"

# Resolver el problema
prob.solve()

# Imprimir resultados
print("Estado:", LpStatus[prob.status])
print("Ganancia máxima: $", value(prob.objective))

print("\nCantidad de cada crudo procesado (Mb/mes):")
for i in crudos:
    print(f"{i}: {value(x[i]):.2f}")

print("\nFlujos al Cracking Catalítico:")
print(f"DOV enviado a CC: {value(y_DOV):.2f} Mb/mes")
print(f"GOP enviado a CC: {value(z_GOP):.2f} Mb/mes")

print("\nProducción de productos intermedios:")
print(f"Nafta Virgen (NFV): {value(NFV_total):.2f} Mb/mes")
print(f"Diesel Oil Virgen (DOV): {value(DOV_total):.2f} Mb/mes")
print(f"Gas Oil Pesado (GOP): {value(GOP_total):.2f} Mb/mes")
print(f"Crudo Reducido (CRR): {value(CRR_total):.2f} Mb/mes")

print("\nProducción de productos finales:")
print(f"Nafta (NF): {value(NF):.2f} Mb/mes")
print(f"Diesel Oil (DO): {value(DO):.2f} Mb/mes")
print(f"Fuel Oil (FO): {value(FO):.2f} Mb/mes")