import pulp

# Declarar variables continuas no negativas
NFC = pulp.LpVariable('NFC', lowBound=0, cat='Continuous')
DOC = pulp.LpVariable('DOC', lowBound=0, cat='Continuous')
FOC = pulp.LpVariable('FOC', lowBound=0, cat='Continuous')
SACPS = pulp.LpVariable('SACPS', lowBound=0, cat='Continuous')
TDFPS = pulp.LpVariable('TDFPS', lowBound=0, cat='Continuous')
CHUPS = pulp.LpVariable('CHUPS', lowBound=0, cat='Continuous')
SALPS = pulp.LpVariable('SALPS', lowBound=0, cat='Continuous')
NEUPS = pulp.LpVariable('NEUPS', lowBound=0, cat='Continuous')
APS = pulp.LpVariable('APS', lowBound=0, cat='Continuous')
ACC = pulp.LpVariable('ACC', lowBound=0, cat='Continuous')
NFVNF = pulp.LpVariable('NFVNF', lowBound=0, cat='Continuous')
NFVFO = pulp.LpVariable('NFVFO', lowBound=0, cat='Continuous')
DOVCC = pulp.LpVariable('DOVCC', lowBound=0, cat='Continuous')
DOVDO = pulp.LpVariable('DOVDO', lowBound=0, cat='Continuous')
DOVFO = pulp.LpVariable('DOVFO', lowBound=0, cat='Continuous')
GOPCC = pulp.LpVariable('GOPCC', lowBound=0, cat='Continuous')
CRRFO = pulp.LpVariable('CRRFO', lowBound=0, cat='Continuous')
NCCNF = pulp.LpVariable('NCCNF', lowBound=0, cat='Continuous')
NCCDO = pulp.LpVariable('NCCDO', lowBound=0, cat='Continuous')
DCCDO = pulp.LpVariable('DCCDO', lowBound=0, cat='Continuous')
DCCFO = pulp.LpVariable('DCCFO', lowBound=0, cat='Continuous')

# Definir el problema de maximización
problema = pulp.LpProblem("Problema_5", pulp.LpMaximize)

# Funcional objetivo
problema += (
    35 * NFC + 30 * DOC + 24 * FOC
    - 27 * SACPS - 25 * TDFPS - 23 * CHUPS
    - 22 * SALPS - 20 * NEUPS - 0.4 * APS - 0.25 * ACC
), "Funcional_objetivo"

# Restricciones
problema += (SACPS + TDFPS + CHUPS + SALPS + NEUPS == APS), "Restriccion_1"
problema += (APS <= 500), "Restriccion_2"
problema += (SACPS <= 120), "Restriccion_3"
problema += (TDFPS <= 120), "Restriccion_4"
problema += (CHUPS <= 150), "Restriccion_5"
problema += (SALPS <= 110), "Restriccion_6"
problema += (NEUPS <= 150), "Restriccion_7"
problema += (
    0.22 * SACPS + 0.2 * TDFPS + 0.15 * CHUPS + 0.08 * SALPS + 0.03 * NEUPS
    == NFVNF + NFVFO
), "Restriccion_8"
problema += (
    0.28 * SACPS + 0.26 * TDFPS + 0.3 * CHUPS + 0.26 * SALPS + 0.28 * NEUPS
    == DOVCC + DOVDO + DOVFO
), "Restriccion_9"
problema += (
    0.4 * SACPS + 0.37 * TDFPS + 0.35 * CHUPS + 0.3 * SALPS + 0.32 * NEUPS
    == GOPCC
), "Restriccion_10"
problema += (
    0.08 * SACPS + 0.15 * TDFPS + 0.18 * CHUPS + 0.24 * SALPS + 0.35 * NEUPS
    == CRRFO
), "Restriccion_11"
problema += (DOVCC + GOPCC == ACC), "Restriccion_12"
problema += (ACC <= 395), "Restriccion_13"

problema += (0.25 * DOVCC + 0.55 * GOPCC == NCCNF + NCCDO), "Restriccion_14"
problema += (0.85 * DOVCC + 0.6 * GOPCC == DCCDO + DCCFO), "Restriccion_15"
problema += (NFVNF + NCCNF == NFC), "Restriccion_16"
problema += (59 * NFVNF + 98 * NCCNF >= 80*NFC), "Restriccion_17"

problema += (NFC >= 150), "Restriccion_18"
problema += (NFC <= 350), "Restriccion_19"

problema += (DOVDO + DCCDO + NCCDO == DOC), "Restriccion_20"
problema += (NCCDO <= 0.1 * DOC), "Restriccion_21"

problema += (DOC >= 150), "Restriccion_22"
problema += (DOC <= 350), "Restriccion_23"

problema += (NFVFO + DOVFO + DCCFO + CRRFO == FOC), "Restriccion_24"
problema += (60*NFVFO + 42*DOVFO + 52*DCCFO + 14*CRRFO >= 21*FOC), "Restriccion_25"
problema += (FOC <= 400), "Restriccion_26"

# Resolver el problema
problema.solve()
# Imprimir el estado de la solución
print("Estado de la solución:", pulp.LpStatus[problema.status])
# Imprimir los valores de las variables
for v in problema.variables():
    print(f"{v.name} = {v.varValue}")
# Imprimir el valor de la función objetivo
print("Valor de la función objetivo:", pulp.value(problema.objective))
