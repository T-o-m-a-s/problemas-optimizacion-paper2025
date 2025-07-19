from pulp import *

# Initialize the model
model = LpProblem("Refinery_Optimization", LpMaximize)

# Variables
# Crude inputs to Pipestill (kBbl/D)
CR1 = LpVariable("CR1", lowBound=0, upBound=6)  # Crude 1
CR2 = LpVariable("CR2", lowBound=0, upBound=6)  # Crude 2
CR3 = LpVariable("CR3", lowBound=0, upBound=6)  # Crude 3

# Intermediate products from Pipestill (kBbl/D)
NFV1 = LpVariable("NFV1", lowBound=0)  # Nafta Virgen from CR1
NFV2 = LpVariable("NFV2", lowBound=0)  # Nafta Virgen from CR2
NFV3 = LpVariable("NFV3", lowBound=0)  # Nafta Virgen from CR3
DOV1 = LpVariable("DOV1", lowBound=0)  # Diesel Oil Virgen from CR1
DOV2 = LpVariable("DOV2", lowBound=0)  # Diesel Oil Virgen from CR2
DOV3 = LpVariable("DOV3", lowBound=0)  # Diesel Oil Virgen from CR3
GOP1 = LpVariable("GOP1", lowBound=0)  # Gas Oil Pesado from CR1
GOP2 = LpVariable("GOP2", lowBound=0)  # Gas Oil Pesado from CR2
GOP3 = LpVariable("GOP3", lowBound=0)  # Gas Oil Pesado from CR3
CRR1 = LpVariable("CRR1", lowBound=0)  # Crudo Reducido from CR1
CRR2 = LpVariable("CRR2", lowBound=0)  # Crudo Reducido from CR2
CRR3 = LpVariable("CRR3", lowBound=0)  # Crudo Reducido from CR3

# Catalytic Cracking inputs (kBbl/D)
DOV_to_CC = LpVariable("DOV_to_CC", lowBound=0)  # DOV to Catalytic Cracking
GOP_to_CC = LpVariable("GOP_to_CC", lowBound=0)  # GOP to Catalytic Cracking

# Catalytic Cracking outputs (kBbl/D)
NFC = LpVariable("NFC", lowBound=0)  # Nafta Catalítica
DOC = LpVariable("DOC", lowBound=0)  # Diesel Oil Catalítico

# Blending variables for final products (kBbl/D)
NFV_to_NF = LpVariable("NFV_to_NF", lowBound=0)  # NFV to Nafta Comercial
NFC_to_NF = LpVariable("NFC_to_NF", lowBound=0)  # NFC to Nafta Comercial
DOV_to_DO = LpVariable("DOV_to_DO", lowBound=0)  # DOV to Diesel Oil Comercial
NFC_to_DO = LpVariable("NFC_to_DO", lowBound=0)  # NFC to Diesel Oil Comercial
DOC_to_DO = LpVariable("DOC_to_DO", lowBound=0)  # DOC to Diesel Oil Comercial
CRR_to_FO = LpVariable("CRR_to_FO", lowBound=0)  # CRR to Fuel Oil Comercial
DOC_to_FO = LpVariable("DOC_to_FO", lowBound=0)  # DOC to Fuel Oil Comercial
DOV_to_FO = LpVariable("DOV_to_FO", lowBound=0)  # DOV to Fuel Oil Comercial
NFV_to_FO = LpVariable("NFV_to_FO", lowBound=0)  # NFV to Fuel Oil Comercial

# Final products (kBbl/D)
NF = LpVariable("NF", lowBound=0, upBound=4)  # Nafta Comercial
DO = LpVariable("DO", lowBound=0, upBound=4)  # Diesel Oil Comercial
FO = LpVariable("FO", lowBound=0)  # Fuel Oil Comercial

# Constraints
# Pipestill capacity
model += CR1 + CR2 + CR3 <= 10, "Pipestill_Capacity"

# Crude yields
model += NFV1 == 0.23 * CR1, "NFV1_Yield"
model += DOV1 == 0.28 * CR1, "DOV1_Yield"
model += GOP1 == 0.40 * CR1, "GOP1_Yield"
model += CRR1 == 0.08 * CR1, "CRR1_Yield"
model += NFV2 == 0.15 * CR2, "NFV2_Yield"
model += DOV2 == 0.31 * CR2, "DOV2_Yield"
model += GOP2 == 0.35 * CR2, "GOP2_Yield"
model += CRR2 == 0.18 * CR2, "CRR2_Yield"
model += NFV3 == 0.03 * CR3, "NFV3_Yield"
model += DOV3 == 0.27 * CR3, "DOV3_Yield"
model += GOP3 == 0.27 * CR3, "GOP3_Yield"
model += CRR3 == 0.42 * CR3, "CRR3_Yield"

# Material balances for intermediates
NFV_total = NFV1 + NFV2 + NFV3
DOV_total = DOV1 + DOV2 + DOV3
GOP_total = GOP1 + GOP2 + GOP3
CRR_total = CRR1 + CRR2 + CRR3

model += NFV_total == NFV_to_NF + NFV_to_FO, "NFV_Balance"
model += DOV_total == DOV_to_CC + DOV_to_DO + DOV_to_FO, "DOV_Balance"
model += GOP_total == GOP_to_CC, "GOP_Balance"
model += CRR_total == CRR_to_FO, "CRR_Balance"

# Catalytic Cracking capacity
model += DOV_to_CC + GOP_to_CC <= 6.5, "CC_Capacity"

# Catalytic Cracking yields
model += NFC == 0.25 * DOV_to_CC + 0.55 * GOP_to_CC, "NFC_Yield"
model += DOC == 0.85 * DOV_to_CC + 0.60 * GOP_to_CC, "DOC_Yield"

# Final product compositions
model += NF == NFV_to_NF + NFC_to_NF, "NF_Composition"
model += DO == DOV_to_DO + NFC_to_DO + DOC_to_DO, "DO_Composition"
model += FO == CRR_to_FO + DOC_to_FO + DOV_to_FO + NFV_to_FO, "FO_Composition"

# Quality constraints
# Nafta Comercial: Octane number >= 80
model += 59 * NFV_to_NF + 98 * NFC_to_NF >= 80 * NF, "NF_Octane"

# Diesel Oil Comercial: NFC <= 10%
model += NFC_to_DO <= 0.10 * DO, "DO_NFC_Limit"

# Fuel Oil Comercial: V.B.N. >= 21
model += (14 * CRR_to_FO + 52 * DOC_to_FO + 42 * DOV_to_FO + 60 * NFV_to_FO) >= 21 * FO, "FO_VBN"

# Objective function (Profit in US$/D)
revenue = 1000 * (290 * NF + 240 * DO + 210 * FO)
crude_cost = 1000 * (170 * CR1 + 150 * CR2 + 130 * CR3)
processing_cost = 1000 * (5 * (CR1 + CR2 + CR3) + 10 * (DOV_to_CC + GOP_to_CC))
fixed_cost = 200000
model += revenue - crude_cost - processing_cost - fixed_cost, "Profit"

# Solve the model
model.solve()

# Print results
print("Status:", LpStatus[model.status])
print("Profit: ${:.2f}".format(value(model.objective)))
print("\nCrude Inputs (kBbl/D):")
print(f"CR1: {value(CR1):.2f}")
print(f"CR2: {value(CR2):.2f}")
print(f"CR3: {value(CR3):.2f}")
print("\nFinal Products (kBbl/D):")
print(f"Nafta Comercial (NF): {value(NF):.2f}")
print(f"Diesel Oil Comercial (DO): {value(DO):.2f}")
print(f"Fuel Oil Comercial (FO): {value(FO):.2f}")
print("\nCatalytic Cracking Inputs (kBbl/D):")
print(f"DOV to CC: {value(DOV_to_CC):.2f}")
print(f"GOP to CC: {value(GOP_to_CC):.2f}")
print("\nBlending Quantities (kBbl/D):")
print(f"NFV to NF: {value(NFV_to_NF):.2f}")
print(f"NFC to NF: {value(NFC_to_NF):.2f}")
print(f"DOV to DO: {value(DOV_to_DO):.2f}")
print(f"NFC to DO: {value(NFC_to_DO):.2f}")
print(f"DOC to DO: {value(DOC_to_DO):.2f}")
print(f"CRR to FO: {value(CRR_to_FO):.2f}")
print(f"DOC to FO: {value(DOC_to_FO):.2f}")
print(f"DOV to FO: {value(DOV_to_FO):.2f}")
print(f"NFV to FO: {value(NFV_to_FO):.2f}")