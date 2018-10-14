from pandas import DataFrame, ExcelWriter
import os
import math

class Escribidor():
    def __init__(self, horas_aula, horas_planificacion, profesores, profesores_horas, path):
        self.horas_aula = horas_aula
        self.horas_planificacion = horas_planificacion
        self.profesores = profesores
        self.profesores_horas = profesores_horas
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
        self.lunes_profes = {prof: [""]*11 for prof in self.profesores}
        self.martes_profes = {prof: [""]*11 for prof in self.profesores}
        self.miercoles_profes = {prof: [""]*11 for prof in self.profesores}
        self.jueves_profes = {prof: [""]*11 for prof in self.profesores}
        self.viernes_profes = {prof: [""]*11 for prof in self.profesores}
        self.dias_profes = [self.lunes_profes,
                     self.martes_profes, 
                     self.miercoles_profes,
                     self.jueves_profes,
                     self.viernes_profes]

    def arreglar_planificaciones(self):
        """
        Actualmente, se esta demorando mucho en encontrar una solucion al incluir 
        las variables de planificacion, si estas se omiten (todavia cumpliendo 
        la restriccion del gobierno) y se agregan despues, completando horarios
        con planificaciones queda bien
        """
        horas_aula_profesores = {
            profesor: 0 for profesor in self.profesores_horas.keys()}
        for tupla in self.horas_aula:
            horas_aula_profesores[tupla[0][0]] += 1



        for prof in self.profesores:
                
            horas_contrato = self.profesores_horas[prof]
            horas_aula_tot = horas_aula_profesores[prof]
            horas_plan_necesarias = math.ceil((2/3)*horas_aula_tot)
            if horas_plan_necesarias > horas_contrato:
                print(f"profesor {prof} no cumple")

            listo = False
            i = 1
            for dia in self.dias_profes:
                if listo: 
                    break
                for mod in range(len(dia[prof])-3):
                    if dia[prof][mod] == "":
                        dia[prof][mod] = 'PLAN'
                        self.horas_planificacion.add((prof, i, mod))
                        horas_plan_necesarias -= 1
                        if horas_plan_necesarias <= 0:
                            listo = True
                            break
                i += 1

            i = 1
            if not listo:
                for dia in self.dias_profes:
                    if listo:
                        break
                    for mod in range(len(dia[prof]) - 3, len(dia[prof])):
                        if dia[prof][mod] == "":
                            dia[prof][mod] = 'PLAN'
                            self.horas_planificacion.add((prof, i, mod))
                            horas_plan_necesarias -= 1
                            if horas_plan_necesarias <= 0:
                                listo = True
                                break
                i += 1

    def revisar_porcentajes(self):
        horas_aula_profesores = {
            profesor: 0 for profesor in self.profesores_horas.keys()}
        horas_plan_profesores = {
            profesor: 0 for profesor in self.profesores_horas.keys()}
        for tupla in self.horas_aula:
            horas_aula_profesores[tupla[0][0]] += 1

        for tupla in self.horas_planificacion:
            horas_plan_profesores[tupla[0]] += 1

        for profesor, horas_contrato in self.profesores_horas.items():
            horas_plan = horas_plan_profesores[profesor]
            horas_aula = horas_aula_profesores[profesor]
            try:
                print(
                    f"""Profesor {profesor}:
                    Contrato: {(horas_contrato*60)/45} modulos
                    AULA: {horas_aula} modulos
                    PLAN: {horas_plan} modulos
                    %: {horas_plan/(horas_aula+horas_plan)} plan/(plan + aula)""")
            except ZeroDivisionError:
                print("No tiene horas aula ni plan ")


    def escribir_horarios_profes(self):
        for tupla in self.horas_aula:
            prof, curso, ramo, dia = tupla[0]
            modulo = tupla[1]
            if dia == 1:
                self.lunes_profes[prof][modulo-1] += curso 
            elif dia == 2:
                self.martes_profes[prof][modulo-1] += curso 
            elif dia == 3:
                self.miercoles_profes[prof][modulo-1] += curso 
            elif dia == 4:
                self.jueves_profes[prof][modulo-1] += curso 
            elif dia == 5:
                self.viernes_profes[prof][modulo-1] += curso 
        

        for tupla in self.horas_planificacion:
            prof = tupla[0]
            dia = tupla[1]
            modulo = tupla[2]
            if dia == 1:
                self.lunes_profes[prof][modulo-1] += "PLAN" 
            elif dia == 2:
                self.martes_profes[prof][modulo-1] += "PLAN" 
            elif dia == 3:
                self.miercoles_profes[prof][modulo-1] += "PLAN" 
            elif dia == 4:
                self.jueves_profes[prof][modulo-1] += "PLAN" 
            elif dia == 5:
                self.viernes_profes[prof][modulo-1] += "PLAN" 

        self.arreglar_planificaciones()
        self.revisar_porcentajes()

        dfs = {}
        for prof in self.profesores:
            dfs[prof] = DataFrame({'LUNES': self.lunes_profes[prof],
                                    'MARTES': self.martes_profes[prof],
                                    'MIERCOLES': self.miercoles_profes[prof],
                                    'JUEVES': self.jueves_profes[prof], 
                                    'VIERNES': self.viernes_profes[prof]})
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
                lunes[curso][modulo-1] += ramo 
            elif dia == 2:
                martes[curso][modulo-1] += ramo 
            elif dia == 3:
                miercoles[curso][modulo-1] += ramo 
            elif dia == 4:
                jueves[curso][modulo-1] += ramo 
            elif dia == 5:
                viernes[curso][modulo-1] += ramo 

        dfs = {}
        for curso in self.cursos:
            dfs[curso] = DataFrame({'LUNES': lunes[curso], 'MARTES': martes[curso], 'MIERCOLES': miercoles[curso],
                                    'JUEVES': jueves[curso], 'VIERNES': viernes[curso]})
            dfs[curso].to_excel(self.writer, curso)
            self.writer.save()
