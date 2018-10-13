# coding: UTF-8

import csv
from pprint import pprint
from random import choice


RAMOS_EQUIVALENTES = {
    'Soporte tec': 'TECNOLOGÍA',
    'JEFA UTP': 'JEFA UTP',
    'PAE SALUD': 'PAE SALUD',
    'LENGUAJE': 'LENGUAJE',
    'Monitora 2°': 'Monitora',
    'ED FÍSICA': 'EDUCACIÓN FÍSICA',
    'EDUCACIÓN FÍSICA': 'EDUCACIÓN FÍSICA',
    'DIRECTORA': 'TECNOLOGÍA',
    'TECNOLOGÍA': 'TECNOLOGÍA',
    'Refuerzo SEP': 'REFUERZO SEP',
    'CRA': 'CRA',
    'Sicóloga': 'SICÓLOGA',
    'Cocina': 'COCINA',
    'Sec Dirección': 'SECRETARIA DIRECCIÓN',
    'C NATURALES': 'CIENCIAS NATURALES',
    'EDUCADORA': 'ORIENTACIÓN',
    'RELIGIÓN': 'RELIGIÓN',
    'Baile': 'BAILE',
    'ARTE': 'ARTE',
    'HISTORIA': 'HISTORIA',
    'MATEMÁTICA': 'MATEMÁTICA',
    'GENERAL BÁSICO': 'GENERAL BÁSICO',
    'Sec UTP': 'SECRETARIA UTP',
    'CONVIV ESCOLAR': 'ORIENTACIÓN',
    'ORIENTACIÓN': 'ORIENTACIÓN',
    'Técnico en párvulos': 'TÉCNICO EN PÁRVULOS',
    'HISTORIA ENLACES': 'HISTORIA',
    'MÚSICA': 'MÚSICA',
    'Monitora 1°': 'Monitora',
    'INGLÉS': 'INGLÉS',
    'Monitora 4°': 'Monitora',
    'Monitora 3°': 'Monitora',
    'Trab Social': 'TRABAJO SOCIAL',
    'CIENCIAS NATURALES': 'CIENCIAS NATURALES'
}


PLAN = 'datos/plan.csv'
# plan.csv es el que dan
# plan_2.csv es uno propuesto mas dificil


def vacio_a_cero(horas):
    try:
        return int(horas)
    except ValueError:
        return 0


def asignaturas_existentes():
    ramos = set()
    with open(PLAN, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            temp = parse_asignaturas(row['Asignatura'])
            if temp != []:
                for ramo in temp:
                    ramos.add(ramo)
    return ramos


def parse_asignaturas(ramos):
    ramos = [ramo.strip() for ramo in ramos.split(',')]
    if ramos == ['']:
        ramos = []
    return ramos


def mapea_asignatura(ramos):
    ramos = parse_asignaturas(ramos)
    return [RAMOS_EQUIVALENTES[ramo] for ramo in ramos]


def crea_prof(kwargs):
    kwargs = {elem: kwargs[elem].strip() for elem in kwargs}
    profesor = {
        'id': '',
        'rut': kwargs['Rut'],
        'nombre': kwargs['Nombre'].replace('  ', ' '),
        'tipo': kwargs['Tipo de Funcionario'],
        'cargo': kwargs['Cargo'],
        'asignaturas': mapea_asignatura(kwargs['Asignatura']),
        'nivel': kwargs['Nivel'],
        'hpa': vacio_a_cero(kwargs['Horas Plan/Aula']),
        'hc': vacio_a_cero(kwargs['Horas Contrato']),
        'hsep': vacio_a_cero(kwargs['Horas SEP']),
        'hpie': vacio_a_cero(kwargs['Horas PIE']),
        'hd': vacio_a_cero(kwargs['Horas Directivas']),
        'ht': vacio_a_cero(kwargs['Total Horas'])
    }
    return profesor


def profs_csv(profs):
    prof_return = []
    for profesor in profs:
        profesor['asignaturas'] = ','.join(profesor['asignaturas'])
        prof_return.append(profesor)
    return prof_return


def genera_profesores():
    profesores = []
    with open(PLAN, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            profesores.append(crea_prof(row))
    return list(filter(lambda profesor: profesor['rut'] != '', profesores))


def exporta_profesores():
    with open('datos/profesores.csv', 'w', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        headers = [
            'id',
            'rut',
            'nombre',
            'tipo',
            'cargo',
            'asignaturas',
            'nivel',
            'hpa',
            'hc',
            'hsep',
            'hpie',
            'hd',
            'ht'
        ]
        spamwriter.writerow(headers)
        profs = profs_csv(genera_profesores())
        for idp, profesor in enumerate(profs):
            profesor['id'] = idp
            spamwriter.writerow([profesor[head] for head in headers])


def exporta_ramos():
    with open('datos/ramos.csv', 'w', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        headers = [
            'id',
            'ramo'
        ]
        spamwriter.writerow(headers)
        ramos = ramos_utiles()

        for idp, ramo in ramos.items():
            spamwriter.writerow([idp, ramo])


def ramos_utiles():
    r_utiles = {}

    with open('datos/horas.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for _id, row in enumerate(reader):
            r_utiles[_id] = row['\ufefframo']

    return r_utiles


def genera_ramos():
    ramos = set()
    for ramo in RAMOS_EQUIVALENTES:
        ramos.add(RAMOS_EQUIVALENTES[ramo])
    return ramos


def genera_profesores_dict():
    profesores = genera_profesores()

    ramos = ramos_utiles()

    # r_reversos = {v: k for k, v in ramos.items()}

    for profesor in profesores:
        profesor.pop('id')
        asig = []
        for ramo in profesor['asignaturas']:
            if ramo in ramos.values():
                asig.append(ramo)
        profesor['asignaturas'] = asig

    profesores = list(
        filter(lambda prof: prof['asignaturas'] != [], profesores))

    profesores = {_id: profesor for _id, profesor in enumerate(profesores)}

    return profesores, ramos


if __name__ == '__main__':
    exporta_profesores()
    exporta_ramos()
