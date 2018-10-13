from pandas import DataFrame, ExcelWriter
import os
# TODO:PASAR profesores COMO PARAMETROS


class Escribidor():
    def __init__(self, horas_aula, horas_planificacion, profesores, path):
        self.horas_aula = horas_aula
        self.horas_planificacion = horas_planificacion
        self.profesores = profesores
        self.cursos = []
        self.writer = ExcelWriter(path)
        self.cargar_datos_basicos()

        os.remove('resultados/resultados.xlsx')


    def cargar_datos_basicos(self):
        letras = ["A", "B"]
        niveles = [i for i in range(1, 9)]
        for i in letras:
            for j in niveles:
                self.cursos.append(str(j)+i)

    def arreglar_planificaciones(self):
        """
        Actualmente, se esta demorando mucho en encontrar una solucion al incluir 
        las variables de planificacion, si estas se omiten (todavia cumpliendo 
        la restriccion del gobierno) y se agregan despues, completando horarios
        con planificaciones queda bien
        """
        pass

    def escribir_horarios_profes(self):
        lunes = {prof: [""]*8 for prof in self.profesores}
        martes = {prof: [""]*8 for prof in self.profesores}
        miercoles = {prof: [""]*8 for prof in self.profesores}
        jueves = {prof: [""]*8 for prof in self.profesores}
        viernes = {prof: [""]*8 for prof in self.profesores}

        for tupla in self.horas_aula:
            prof, curso, ramo, dia = tupla[0]
            modulo = tupla[1]
            if dia == 1:
                lunes[prof][modulo-1] += curso + '; '
            elif dia == 2:
                martes[prof][modulo-1] += curso + '; '
            elif dia == 3:
                miercoles[prof][modulo-1] += curso + '; '
            elif dia == 4:
                jueves[prof][modulo-1] += curso + '; '
            elif dia == 5:
                viernes[prof][modulo-1] += curso + '; '


        # A estos diccionarios de dias falta agregarle las horas de planificacion
        dfs = {}
        for prof in self.profesores:
            dfs[prof] = DataFrame({'LUNES': lunes[prof], 'MARTES': martes[prof],
                                    'MIERCOLES': miercoles[prof],
                                    'JUEVES': jueves[prof], 'VIERNES': viernes[prof]})
            dfs[prof].to_excel(self.writer, prof)
            self.writer.save()



    def escribir_horarios_cursos(self):

        lunes = {curso: [""]*8 for curso in self.cursos}
        martes = {curso: [""]*8 for curso in self.cursos}
        miercoles = {curso: [""]*8 for curso in self.cursos}
        jueves = {curso: [""]*8 for curso in self.cursos}
        viernes = {curso: [""]*8 for curso in self.cursos}

        for tupla in self.horas_aula:
            prof, curso, ramo, dia = tupla[0]
            modulo = tupla[1]
            if dia == 1:
                lunes[curso][modulo-1] += ramo + '; '
            elif dia == 2:
                martes[curso][modulo-1] += ramo + '; '
            elif dia == 3:
                miercoles[curso][modulo-1] += ramo + '; '
            elif dia == 4:
                jueves[curso][modulo-1] += ramo + '; '
            elif dia == 5:
                viernes[curso][modulo-1] += ramo + '; '

        dfs = {}
        for curso in self.cursos:
            dfs[curso] = DataFrame({'LUNES': lunes[curso], 'MARTES': martes[curso], 'MIERCOLES': miercoles[curso],
                                    'JUEVES': jueves[curso], 'VIERNES': viernes[curso]})
            dfs[curso].to_excel(self.writer, curso)
            self.writer.save()
