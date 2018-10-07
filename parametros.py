from parser_archivos import genera_profesores_dict, ramos_utiles
from pprint import pprint
from gurobipy import multidict
import csv

PROFESORES, RAMOS = genera_profesores_dict()

nivel = [str(i) for i in range(1, 9)]
letra_curso = ['A', 'B']


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
    for ramo in RAMOS.values():
        dict_retorno[(curso, ramo)] = int(horas_lvl[(int(curso[0]), ramo)])

pprint(dict_retorno)
