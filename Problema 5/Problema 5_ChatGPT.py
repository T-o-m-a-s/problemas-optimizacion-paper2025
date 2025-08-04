import pulp

# Crear el modelo
model = pulp.LpProblem("Refineria_Max_Ganancia", pulp.LpMaximize)

# VARIABLES DE DECISIÓN
x_SAC = pulp.LpVariable("x_SAC", lowBound=0)
x_TDF = pulp.LpVariable("x_TDF", lowBound=0)
x_CHU = pulp.LpVariable("x_CHU", lowBound=0)
x_SAL = pulp.LpVariable("x_SAL", lowBound=0)
x_NEU = pulp.LpVariable("x_NEU", lowBound=0)

y_GOP = pulp.LpVariable("y_GOP", lowBound=0)  # alimentación de GOP al cracking
y_DOV = pulp.LpVariable("y_DOV", lowBound=0)  # alimentación de DOV al cracking

# PRODUCTOS INTERMEDIOS
NFV = 0.22*x_SAC + 0.20*x_TDF + 0.15*x_CHU + 0.08*x_SAL + 0.03*x_NEU
DOV = 0.28*x_SAC + 0.26*x_TDF + 0.30*x_CHU + 0.26*x_SAL + 0.28*x_NEU
GOP = 0.40*x_SAC + 0.37*x_TDF + 0.35*x_CHU + 0.30*x_SAL + 0.32*x_NEU
CRR = 0.08*x_SAC + 0.15*x_TDF + 0.18*x_CHU + 0.24*x_SAL + 0.35*x_NEU

# PRODUCTOS DEL CRACKING
NCC = 0.25*y_DOV + 0.55*y_GOP  # Nafta catalítica
DCC = 0.85*y_DOV + 0.60*y_GOP  # Diesel oil catalítico

# PRODUCTOS FINALES
NF = NFV + NCC
DO = DOV + DCC
FO = CRR  # en este modelo base, solo CRR va a Fuel Oil

# --------------------
# RESTRICCIONES
# --------------------

# 1. Capacidad de planta
model += x_SAC + x_TDF + x_CHU + x_SAL + x_NEU <= 500, "Capacidad_PipeStill"
model += y_GOP + y_DOV <= 395, "Capacidad_Cracking"

# 2. Disponibilidad de crudos
model += x_SAC <= 120, "Disp_SAC"
model += x_TDF <= 120, "Disp_TDF"
model += x_CHU <= 150, "Disp_CHU"
model += x_SAL <= 110, "Disp_SAL"
model += x_NEU <= 150, "Disp_NEU"

# 3. Alimentación del CC no puede superar lo disponible
model += y_GOP <= GOP, "GOP_disponible_para_CC"
model += y_DOV <= DOV, "DOV_disponible_para_CC"

# 4. Requisitos comerciales (rangos de producción)
model += NF >= 150, "NF_min"
model += NF <= 350, "NF_max"
model += DO >= 150, "DO_min"
model += DO <= 350, "DO_max"
model += FO >= 0,    "FO_min"
model += FO <= 400,  "FO_max"

# 5. Requisito de octanaje para la Nafta final
model += 59*NFV + 98*NCC >= 80*(NFV + NCC), "Octanaje_Nafta"

# 6. Restricción de flash point en Diesel oil: máx 10% de NCC
model += NCC <= 0.10 * DO, "Flash_point_Diesel"

# 7. Viscosidad del Fuel Oil final
model += (
    14*CRR + 42*DOV + 52*DCC + 60*NFV >= 21 * FO
), "Viscosidad_FuelOil"

# --------------------
# FUNCIÓN OBJETIVO
# --------------------

# Ingresos
ingresos = 35*NF + 30*DO + 24*FO

# Costos
costo_crudos = (
    27*x_SAC + 25*x_TDF + 23*x_CHU + 22*x_SAL + 20*x_NEU
)
costo_operativo = 0.40*(x_SAC + x_TDF + x_CHU + x_SAL + x_NEU) + 0.25*(y_GOP + y_DOV)

# Ganancia total
model += ingresos - costo_crudos - costo_operativo, "Ganancia_total"

# --------------------
# RESOLVER EL MODELO
# --------------------
model.solve()

# --------------------
# MOSTRAR RESULTADOS
# --------------------
print("Estado:", pulp.LpStatus[model.status])
for var in model.variables():
    print(f"{var.name} = {var.varValue:.2f}")
print(f"Ganancia máxima: ${pulp.value(model.objective):,.2f}")
