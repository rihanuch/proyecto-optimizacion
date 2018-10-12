from faker import Faker
from random import choice, randint

RAMOS_EQUIVALENTES = {
    # 'Soporte tec': 'TECNOLOGÍA',
    # 'JEFA UTP': 'MÚSICA',
    'LENGUAJE': 'LENGUAJE',
    # 'Monitora 2°': 'INGLÉS',  # cambio de monitora a ingles
    'ED FÍSICA': 'EDUCACIÓN FÍSICA',
    # 'Refuerzo SEP': 'GENERAL BÁSICO',  # cambio de refuerzo a general basico
    # 'CRA': 'INGLÉS',
    # 'ORIENTACIÓN': 'ORIENTACIÓN',
    # 'Sicóloga': 'ORIENTACIÓN',
    'C NATURALES': 'CIENCIAS NATURALES',
    # 'EDUCADORA': 'ORIENTACIÓN',
    'RELIGIÓN': 'RELIGIÓN',
    'ARTE': 'ARTE',
    # 'HISTORIA': 'HISTORIA',
    'MATEMÁTICA': 'MATEMÁTICA',
    'GENERAL BÁSICO': 'GENERAL BÁSICO',
    # 'CONVIV ESCOLAR': 'ORIENTACIÓN',
    # 'Técnico en párvulos': 'HISTORIA',
    # 'HISTORIA ENLACES': 'HISTORIA',
    'MÚSICA': 'MÚSICA',
    # 'Monitora 1°': 'INGLÉS',  # cambio de monitora a ingles
    'INGLÉS': 'INGLÉS',
    # 'Monitora 4°': 'MÚSICA',  # cambio de monitora a musica
    # 'Monitora 3°': 'ARTE',  # cambio de monitora a arte
    # 'Trab Social': 'ORIENTACIÓN'
}


fake = Faker('es_ES')
# for i in range(130, 151):
#     print(str(i) + ";0;"+fake.name()+";0;0;" +
#           choice(list(RAMOS_EQUIVALENTES.keys()))+";0;0;0;0;0;0;"+str(randint(20, 40))+";0")


def generador_profesor(i):
    # return str(i) + ";0;"+fake.name()+";0;0;" + choice(list(RAMOS_EQUIVALENTES.keys())) + ";0;0;0;0;0;0;"+str(randint(40, 60))+";0"
    return str(i) + ";0;"+ f"PROF_{str(i)}"+";0;0;" + "LENGUAJE" + ";0;0;0;0;0;0;"+str(randint(30, 40))+";0"
# N°;Rut;Nombre;Tipo de Funcionario;Cargo;Asignatura;Nivel;Horas Plan/Aula;Horas Contrato;Horas SEP;Horas PIE;Horas Directivas;Total Horas;Observaciones
