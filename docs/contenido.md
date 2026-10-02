# Sistema difuso de propensión al infarto

Diseño académico con peso y edad mediante inferencia Mamdani  
Estudiante: Juan Esteban Ortiz Rendón  
Docente: Carlos Alberto Valencia Hernández  
Asignatura: Seminario IA  
Universidad Autónoma Latinoamericana  
Fecha: 2 de octubre de 2026

> Uso exclusivamente académico. El índice no es una probabilidad clínica, no es un diagnóstico y no orienta tratamientos.

## 1. Análisis del problema

Se plantea un sistema de lógica difusa que recibe peso y edad y devuelve un índice entre 0 y 100. El objetivo es demostrar el proceso completo de diseño: definir rangos y conjuntos, calcular pertenencias, aplicar reglas, agregar sus consecuencias y obtener una salida numérica mediante el centroide.

El enunciado de clase denomina la salida probabilidad de infarto. En esta implementación se presenta como índice académico de propensión, porque las reglas y los puntos de corte son supuestos didácticos, no una estimación clínica calibrada. No permite diagnosticar, recomendar tratamientos ni interpretar 70 puntos como un 70 % de probabilidad real.

## 2. Alcance y decisiones de diseño

Se adoptan los rangos sugeridos en clase: peso de 0 a 200 kg y edad de 0 a 120 años. Los extremos se conservan para comprobar cobertura matemática; no implican que toda combinación represente una persona real. El modelo usa únicamente estas dos entradas y no incorpora altura, historia clínica u otras variables.

Los nombres ligero, intermedio y elevado describen categorías internas de peso absoluto, no diagnósticos de bajo peso, peso saludable u obesidad. Las categorías de edad también son etiquetas del ejercicio. Las funciones y reglas siguientes son una propuesta propia y no valores dictados por el profesor.

La entrega incluye diseño, matriz completa, nueve reglas expresadas en código y validación numérica del motor. La interfaz implementada genera las visualizaciones desde el motor real; las capturas solo se consideran evidencia cuando hayan sido obtenidas de una ejecución real.

## 3. Variables y funciones de membresía

| Variable | Rol y rango | Conjuntos |
|---|---|---|
| Peso | Entrada de 0 a 200 kg | Ligero, intermedio, elevado |
| Edad | Entrada de 0 a 120 años | Joven, adulta, mayor |
| Índice de propensión | Salida de 0 a 100 puntos | Bajo, medio, alto |

Una función de membresía asigna a cada valor un grado μ entre 0 y 1. Por ejemplo, μ = 0,4 significa pertenencia parcial a una categoría, no una probabilidad del 40 %. Un mismo valor puede activar dos conjuntos a la vez.

Triangular `[a, b, c]`: vale 0 en a y c, crece linealmente hasta 1 en b y luego disminuye. Trapezoidal `[a, b, c, d]`: crece de 0 a 1 entre a y b, permanece en 1 entre b y c y cae a 0 entre c y d. Fuera de sus límites vale 0. Si a = b se usa un hombro izquierdo; si c = d se usa un hombro derecho, sin divisiones por cero.

| Variable | Conjunto | Función | Parámetros exactos |
|---|---|---|---|
| Peso | Ligero | Trapezoidal | [0, 0, 50, 70] |
| Peso | Intermedio | Triangular | [50, 75, 100] |
| Peso | Elevado | Trapezoidal | [80, 110, 200, 200] |
| Edad | Joven | Trapezoidal | [0, 0, 25, 40] |
| Edad | Adulta | Triangular | [30, 50, 70] |
| Edad | Mayor | Trapezoidal | [60, 80, 120, 120] |
| Índice | Bajo | Trapezoidal | [0, 0, 20, 40] |
| Índice | Medio | Triangular | [30, 50, 70] |
| Índice | Alto | Trapezoidal | [60, 80, 100, 100] |

Se utilizan trapecios en los extremos para mantener cobertura hasta los límites y triángulos en el centro para representar pertenencia gradual. Los solapamientos evitan saltos de categoría y zonas sin reglas activas. El peso acepta valores decimales y la edad acepta únicamente años enteros entre 0 y 120; no se redondea silenciosamente una edad fraccionaria.

## 4. Gráficas del diseño difuso

Las tres gráficas interactivas que aparecen antes de este contenido se generan desde las definiciones reales de `model/config.py` mediante `model/membership.py`; no son imágenes ni tablas de demostración.

Lectura: ubicar el valor en el eje horizontal y leer la altura de cada curva. A 90 kg, la pertenencia a intermedio es 0,4 y a elevado es 0,3333. Ambas intervienen en las reglas; sus grados no tienen que sumar 1.

## 5. Matriz difusa y reglas de producción

Las filas corresponden a los conjuntos de peso y las columnas a los de edad. Cada cruce define el consecuente de una regla. Hay 3 × 3 = 9 reglas y todas tienen peso 1.

| Peso y edad | Joven | Adulta | Mayor |
|---|---|---|---|
| Ligero | Bajo · R1 | Medio · R2 | Alto · R3 |
| Intermedio | Bajo · R4 | Medio · R5 | Alto · R6 |
| Elevado | Medio · R7 | Alto · R8 | Alto · R9 |

- R1. SI el peso es ligero Y la edad es joven, ENTONCES el índice es bajo.
- R2. SI el peso es ligero Y la edad es adulta, ENTONCES el índice es medio.
- R3. SI el peso es ligero Y la edad es mayor, ENTONCES el índice es alto.
- R4. SI el peso es intermedio Y la edad es joven, ENTONCES el índice es bajo.
- R5. SI el peso es intermedio Y la edad es adulta, ENTONCES el índice es medio.
- R6. SI el peso es intermedio Y la edad es mayor, ENTONCES el índice es alto.
- R7. SI el peso es elevado Y la edad es joven, ENTONCES el índice es medio.
- R8. SI el peso es elevado Y la edad es adulta, ENTONCES el índice es alto.
- R9. SI el peso es elevado Y la edad es mayor, ENTONCES el índice es alto.

La matriz supone, con fines didácticos, una salida mayor al pasar a categorías de edad mayores y una penalización adicional para peso elevado. No se atribuye a esta matriz validez médica. La repetición de consecuencias es intencional: varias combinaciones pueden recomendar el mismo conjunto de salida.

Las nueve tuplas `RULES` del código constituyen la representación ejecutable de estos cruces. El identificador R1 a R9 se conserva en el informe de activaciones, de modo que la tabla, el código y la interfaz puedan compararse sin ambigüedad.

## 6. Inferencia Mamdani paso a paso

1. **Validar entradas.** Rechazar valores no numéricos, infinitos, NaN y valores fuera de rango. No recortar silenciosamente un dato inválido. Los límites 0 y 200 para peso y 0 y 120 para edad son inclusivos.
2. **Fusificar.** Evaluar las tres funciones de peso y las tres de edad para obtener seis grados de pertenencia.
3. **Activar reglas.** Para cada regla, tomar el mínimo entre la pertenencia del peso y la de la edad. Ese mínimo es su fuerza de activación alfa. El operador Y se implementa con mínimo.
4. **Aplicar implicación.** Recortar la función de salida indicada por cada regla a la altura alfa. Se usa mínimo entre alfa y la pertenencia original de cada punto de salida.
5. **Agregar consecuencias.** Tomar el máximo punto a punto de las nueve curvas recortadas. Reglas con la misma consecuencia se combinan por máximo, no sumando sus activaciones.
6. **Desfusificar.** Calcular el centroide como el área ponderada por la coordenada de salida dividida entre el área total. El código integra z por la pertenencia agregada y lo divide entre la integral de esa pertenencia, con la regla trapezoidal.
7. **Presentar el resultado.** Mostrar el índice con dos decimales y su pertenencia a bajo, medio y alto. La etiqueta es el conjunto de mayor pertenencia al índice obtenido; en empate se prioriza alto, después medio y luego bajo. Esta etiqueta no reemplaza la salida numérica.

La malla de salida contiene 1001 puntos de 0 a 100, con paso 0,1. Se conserva precisión completa durante la inferencia. Un área agregada nula se trata como error de configuración. El centroide de una región extrema no coincide necesariamente con 0 o 100; por eso una regla completamente alta produce aproximadamente 84,44 puntos.

## 7. Validaciones del motor de referencia

Resultados obtenidos al ejecutar el código del diseño. Los tres primeros casos constituyen la validación solicitada; el cuarto examina el solapamiento. Son pruebas de coherencia matemática, no validación clínica.

| Caso | Entradas | Reglas activas | Índice | Etiqueta |
|---|---|---|---:|---|
| 1 | 55 kg / 25 años | R1 = 0,7500; R4 = 0,2000 | 16,5384 | Bajo |
| 2 | 75 kg / 50 años | R5 = 1,0000 | 50,0000 | Medio |
| 3 | 130 kg / 80 años | R9 = 1,0000 | 84,4445 | Alto |
| 4 | 90 kg / 50 años | R5 = 0,4000; R8 = 0,3333 | 65,4664 | Alto |

Caso 1: a 55 kg, ligero = 0,75 e intermedio = 0,20; a 25 años, joven = 1. R1 y R4 recortan bajo y se agregan con máximo a 0,75. El centroide es 16,5384 puntos.

Caso 2: a 75 kg, intermedio = 1; a 50 años, adulta = 1. Solo R5 se activa, con fuerza 1. El triángulo medio es simétrico alrededor de 50; su centroide es exactamente 50 puntos.

Caso 3: a 130 kg, elevado = 1; a 80 años, mayor = 1. Solo R9 se activa, con fuerza 1. El centroide del trapecio alto es 84,4445 puntos con la malla definida.

Caso 4: a 90 kg, intermedio = 0,4 y elevado = 0,3333; a 50 años, adulta = 1. R5 activa medio a 0,4 y R8 activa alto a 0,3333. El máximo de ambas curvas recortadas produce 65,4664 puntos. La etiqueta alto corresponde a la mayor pertenencia de ese resultado, no necesariamente a la regla con alfa más grande.

Controles adicionales: se comprueba cobertura de los conjuntos, salidas finitas para las cuatro esquinas del dominio, rechazo de texto, booleanos, `None`, NaN, infinitos, valores vacíos y valores fuera de rango. La tolerancia de regresión es 0,02 puntos. No se presupone monotonicidad global.

## 8. Código ejecutable del motor y reglas

La implementación está dividida sin alterar el comportamiento: `model/config.py` contiene la única fuente de verdad, `model/membership.py` contiene las funciones y `model/inference.py` contiene la inferencia. La configuración ejecutable equivale a:

```python
VARIABLES = {
    "peso": {"range": (0, 200), "sets": {
        "ligero": ("trap", (0, 0, 50, 70)),
        "intermedio": ("tri", (50, 75, 100)),
        "elevado": ("trap", (80, 110, 200, 200))}},
    "edad": {"range": (0, 120), "sets": {
        "joven": ("trap", (0, 0, 25, 40)),
        "adulta": ("tri", (30, 50, 70)),
        "mayor": ("trap", (60, 80, 120, 120))}},
    "salida": {"range": (0, 100), "sets": {
        "bajo": ("trap", (0, 0, 20, 40)),
        "medio": ("tri", (30, 50, 70)),
        "alto": ("trap", (60, 80, 100, 100))}},
}
RULES = (
    ("R1", "ligero", "joven", "bajo", 1.0),
    ("R2", "ligero", "adulta", "medio", 1.0),
    ("R3", "ligero", "mayor", "alto", 1.0),
    ("R4", "intermedio", "joven", "bajo", 1.0),
    ("R5", "intermedio", "adulta", "medio", 1.0),
    ("R6", "intermedio", "mayor", "alto", 1.0),
    ("R7", "elevado", "joven", "medio", 1.0),
    ("R8", "elevado", "adulta", "alto", 1.0),
    ("R9", "elevado", "mayor", "alto", 1.0),
)
```

La función real completa puede inspeccionarse en la sección **Matriz y reglas**. Allí se muestra con `inspect.getsource`, directamente desde el evaluador importado.

## 9. Código ejecutable del motor y validación

El evaluador valida ambas entradas, calcula las seis pertenencias, crea `np.linspace(0, 100, 1001)`, recorre las nueve reglas, aplica `min` en antecedente e implicación, agrega con `np.maximum` y calcula:

```python
area = np.trapezoid(agregado, z)
indice = np.trapezoid(z * agregado, z) / area
```

El resultado incluye versión, entradas, grados de entrada, traza de nueve reglas, 9 curvas recortadas, universo, curva agregada, área, centroide, etiqueta y grados de salida. La prueba central `evaluar(75, 50)` devuelve índice 50 y nivel medio. El código no redondea internamente; el formato a dos decimales pertenece solo a la interfaz.

## 10. Evidencias y requisitos del aplicativo

Evidencia disponible: parámetros completos, matriz, listado `RULES` incorporado al motor, identificadores estables, resultados numéricos obtenidos por ejecución, pruebas automatizadas y registro de versiones. Una captura solo se declara realizada si existe el archivo auténtico correspondiente.

| Evidencia | Contenido verificable |
|---|---|
| Registro de reglas | Las nueve reglas cargadas desde el mismo registro que ejecuta el motor; total igual a 9. |
| Traza de una simulación | Peso, edad, seis pertenencias, nueve fuerzas alfa y reglas activas identificadas. |
| Tres validaciones | Casos 1 a 3 con entrada, salida, curvas y fecha de ejecución. |
| Prueba de solapamiento | Caso 4 con R5 y R8 activas y curva agregada. |
| Resultados de pruebas | Salida real de pytest, versión del modelo y versiones instaladas. |

La aplicación usa Python y Streamlit para la interfaz, NumPy para el motor, pandas para tablas, Plotly para curvas interactivas, python-docx para exportar informes y pytest para pruebas. No usa OpenCV, entrenamiento de IA, bases de datos ni servicios externos. El motor Mamdani está implementado explícitamente.

La interfaz usa fondo blanco, rojo principal `#B91C1C`, rojo oscuro `#7F1D1D`, fondo secundario `#FEF2F2` y texto `#1F2937`. Sus secciones son Simulador, Diseño y documentación, Matriz y reglas, Validaciones y Evidencias. Esta documentación conserva el análisis, limitaciones, código y fuentes, y puede descargarse como Word.

## 11. Entrega y fuentes

Según la transcripción, el trabajo debe estar en el correo del profesor para la próxima clase y puede realizarse en pareja. La transcripción no proporciona correo, hora exacta ni título o enlace del video. El paquete final incluye este informe, código de la aplicación, instrucciones de ejecución y evidencias reales. Si hay compañero, se debe añadir su nombre antes del envío.

Fuente del enunciado: transcripción de la clase aportada por el estudiante, intervenciones de 0:24 a 3:23 y de 18:02 a 18:18. La selección de conjuntos, parámetros y reglas es propia de este diseño.

Referencias técnicas consultadas el 2 de octubre de 2026:

- NumPy, `numpy.trapezoid`: https://numpy.org/doc/2.1/reference/generated/numpy.trapezoid.html
- Streamlit, referencia de API: https://docs.streamlit.io/develop/api-reference

Estas referencias respaldan las herramientas, no los supuestos de riesgo.
