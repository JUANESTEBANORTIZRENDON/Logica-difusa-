# Desplegar CardioLab en Render

## Preparación incluida

- `render.yaml`: servicio web Python, plan Free, instalación y pruebas en cada
  construcción, arranque Streamlit en `0.0.0.0:$PORT`, health check y despliegue
  automático con los commits de la rama conectada.
- `.python-version`: Python 3.14.3, versión usada en la verificación local.
- `requirements.txt`: dependencias directas fijadas a las versiones probadas.
  Las dependencias transitivas siguen siendo resueltas por pip.
- `.streamlit/config.toml`: tema y telemetría de Streamlit desactivada.
- `.gitignore`: excluye el entorno virtual, secretos y perfiles de Chrome.

No requiere base de datos, disco persistente, claves API ni Node.js en Render.
Bootstrap y los demás recursos visuales están en `assets/` y deben subirse.
El script Node de capturas es solo una herramienta local y no se ejecuta al desplegar.

## 1. Subir el proyecto a GitHub

Crea un repositorio vacío en GitHub, por ejemplo `cardiolab`, sin añadir README
ni .gitignore desde GitHub. Puedes elegir un repositorio privado y dar acceso a Render.

Esta carpeta no tenía repositorio Git al preparar el despliegue. Ejecuta en PowerShell:

```powershell
cd "C:\Users\USER\logica difusa corazon"
git init
git branch -M main
git add .
git status --short
git commit -m "Preparar CardioLab para Render"
git remote add origin https://github.com/TU_USUARIO/cardiolab.git
git push -u origin main
```

Sustituye `TU_USUARIO` por tu usuario real. Si Git pide tu identidad, configura
`git config user.name "Tu nombre"` y `git config user.email "Tu correo de GitHub"`
y repite el commit. Si el repositorio ya está inicializado o tiene un remoto,
omite los comandos correspondientes y usa el repositorio existente.

Antes del commit, comprueba que `git status` no incluya `.venv`, `.env`, secretos
ni carpetas `evidencias/chrome-*`. El código, `assets/`, `docs/`, `tests/`,
`.streamlit/config.toml`, `.python-version` y `render.yaml` sí deben estar incluidos.

## 2. Crear el servicio con Blueprint (recomendado)

1. Entra en https://dashboard.render.com/ y conecta GitHub.
2. Selecciona **New > Blueprint**.
3. Elige el repositorio `cardiolab` y la rama `main`.
4. Usa `render.yaml`, ubicado en la raíz, como archivo del Blueprint.
5. Revisa el servicio `cardiolab` y el plan **Free**. Puedes cambiar el nombre
   si Render indica que ya está ocupado.
6. Confirma la creación/despliegue desde el formulario.
7. Espera a que termine el build y el servicio figure como **Live**.
8. Abre la dirección `https://...onrender.com` que muestre Render.

La construcción instala dependencias y ejecuta pytest. Si una prueba falla,
el build se detiene: revisa el primer error en los logs.

## Alternativa: configuración manual

Si prefieres **New > Web Service**, conecta el mismo repositorio y configura:

| Campo | Valor |
|---|---|
| Language / Runtime | Python 3 |
| Branch | main |
| Root Directory | Vacío (app.py está en la raíz) |
| Instance Type | Free |
| Build Command | `python -m pip install -r requirements.txt && python -m pytest -q` |
| Start Command | `python -m streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT --server.headless=true --server.fileWatcherType=none` |
| Health Check Path | `/_stcore/health` |

Python se toma de `.python-version`. Si defines `PYTHON_VERSION` en el panel,
usa `3.14.3`, porque esa variable tiene prioridad sobre el archivo.
No es necesario definir `PORT`: Render lo proporciona. `$PORT` es sintaxis del
shell Linux de Render; no copies ese comando literalmente a PowerShell.
Elige Blueprint **o** Web Service manual; no crees ambos para la misma aplicación.

## 3. Comprobar el despliegue

1. Abre el simulador y calcula 75 kg / 50 años: debe mostrar 50,00 puntos y Riesgo medio.
2. Comprueba que la edad se muestra como entero y el peso acepta decimales.
3. Abre las cinco secciones y prueba JSON, CSV y DOCX en Evidencias.
4. Revisa la interfaz en móvil. Los estilos deben cargar sin un CDN.
5. Visita `https://TU_SERVICIO.onrender.com/_stcore/health`: debe responder `ok`.

El plan gratuito puede suspender el servicio tras 15 minutos sin actividad;
la siguiente visita puede tardar alrededor de un minuto en reactivarlo.
El estado de sesión es temporal y se puede perder al reiniciar o volver a desplegar.
Descarga los resultados que quieras conservar.

## Actualizar la aplicación

```powershell
git add .
git commit -m "Actualizar CardioLab"
git push
```

Con el Blueprint preparado, un commit en la rama conectada dispara un nuevo despliegue.

## Diagnóstico rápido

- **No open ports detected**: revisa el Start Command, `0.0.0.0` y `$PORT`.
- **No matching distribution found**: revisa la versión de Python y el paquete
  nombrado en el error. El build Linux de Render es la verificación final de
  disponibilidad de los paquetes fijados; las pruebas locales se hicieron en Windows.
- **No aparece el diseño**: confirma que subiste `assets/clinic.css` y
  `assets/vendor/bootstrap.min.css`.
- **Falta contenido o un módulo**: confirma que las carpetas del proyecto se subieron
  completas y que Root Directory está vacío.
- **removeChild en Chrome**: desactiva la traducción automática para este sitio
  y recarga la página original.

## Documentación oficial consultada

- https://render.com/docs/infrastructure-as-code
- https://render.com/docs/blueprint-spec
- https://render.com/docs/python-version
- https://render.com/docs/web-services
- https://render.com/docs/free

Preparar estos archivos no crea un servicio en tu cuenta de Render. El despliegue
remoto se completa al conectar GitHub y confirmar la creación en Render.
