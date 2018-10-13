from gurobipy import *
from combinaciones import profesores_horas, profesores_ensenan, horas_por_curso, \
    profesores, ramos, dias, modulos, cursos, combinaciones_1, \
    combinaciones_2, combinaciones_3, combinaciones_4, profesor_ramo,\
    ramos_seguidos
from pprint import pprint
from revision_restricciones import revisar_R5, revisar_restriccion_gobierno
from resultados.resultados import Escribidor


# Modelob
m = Model('Horarios profesores')

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
m.setObjective(quicksum(X[(p)] for p in profesores), GRB.MINIMIZE)


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
              45*(quicksum(P[(profesor, ramo), dia, modulo]
                           for ramo in ramos for modulo in modulos for dia in dias))
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
# m.addConstrs((A[(p, c, r, d), m] == A[(p, c, r, d), m+1]
#               for p in profesores 
#               for c in cursos 
#               for r in ramos_seguidos 
#               for d in dias 
#               for m in modulos[:-1]), "R6_1")

m.addConstrs((quicksum(A[(p, c, r, d), m] for m in modulos) <= 2
            for c in cursos
            for p in profesores
            for r in ramos_seguidos
            for d in dias), "R6_2")



# R7_1 original
m.addConstrs((X[(profesor)] <=
              (45*quicksum(A[(profesor, curso, ramo, dia), modulo]
                           for curso in cursos for ramo in ramos for dia in dias for modulo in modulos) +
               quicksum(U[(profesor, dia)] for dia in dias)) /
              (36 * profesores_horas[(profesor)])
              for profesor in profesores), "R7_1")


# R7_1 arreglada, tiempo infinito
# m.addConstrs((X[(p)] <=
#             45*(
#                 quicksum(A[(p,c,r,d), m] 
#                     for c in cursos
#                     for r in ramos
#                     for d in dias
#                     for m in modulos)
#                 +
#                 quicksum(U[(p, d)]
#                     for d in dias)
#             )/
#             36*(
#                 quicksum(A[(p, c, r, d), m]
#                          for c in cursos
#                          for r in ramos
#                          for d in dias
#                          for m in modulos)
#                 +
#                 quicksum(U[(p, d)]
#                          for d in dias)
#                 + 
#                 quicksum(P[(p,r), d, m] 
#                 for r in ramos
#                 for d in dias
#                 for m in modulos)
#             )            

#             for p in profesores
#             ), "R7_1")



# R7_2
m.addConstrs((X[(profesor)] >= (45*quicksum(A[(profesor, curso, ramo, dia), modulo]
                                            for curso in cursos for ramo in ramos for dia in dias for modulo in modulos) +
                                quicksum(U[(profesor, dia)] for dia in dias) - (36 * profesores_horas[(profesor)]))/(36 * profesores_horas[(profesor)]) for profesor in profesores), "R7_2")

# Se deberia arreglar un R7_2 arreglado tambien



# Esta R8 esta mala, pero puede aceptarse que un curso tenga 2 profesores distintos de matematicas
# m.addConstrs((
#     quicksum(A[(p, c, r, t), m]
#              for m in modulos for t in dias for p in profesores) == 1
#     for c in cursos for r in ramos),
#     "R8")

# R9
m.addConstrs((quicksum(A[(profesor, curso, ramo, dia), modulo]
                       for ramo in ramos
                       for profesor in profesores) <= 1
              for curso in cursos for modulo in modulos for dia in dias), "R9")


# Experticia profesores
# 10000000 es M muy grande
m.addConstrs((
    profesores_ensenan[(p, r)] * 10000000 >=
    quicksum(A[(p, c, r, t), m]
             for m in modulos for t in dias for c in cursos)
    for p in profesores for r in ramos),
    "R10")



# Nueva restriccion, podria areglar lo de las horas de planificacion, no se si 
# hay algo malo con horas/minutos pero no funciona
# m.addConstrs((
#             45*quicksum(P[(p, r), d, m]
#                         for r in ramos
#                         for d in dias
#                         for m in modulos)
#             >=
#             0.6*60*profesores_horas[(p)]

#             for p in profesores
#         ), "Rx")






if __name__ == '__main__':
    # Optimize
    m.optimize()
    status = m.status
    if status == GRB.Status.UNBOUNDED:
        print('The model cannot be solved because it is unbounded')
    if status == GRB.Status.OPTIMAL:
        print('The optimal objective is %g' % m.objVal)
    if status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
        print('Optimization was stopped with status %d' % status)

    horas_aula = [a for a, b in A.items() if b.X == 1]  # Debe ser 528
    horas_planificacion = [a for a, b in P.items() if b.X == 1]
    no_cumplen = [a for a, b in X.items() if b.X == 1]
    
    
    # print(no_cumplen)
    print(horas_planificacion) # Ahora esta dando una lista vacia

    revisar_restriccion_gobierno(profesores_horas, horas_aula)



    # Necesita libreria pandas y sus requerimientos
    # Borra el archivo anterior
    escribidor = Escribidor(horas_aula, horas_planificacion,
                            profesores, 'resultados/resultados.xlsx')

    escribidor.escribir_horarios_cursos()
    escribidor.escribir_horarios_profes()

 
