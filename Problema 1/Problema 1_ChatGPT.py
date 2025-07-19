
import pulp

# Crear el modelo
model = pulp.LpProblem("Refineria", pulp.LpMaximize)

# Variables
crudos = ['CR1', 'CR2', 'CR3']
x = pulp.LpVariable.dicts("Crudo", crudos, 0)  # kBbl/día

# Productos intermedios
rendimientos = {
    'CR1': {'NFV': 0.23, 'DOV': 0.28, 'GOP': 0.40, 'CRR': 0.08},
    'CR2': {'NFV': 0.15, 'DOV': 0.31, 'GOP': 0.35, 'CRR': 0.18},
    'CR3': {'NFV': 0.03, 'DOV': 0.27, 'GOP': 0.27, 'CRR': 0.42},
}

# Disponibilidad y costos
max_crudo = 6.0
costos_crudo = {'CR1': 170, 'CR2': 150, 'CR3': 130}

# Costos y precios
cost_PS = 5
cost_CC = 10
precio_venta = {'NF': 290, 'DO': 240, 'FO': 210}
cost_fijo = 200_000  # en US$/día

# Variables intermedias
nfv = pulp.LpVariable("NFV", 0)
dov = pulp.LpVariable("DOV", 0)
gop = pulp.LpVariable("GOP", 0)
crr = pulp.LpVariable("CRR", 0)

# Variables cracking
y_dov = pulp.LpVariable("DOV_CC", 0)
y_gop = pulp.LpVariable("GOP_CC", 0)
nfc = pulp.LpVariable("NFC", 0)
doc = pulp.LpVariable("DOC", 0)

# Productos finales
nf = pulp.LpVariable("NF", 0, 4)
do = pulp.LpVariable("DO", 0, 4)
fo = pulp.LpVariable("FO", 0)

# Mezclas
nfv_nf = pulp.LpVariable("NFV_a_NF", 0)
nfc_nf = pulp.LpVariable("NFC_a_NF", 0)

dov_do = pulp.LpVariable("DOV_a_DO", 0)
nfc_do = pulp.LpVariable("NFC_a_DO", 0)
doc_do = pulp.LpVariable("DOC_a_DO", 0)

crr_fo = pulp.LpVariable("CRR_a_FO", 0)
doc_fo = pulp.LpVariable("DOC_a_FO", 0)
dov_fo = pulp.LpVariable("DOV_a_FO", 0)
nfv_fo = pulp.LpVariable("NFV_a_FO", 0)

# Restricciones de disponibilidad
for c in crudos:
    model += x[c] <= max_crudo

# Capacidad del Pipe Still
model += pulp.lpSum([x[c] for c in crudos]) <= 10

# Cálculo de productos intermedios
model += nfv == pulp.lpSum([x[c] * rendimientos[c]['NFV'] for c in crudos])
model += dov == pulp.lpSum([x[c] * rendimientos[c]['DOV'] for c in crudos])
model += gop == pulp.lpSum([x[c] * rendimientos[c]['GOP'] for c in crudos])
model += crr == pulp.lpSum([x[c] * rendimientos[c]['CRR'] for c in crudos])

# Capacidad del Cracking Catalítico
model += y_dov + y_gop <= 6.5

# Productos del cracking
model += nfc == 0.25 * y_dov + 0.55 * y_gop
model += doc == 0.85 * y_dov + 0.60 * y_gop

# Balance de mezclas
model += nf == nfv_nf + nfc_nf
model += do == dov_do + nfc_do + doc_do
model += fo == crr_fo + doc_fo + dov_fo + nfv_fo

# Balance de materias primas
model += nfv_nf + nfv_fo <= nfv
model += dov_do + dov_fo + y_dov <= dov
model += gop == y_gop
model += crr_fo <= crr
model += nfc_nf + nfc_do <= nfc
model += doc_do + doc_fo <= doc

# Especificaciones
model += (59 * nfv_nf + 98 * nfc_nf) >= 80 * nf  # Octanaje
model += nfc_do <= 0.10 * do                    # Flash point
model += (14 * crr_fo + 52 * doc_fo + 42 * dov_fo + 60 * nfv_fo) >= 21 * fo  # VBN

# Función objetivo: Maximizar utilidad
ganancia = (
    precio_venta['NF'] * nf +
    precio_venta['DO'] * do +
    precio_venta['FO'] * fo -
    pulp.lpSum([x[c] * costos_crudo[c] for c in crudos]) -
    cost_PS * pulp.lpSum([x[c] for c in crudos]) -
    cost_CC * (y_dov + y_gop) -
    cost_fijo
)

model += ganancia

# Resolver
model.solve()

# Resultados
print(f"Estado: {pulp.LpStatus[model.status]}")
print(f"Ganancia máxima: {pulp.value(model.objective):,.2f} US$/día")
for v in model.variables():
    if v.varValue > 0.001:
        print(f"{v.name}: {v.varValue:.2f}")
