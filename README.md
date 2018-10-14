# Entrega 2 optimizacion


## Correr
- `python main.py`


## Consideraciones
- El modelo de la entrega 1 no consideraba dentro de los calculos las horas de planificacion, tratamos de arreglarlo para que si lo hiciera pero fue muy complicado.
- Ante esta situacion decidimos tomar un acercamiento heuristico, ya que nuestro modelo dejaba las horas libres en el horario de los profesores pero no pudimos meter directamente en el modelos las horas de planificacion necesarias.
- Entonces el procedimiento es el siguiente:

    1. Calcular los horarios de cada curso y profesor
    2. Con ese output ver que horarios les quedan libres a los profesores
    3. Rellenar con modulos de planificacion hasta que se cumpla la restriccion del gobierno
- Con este acercamiento logramos que todos los profesores cumplieran la normativa, sin tener que trabajar mas de lo que sale en su contrato (revisar poniendo el metodo `revisar_porcentajes` en `escribir_horarios_profes`, del archivo `resultados.py`)