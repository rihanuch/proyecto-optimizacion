from pprint import pprint
from combinaciones import diccionario_profesores_ramos, diccionario_profesores_ensenan, horas_por_curso
from parser_archivos import  genera_profesores_dict
import csv
from persons import generador_profesor
# diccionario_profesores_ramos = horas contratado {prof: horas contratado}
# diccionario_profesores_ensenan = dicta el ramo o no {(prof, ramo): 0 - 1}
# horas_por_curso {(curso, ramo): horas que necesita}

profesores, ramos = genera_profesores_dict()

horas_por_ramo_total_necesitan = {ramo: 0 for ramo in ramos.values()}  # Horas que se necesitan por ramo de profesores
horas_por_curso_total_necesitan = {} # Horas que necesita cada ramo

horas_por_ramo_total_tiene = {ramo: 0 for ramo in ramos.values()}  # Horas que se tienen contratadas por ramo




for tupla, horas in horas_por_curso.items():
    curso, ramo = tupla


    try:
        horas_por_ramo_total_necesitan[ramo] += horas
    except KeyError:
        horas_por_ramo_total_necesitan[ramo] = horas

    try:
        horas_por_curso_total_necesitan[curso] += horas
    except KeyError:
        horas_por_curso_total_necesitan[curso] = horas

for profesor in profesores.values():
    ramo = profesor['asignaturas'][0]
    horas_por_ramo_total_tiene[ramo] += profesor['ht']



def generar_profesores_a_csv(numero):
    with open('plan_2.csv', 'w', encoding='utf-8') as csvfile:
        # spamwriter = csv.writer(csvfile, delimiter=';')
        headers = [
            "N°",
            "Rut",
            "Nombre",
            "Tipo de Funcionario",
            'Cargo',
            "Asignatura",
            'Nivel',
            "Horas Plan/Aula",
            "Horas Contrato",
            'Horas SEP',
            "Horas PIE",
            "Horas Directivas",
            'Total Horas',
            "Observaciones"
        ]
        # spamwriter.writerow(headers)
        csvfile.write(';'.join(headers))
        csvfile.write('\n')
        for i in range(1, numero + 1):
            csvfile.write(generador_profesor(i))
            csvfile.write("\n")

def revisar_R5(vector_A, horas_por_curso):
    # primero, ver cuantas horas de cada ramo tiene cada curso
    x_filtrados = [a for a, b in vector_A.items() if b.X == 1]
    horas_tienen = {}
    for par in horas_por_curso.keys(): 
        # tuplas (curso, ramo)
        horas_tienen[par] = 0
        for total in x_filtrados:
            if total[0][1] == par[0] and total[0][2] == par[1]:
                horas_tienen[par] += 1

        # print(par[1])
        if par[1] == "TECNOLOGÍA":
            print("NECESITAN: ", par, horas_por_curso[par])
            print("TIENEN: ", par, horas_tienen[par])
        if horas_por_curso[par] != horas_tienen[par]:
            print(f"{par} no cumple las restricciones")


def revisar_horas_exactas(horas_por_curso_total_necesitan):

    print(horas_por_curso_total_necesitan)


def revisar_restriccion_gobierno(profesores_horas, horas_aula, horas_planificacion):
    
    horas_aula_profesores = {profesor: 0 for profesor in profesores_horas.keys()}
    horas_plan_profesores = {profesor: 0 for profesor in profesores_horas.keys()}
    for tupla in horas_aula:
        horas_aula_profesores[tupla[0][0]] += 1
     
    for tupla in horas_planificacion:
        horas_plan_profesores[tupla[0]] += 1
     


    for profesor, horas_contrato in profesores_horas.items():
        horas_plan = horas_plan_profesores[profesor]
        horas_aula = horas_aula_profesores[profesor]
        try:
            print(
                f"""Profesor {profesor}:
                Contrato: {(profesores_horas[profesor]*60)/45}
                AULA: {horas_aula}
                PLAN: {horas_plan}
                %: {horas_plan/(horas_aula+horas_plan)}""")
        except ZeroDivisionError:
            print("No tiene horas aula ni plan ")

if __name__ == "__main__":
    # generar_profesores_a_csv(4)
    # pprint(profesores)

    revisar_horas_exactas(horas_por_curso_total_necesitan)
    
    # for i in ramos.values():
        # print(
            # f"{i}: Necesita: {horas_por_ramo_total_necesitan[i]} Tiene: {horas_por_ramo_total_tiene[i]}")
    # pprint(sum(i for _,i in horas_por_ramo_total_necesitan.items()))
