# Sistema difuso académico de propensión al infarto

La interfaz CardioLab utiliza Bootstrap 5.3.8 local y estilos propios inspirados
en la dirección visual del portal de la Clínica Universidad de Navarra
(https://www.cun.es/), sin afiliación. Los estilos están en `assets/clinic.css` y
la presentación en `ui/design.py`. No requiere conexión para cargar Bootstrap.
Las capturas reales del rediseño están en `evidencias/interfaz-escritorio.png`
y `evidencias/interfaz-movil.png`.

Después de actualizar el diseño, reinicia Streamlit con Ctrl+C y
`python -m streamlit run app.py`; recarga el navegador con Ctrl+F5.

El menú técnico de Streamlit está oculto mediante `client.toolbarMode = "minimal"`.

Aplicación local en Streamlit que implementa un motor Mamdani explícito con peso y edad. Su salida es un **índice académico de 0 a 100 puntos**: no es una probabilidad clínica, no es un diagnóstico y no debe usarse para orientar tratamientos.

## Contenido

Para publicar en Render, sigue [la guía de despliegue](docs/render.md).
El archivo `render.yaml` configura el servicio, ejecuta las pruebas al construir
y toma el puerto de Render. `.python-version` fija Python 3.14.3.

- Cinco secciones: Simulador, Diseño y documentación, Matriz y reglas, Validaciones y Evidencias.
- Fuente única `modelo_v1`, nueve reglas trazables y centroide con 1001 puntos.
- Gráficas Plotly generadas desde las funciones reales.
- Descargas JSON, CSV y DOCX bajo acción del usuario.
- Pruebas de regresión, funciones, cobertura, entradas inválidas, esquinas y exportaciones.

## Instalación en Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

En otra terminal, con el entorno activado:

```powershell
python -m pytest
```

Si la política de PowerShell bloquea la activación, se puede llamar directamente a `.\.venv\Scripts\python.exe` en los dos últimos comandos.

## Instalación en Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Pruebas:

```bash
python -m pytest
```

## Reproducir los cuatro casos

En **Simulador**, usa los botones de ejemplo o introduce manualmente:

El peso puede contener decimales. La edad debe introducirse como un número entero de años entre 0 y 120.

| Peso (kg) | Edad (años) | Índice esperado (±0,02) | Etiqueta |
|---:|---:|---:|---|
| 55 | 25 | 16,5384 | bajo |
| 75 | 50 | 50,0000 | medio |
| 130 | 80 | 84,4445 | alto |
| 90 | 50 | 65,4664 | alto |

También se pueden ejecutar desde consola:

```powershell
python -c "from model.inference import evaluar; print([(p,e,evaluar(p,e)['indice'],evaluar(p,e)['nivel']) for p,e in [(55,25),(75,50),(130,80),(90,50)]])"
```

## Privacidad y límites

No se recopilan datos identificables, no hay base de datos ni servicios externos. El resultado vigente vive solo en el estado de sesión de Streamlit. El modelo es un ejercicio didáctico construido con dos variables y supuestos propios; no tiene validación clínica.

## Entorno verificado

Verificación real del 2 de octubre de 2026: Python 3.14.3, NumPy 2.5.3, Streamlit 1.64.0, pandas 3.0.6, Plotly 6.9.0, python-docx 1.2.0 y pytest 9.1.1. Consulta `evidencias/resumen.md` para los comandos y las limitaciones.
