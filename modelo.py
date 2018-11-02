from gurobipy import *
from combinaciones import profesores_horas, profesores_ensenan, horas_por_curso, \
    profesores, ramos, dias, modulos, modulos_profes, cursos, combinaciones_1, \
    combinaciones_2, combinaciones_3, combinaciones_4, profesor_ramo,\
    ramos_seguidos, combinaciones_1_1
from pprint import pprint
from revision_restricciones import revisar_R5, revisar_restriccion_gobierno
from resultados.resultados import Escribidor


# ponderador es el 36 original de la restriccion 7
# originalmente es 36 por los 60 min * % de horas aulas que debe cumplir
# si se disminuye se hace mas estricta la restriccion
# el minimo valor del ponderador para que la funcion objetivo siga siendo 0
# es de 34.286 (se redondeo a 3 decimales). Esto equivale a 57.143333 %
ponderador = 34.286
print("\nPonderador de cumplimiento:", ponderador, "\n")


# Modelob
m = Model('Horarios profesores')

# Variables
A = m.addVars(combinaciones_1, vtype=GRB.BINARY)
A_1 = m.addVars(combinaciones_1_1, vtype=GRB.BINARY)
P = m.addVars(combinaciones_2, vtype=GRB.BINARY)
X = m.addVars(combinaciones_3, vtype=GRB.BINARY)
U = m.addVars(combinaciones_4, vtype=GRB.BINARY)


# se deben cambiar los id numericos a nombres para que se pueda
# acceder correctamente a los keys de los diccionarios
profesores = [prof['nombre'] for prof in profesores.values()]
ramos = [*ramos.values()]

# Función Objetivo
m.setObjective(quicksum(X[(p)] for p in profesores), GRB.MINIMIZE)
# m.setObjective(quicksum(P[(p, r), d, m] for p in profesores for r in ramos for d in dias for m in [8,9,10]), GRB.MINIMIZE)


# un profesor no puede estar en dos lugares al mismo tiempo

m.addConstrs((quicksum(A[(p, c, r, t), m] for r in ramos for c in cursos)
              <= 1 for p in profesores for m in modulos for t in dias), "R1")


# Si planifica no tiene hora aula a la vez
m.addConstrs((
    quicksum(A[(profesor, curso, ramo, dia), modulo]
             for curso in cursos for ramo in ramos)
    + quicksum(P[(profesor, ramo), dia, modulo] for ramo in ramos) <= 1
    for profesor in profesores
    for modulo in modulos
    for dia in dias),
    "R2")


# Definicion de variable para hora de almuerzo
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


# No trabajan mas horas de las que esta contratado
m.addConstrs((60 * (profesores_horas[(profesor)]-2) <= 45*quicksum(A[(profesor, curso, ramo, dia), modulo]
                                                                   for curso in cursos for ramo in ramos for dia in dias for modulo in modulos) +
              45*(quicksum(P[(profesor, ramo), dia, modulo_p]
                           for ramo in ramos for modulo_p in modulos_profes for dia in dias))
              + 45*quicksum(U[(profesor, dia)] for dia in dias) <= 60 * profesores_horas[(profesor)] for profesor in profesores),
             "R4")


# Cursos tienen los modulos requeridos

m.addConstrs((quicksum(A[(p, c, r, t), m]
                       for p in profesores
                       for t in dias
                       for m in modulos) == horas_por_curso[c, r]
              for r in ramos
              for c in cursos), "R5")


# R6

m.addConstrs((quicksum(A[(p, c, r, d), m] for m in modulos) <= 2
              for c in cursos
              for p in profesores
              for r in ramos_seguidos
              for d in dias), "R6")

# R7_1
m.addConstrs((X[(profesor)] <=
              (45*quicksum(A[(profesor, curso, ramo, dia), modulo]
                           for curso in cursos for ramo in ramos for dia in dias for modulo in modulos) +
               quicksum(U[(profesor, dia)] for dia in dias)) /
              (ponderador * profesores_horas[(profesor)])
              for profesor in profesores), "R7_1")


# R7_2
m.addConstrs((X[(profesor)] >= (45*quicksum(A[(profesor, curso, ramo, dia), modulo]
                                            for curso in cursos for ramo in ramos for dia in dias for modulo in modulos) +
                                quicksum(U[(profesor, dia)] for dia in dias) - (ponderador * profesores_horas[(profesor)]))/(36 * profesores_horas[(profesor)]) for profesor in profesores), "R7_2")

# R8_1
m.addConstrs((quicksum(A_1[(curso, ramo), profesor]
                       for profesor in profesores) <= 1
              for curso in cursos for ramo in ramos), "R8")

# R8_2
m.addConstrs((quicksum(A[(profesor, curso, ramo, dia), modulo]
                       for modulo in modulos for dia in dias) ==
              horas_por_curso[curso, ramo] * A_1[(curso, ramo), profesor]
              for profesor in profesores for ramo in ramos for curso in cursos), "R8_2")

# R9
m.addConstrs((quicksum(A[(profesor, curso, ramo, dia), modulo]
                       for ramo in ramos
                       for profesor in profesores) <= 1
              for curso in cursos for modulo in modulos for dia in dias), "R9")



# Experticia profesores: R10
# 10000000 es M muy grande
m.addConstrs((
    profesores_ensenan[(p, r)] * 10000000 >=
    quicksum(A[(p, c, r, t), m]
             for m in modulos for t in dias for c in cursos)
    for p in profesores for r in ramos),
    "R10")
