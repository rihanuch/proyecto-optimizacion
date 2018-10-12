from pandas import DataFrame, ExcelWriter

aa = [(('PROF_A', '5A', 'LENGUAJE', 3), 4),
      (('PROF_A', '5A', 'LENGUAJE', 3), 6),
      (('PROF_A', '5B', 'LENGUAJE', 2), 3),
      (('PROF_A', '6A', 'LENGUAJE', 2), 4),
      (('PROF_A', '6A', 'LENGUAJE', 3), 5),
      (('PROF_A', '6B', 'LENGUAJE', 2), 2),
      (('PROF_A', '6B', 'LENGUAJE', 4), 3),
      (('PROF_A', '7B', 'LENGUAJE', 1), 7),
      (('PROF_B', '5A', 'LENGUAJE', 2), 1),
      (('PROF_B', '5B', 'LENGUAJE', 2), 7),
      (('PROF_B', '7A', 'LENGUAJE', 1), 1),
      (('PROF_B', '7A', 'LENGUAJE', 2), 3),
      (('PROF_B', '7A', 'LENGUAJE', 3), 6),
      (('PROF_B', '7A', 'LENGUAJE', 4), 6),
      (('PROF_B', '7B', 'LENGUAJE', 2), 4),
      (('PROF_B', '7B', 'LENGUAJE', 3), 1),
      (('PROF_B', '7B', 'LENGUAJE', 3), 3),
      (('PROF_B', '8A', 'LENGUAJE', 1), 2),
      (('PROF_B', '8A', 'LENGUAJE', 1), 7),
      (('PROF_B', '8A', 'LENGUAJE', 2), 5),
      (('PROF_B', '8A', 'LENGUAJE', 4), 2),
      (('PROF_C', '5A', 'LENGUAJE', 4), 5),
      (('PROF_C', '5B', 'LENGUAJE', 3), 2),
      (('PROF_C', '5B', 'LENGUAJE', 4), 6),
      (('PROF_C', '6A', 'LENGUAJE', 1), 1),
      (('PROF_C', '6A', 'LENGUAJE', 3), 4),
      (('PROF_C', '6B', 'LENGUAJE', 2), 7),
      (('PROF_C', '6B', 'LENGUAJE', 3), 5),
      (('PROF_C', '8B', 'LENGUAJE', 1), 6),
      (('PROF_C', '8B', 'LENGUAJE', 1), 7),
      (('PROF_C', '8B', 'LENGUAJE', 4), 2),
      (('PROF_C', '8B', 'LENGUAJE', 5), 4)]


def escribir_resultados(horas_aula):
    lunes = [""]*8
    martes = [""]*8
    miercoles = [""]*8
    jueves = [""]*8
    viernes = [""]*8
    for tupla in horas_aula:
        prof, curso, ramo, dia = tupla[0]
        modulo = tupla[1]
        if dia == 1:
            lunes[modulo-1] += prof + curso + '; '
        elif dia == 2:
            martes[modulo-1] += prof + curso + '; '
        elif dia == 3:
            miercoles[modulo-1] += prof + curso + '; '
        elif dia == 4:
            jueves[modulo-1] += prof + curso + '; '
        elif dia == 5:
            viernes[modulo-1] += prof + curso + '; '

    df = DataFrame({'LUNES': lunes, 'MARTES': martes, 'MIERCOLES': miercoles,
                    'JUEVES': jueves, 'VIERNES': viernes})

    writer = ExcelWriter('resultados.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()

