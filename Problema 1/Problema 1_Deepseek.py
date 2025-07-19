
import pulp

# Crear el problema de maximización
prob = pulp.LpProblem("Refineria_Petroleo", pulp.LpMaximize)

# Variables de decisión
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')  # Crudo 1 procesado
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')  # Crudo 2 procesado
x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')  # Crudo 3 procesado

y1 = pulp.LpVariable('y1', lowBound=0, cat='Continuous')  # DOV procesado en CC
y2 = pulp.LpVariable('y2', lowBound=0, cat='Continuous')  # GOP procesado en CC

# Variables para mezclas de productos finales
zNFV = pulp.LpVariable('zNFV', lowBound=0, cat='Continuous')  # NFV en NF
zNFC = pulp.LpVariable('zNFC', lowBound=0, cat='Continuous')  # NFC en NF

zDOV = pulp.LpVariable('zDOV', lowBound=0, cat='Continuous')    # DOV en DO
zNFC_DO = pulp.LpVariable('zNFC_DO', lowBound=0, cat='Continuous')  # NFC en DO
zDOC_DO = pulp.LpVariable('zDOC_DO', lowBound=0, cat='Continuous')  # DOC en DO

zCRR = pulp.LpVariable('zCRR', lowBound=0, cat='Continuous')    # CRR en FO
zDOC_FO = pulp.LpVariable('zDOC_FO', lowBound=0, cat='Continuous')  # DOC en FO
zDOV_FO = pulp.LpVariable('zDOV_FO', lowBound=0, cat='Continuous')  # DOV en FO
zNFV_FO = pulp.LpVariable('zNFV_FO', lowBound=0, cat='Continuous')  # NFV en FO

# Calcular productos intermedios
NFV = 0.23*x1 + 0.15*x2 + 0.03*x3
DOV = 0.28*x1 + 0.31*x2 + 0.27*x3
GOP = 0.40*x1 + 0.35*x2 + 0.27*x3
CRR = 0.08*x1 + 0.18*x2 + 0.42*x3

# Calcular productos del cracking
NFC = 0.25*y1 + 0.55*y2
DOC = 0.85*y1 + 0.60*y2

# Productos finales
NF = zNFV + zNFC
DO = zDOV + zNFC_DO + zDOC_DO
FO = zCRR + zDOC_FO + zDOV_FO + zNFV_FO

# Función objetivo: Maximizar ganancia
ingresos = 290*NF + 240*DO + 210*FO
costos = 170*x1 + 150*x2 + 130*x3 + 5*(x1+x2+x3) + 10*(y1+y2)
costo_fijo = 200
prob += ingresos - costos - costo_fijo, "Ganancia_Neta"

# Restricciones
# Capacidades de plantas
prob += x1 + x2 + x3 <= 10, "Capacidad_Pipestill"
prob += y1 + y2 <= 6.5, "Capacidad_Cracking"

# Disponibilidad de crudos
prob += x1 <= 6, "Disponibilidad_CR1"
prob += x2 <= 6, "Disponibilidad_CR2"
prob += x3 <= 6, "Disponibilidad_CR3"

# Balance de materiales
prob += zNFV + zNFV_FO == NFV, "Balance_NFV"
prob += zDOV + zDOV_FO + y1 == DOV, "Balance_DOV"
prob += y2 == GOP, "Balance_GOP"
prob += zCRR + zDOC_FO + zDOV_FO + zNFV_FO >= CRR, "Balance_CRR"  # Asumiendo que todo CRR va a FO

# Productos del cracking
prob += zNFC + zNFC_DO == NFC, "Balance_NFC"
prob += zDOC_DO + zDOC_FO == DOC, "Balance_DOC"

# Requerimientos de productos finales
prob += NF <= 4, "Max_Nafta_Comercial"
prob += DO <= 4, "Max_Diesel_Comercial"

# Especificaciones comerciales
# Nafta: número de octano mínimo 80
prob += 59*zNFV + 98*zNFC >= 80*NF, "Octano_Nafta"

# Diesel: máximo 10% de NFC
prob += zNFC_DO <= 0.10*DO, "Flash_Point_Diesel"

# Fuel Oil: VBN mínimo 21
prob += 14*zCRR + 52*zDOC_FO + 42*zDOV_FO + 60*zNFV_FO >= 21*FO, "VBN_Fuel_Oil"

# Resolver el problema
prob.solve()

# Mostrar resultados
print("Estado:", pulp.LpStatus[prob.status])
print("Ganancia máxima (kUS$/D):", pulp.value(prob.objective))
print("\nVariables de decisión óptimas:")
for v in prob.variables():
    print(f"{v.name}: {v.varValue:.2f} kBbl/D")

print("\nProductos finales:")
print(f"Nafta Comercial (NF): {pulp.value(NF):.2f} kBbl/D")
print(f"Diesel Oil Comercial (DO): {pulp.value(DO):.2f} kBbl/D")
print(f"Fuel Oil Comercial (FO): {pulp.value(FO):.2f} kBbl/D")

print("\nProductos intermedios:")
print(f"Nafta Virgen (NFV): {pulp.value(NFV):.2f} kBbl/D")
print(f"Diesel Oil Virgen (DOV): {pulp.value(DOV):.2f} kBbl/D")
print(f"Gas Oil Pesado (GOP): {pulp.value(GOP):.2f} kBbl/D")
print(f"Crudo Reducido (CRR): {pulp.value(CRR):.2f} kBbl/D")
print(f"Nafta Catalítica (NFC): {pulp.value(NFC):.2f} kBbl/D")
print(f"Diesel Oil Catalítico (DOC): {pulp.value(DOC):.2f} kBbl/D")