# DEFINIR PARAMETROS
from gurobipy import *
from parser_archivos import genera_profesores_dict
from pprint import pprint
import csv

profesores, ramos = genera_profesores_dict()
nivel = [str(i) for i in range(1, 9)]
letra_curso = ["A", "B"]

cursos = [i + j for i in nivel for j in letra_curso]

modulos = [i for i in range(1, 8)]
dias = [i for i in range(1, 5)]


def horas_nivel():
    retorno = {}
    with open('horas.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            for i in range(1, 9):
                retorno[(i, row['\ufefframo'])] = row[str(i)]

    return retorno


horas_lvl = horas_nivel()

cursos = []
for lvl in nivel:
    for letra in letra_curso:
        cursos.append(f'{lvl}{letra}')

dict_retorno = {}

for curso in cursos:
    for ramo in ramos.values():
        dict_retorno[(curso, ramo)] = int(horas_lvl[(int(curso[0]), ramo)])

_, horas_por_curso = multidict(dict_retorno)


# nombres_ramos = ramos.values()
diccionario_profesores_ramos = {}
diccionario_profesores_ensenan = {}
for id_, profesor in profesores.items():
    for ramo_nombre in ramos.values():
        diccionario_profesores_ensenan[profesor['nombre']] = profesor['ht']

        if ramo_nombre in profesor['asignaturas']:
            diccionario_profesores_ramos[(profesor['nombre'], ramo_nombre)] = 1
        else:
            diccionario_profesores_ramos[(profesor['nombre'], ramo_nombre)] = 0

# pprint(diccionario_profesores)
_, profesores_ensenan = multidict(diccionario_profesores_ramos)
_, profesores_horas = multidict(diccionario_profesores_ensenan)
# print(profesores_horas)


combinaciones_1 = []
for profesor in profesores.values():
    for curso in cursos:
        for ramo in ramos.values():
            for dia in dias:
                for mod in modulos:
                    combinaciones_1.append(
                        ((profesor['nombre'], curso, ramo, dia), mod))


combinaciones_1 = tuplelist(combinaciones_1)  # A

# print(len(profesores)*len(cursos)*len(dias)*len(ramos)*len(modulos))
# combinaciones_x = tuplelist(combinaciones_1) #A
# combinaciones_y = tuplelist(set(combinaciones_1)) #A
# print(len(combinaciones_x))
# print(len(combinaciones_y))


combinaciones_2 = []
for profesor in profesores.values():
    for ramo in ramos.values():
        for dia in dias:
            for mod in modulos:
                combinaciones_2.append(((profesor['nombre'], ramo), dia, mod))


combinaciones_2 = tuplelist(combinaciones_2)  # P

combinaciones_3 = tuplelist([i['nombre'] for i in profesores.values()])  # X

combinaciones_4 = tuplelist((i['nombre'], j)
                            for i in profesores.values() for j in dias)  # U

# ----------------------

# Modelo
m = Model('aaa')

# Variables
A = m.addVars(combinaciones_1, vtype=GRB.BINARY)
P = m.addVars(combinaciones_2, vtype=GRB.BINARY)
X = m.addVars(combinaciones_3, vtype=GRB.BINARY)
U = m.addVars(combinaciones_4, vtype=GRB.BINARY)


# se deben cambiar los id numericos a nombres para que se pueda
# acceder correctamente a los keys de los diccionarios
profesores = [prof['nombre'] for prof in profesores.values()]
ramos = [*ramos.values()]

# Función Objetivo
m.setObjective(quicksum(X[w] for w in combinaciones_3), GRB.MINIMIZE)

# un profesor no puede estar en dos lugares al mismo tiempo
m.addConstrs((
    quicksum(A[(p, c, r, t), m] for c in cursos for r in ramos) <= 1
    for t in dias for m in modulos for p in profesores),
    "R1")


m.addConstrs((
    (quicksum(A[(p, c, r, t), m] for c in cursos for r in ramos) +
     quicksum(P[(p, r), t, m] for r in ramos)) <= 1
    for t in dias for m in modulos for p in profesores),
    "R2")

m.addConstrs((
    ((quicksum(A[(p, c, r, t), 6] for c in cursos for r in ramos) +
      quicksum(P[(p, r), t, 6] for r in ramos) +
      quicksum(A[(p, c, r, t), 7] for c in cursos for r in ramos) +
      quicksum(P[(p, r), t, 7] for r in ramos))/2) >= U[(p, t)]
    for p in profesores for t in dias),
    "R3_1")

m.addConstrs((
    ((quicksum(A[(p, c, r, t), 6] for c in cursos for r in ramos) +
      quicksum(P[(p, r), t, 6] for r in ramos) +
      quicksum(A[(p, c, r, t), 7] for c in cursos for r in ramos) +
      quicksum(P[(p, r), t, 7] for r in ramos)) - 1) <= U[(p, t)]
    for p in profesores for t in dias),
    "R3_2")


m.addConstrs((
    (quicksum(A[(p, c, r, t), m] * 45
              for c in cursos for r in ramos for t in dias for m in modulos) +
     quicksum(P[(p, r), t, m] * 45
              for r in ramos for t in dias for m in modulos) +
     quicksum(U[(p, t)] * 45 for t in dias)) <=
    profesores_horas[(p)] * 60 for p in profesores),
    "R4")

m.addConstrs((
    quicksum(A[(p, c, r, t), m]
             for m in modulos for t in dias for p in profesores) ==
    horas_por_curso[(c, r)] for c in cursos for r in ramos),
    "R5")

# Optimize
m.optimize()
status = m.status
if status == GRB.Status.UNBOUNDED:
    print('The model cannot be solved because it is unbounded')
    exit(0)
if status == GRB.Status.OPTIMAL:
    print('The optimal objective is %g' % m.objVal)
    exit(0)
if status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
    print('Optimization was stopped with status %d' % status)
    exit(0)

# Relax the constraints to make the model feasible
print('The model is infeasible; relaxing the constraints')
orignumvars = m.NumVars
m.feasRelaxS(0, False, False, True)
m.optimize()
status = m.status
if status in (GRB.Status.INF_OR_UNBD, GRB.Status.INFEASIBLE, GRB.Status.UNBOUNDED):
    print('The relaxed model cannot be solved \
           because it is infeasible or unbounded')
    exit(1)

if status != GRB.Status.OPTIMAL:
    print('Optimization was stopped with status %d' % status)
    exit(1)

print('\nSlack values:')
slacks = m.getVars()[orignumvars:]
for sv in slacks:
    if sv.X > 1e-6:
        print('%s = %g' % (sv.VarName, sv.X))
