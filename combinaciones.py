# DEFINIR PARAMETROS
from gurobipy import *
from parser_archivos import genera_profesores_dict
from pprint import pprint
import csv

profesores, ramos = genera_profesores_dict()
ramos_seguidos = ['ARTE', 'MÚSICA',
                  'EDUCACIÓN FÍSICA', 
                  'ORIENTACIÓN',
                  'TECNOLOGÍA',
                  'RELIGIÓN']
nivel = [str(i) for i in range(1, 9)]
letra_curso = ["A", "B"]

cursos = [i + j for i in nivel for j in letra_curso]

modulos = [i for i in range(1, 9)]
dias = [i for i in range(1, 6)]

# Para excel
profesor_ramo = {i['nombre']: i['asignaturas'] for i in profesores.values()}


def horas_nivel():
    retorno = {}
    with open('datos/horas.csv', encoding='utf-8') as f:
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


# Todos los pares profesores con las horas que estan contratados
diccionario_profesores_ramos = {}
# Todas las tuplas profesor - ramo con 1 si ensena ese ramo
diccionario_profesores_ensenan = {}


for id_, profesor in profesores.items():
    for ramo_nombre in ramos.values():
        diccionario_profesores_ensenan[profesor['nombre']] = profesor['ht']

        if ramo_nombre in profesor['asignaturas']:
            diccionario_profesores_ramos[(profesor['nombre'], ramo_nombre)] = 1
        else:
            diccionario_profesores_ramos[(profesor['nombre'], ramo_nombre)] = 0



_, profesores_ensenan = multidict(diccionario_profesores_ramos)
_, profesores_horas = multidict(diccionario_profesores_ensenan)


combinaciones_1 = []
for profesor in profesores.values():
    for curso in cursos:
        for ramo in ramos.values():
            for dia in dias:
                for mod in modulos:
                    combinaciones_1.append(
                        ((profesor['nombre'], curso, ramo, dia), mod))


combinaciones_1 = tuplelist(combinaciones_1)


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
