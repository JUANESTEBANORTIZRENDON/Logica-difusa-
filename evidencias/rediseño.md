# Verificación del rediseño CardioLab

Referencia consultada: https://www.cun.es/
Bootstrap local: 5.3.8; fuente y licencia en `assets/vendor/README.md`.

Se ejecutó `python -m pytest -q`: 37 pruebas aprobadas en 9,03 s durante el rediseño.
Las pruebas incluyen el cálculo, las cinco secciones y las exportaciones.

Se abrió la aplicación real en Chrome headless mediante el protocolo de
depuración del navegador. Capturas inspeccionadas visualmente:

- `interfaz-escritorio.png`: 1440 × 1100 píxeles.
- `interfaz-movil.png`: 390 × 1000 píxeles, simulación de viewport móvil.

Se comprobó que el ancho del documento coincide con el viewport en ambos tamaños
(1440 y 390), sin desbordamiento horizontal. Bootstrap está cargado y la franja
académica utiliza su utilidad flex. La ilustración SVG, el botón principal y las
tarjetas se ven en la captura final. No se ha probado un dispositivo físico.

Para reproducir las capturas: iniciar Streamlit en 127.0.0.1:8518 y ejecutar
`node evidencias/capturar-ui.mjs` con Chrome instalado en su ruta habitual.
Las capturas documentan el estado inicial del simulador; no sustituyen las
capturas de los casos de validación indicadas en el informe original.
