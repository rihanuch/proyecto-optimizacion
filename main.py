from modelo import m, profesores, profesores_horas, X, A, P
from gurobipy import *
from resultados.resultados import Escribidor

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
    horas_planificacion = [(a[0][0], a[1], a[2])
                           for a, b in P.items() if b.X == 1]

    no_cumplen = [a for a, b in X.items() if b.X == 1]

    # Necesita libreria pandas y sus requerimientos
    # Borra el archivo anterior
    escribidor = Escribidor(horas_aula, set(horas_planificacion),
                            profesores, profesores_horas, 'resultados/resultados.xlsx')

    escribidor.escribir_horarios_cursos()
    escribidor.escribir_horarios_profes()
