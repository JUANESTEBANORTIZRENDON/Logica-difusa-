## Resumen de evidencia real

Ejecución realizada el 2 de octubre de 2026 en Windows, zona horaria `America/Bogota`, con `modelo_v1`.

### Versiones realmente probadas

| Componente | Versión |
|---|---:|
| Python | 3.14.3 |
| NumPy | 2.5.3 |
| Streamlit | 1.64.0 |
| pandas | 3.0.6 |
| Plotly | 6.9.0 |
| python-docx | 1.2.0 |
| pytest | 9.1.1 |

### Resultados auténticos

Comando: `.\.venv\Scripts\python.exe -m pytest -q`

Resultado final: **36 pruebas aprobadas en 7,58 s**. La suite cubrió las funciones y hombros, solapamientos, dominio completo, los cuatro casos de referencia, alfas exigidas, nueve cruces, entradas inválidas, cuatro esquinas, no mutación, JSON/CSV/DOCX, estructura y recorrido de las cinco secciones mediante la herramienta de pruebas de Streamlit.

| Entrada | Resultado ejecutado |
|---|---|
| 55 kg / 25 años | 16,538410 · bajo |
| 75 kg / 50 años | 50,000000 · medio |
| 130 kg / 80 años | 84,444500 · alto |
| 90 kg / 50 años | 65,466381 · alto |

Prueba de arranque: el servidor se inició con `python -m streamlit run app.py --server.port 8501 --server.headless true` y respondió **HTTP 200** en `http://127.0.0.1:8501`. Después se cerró el proceso de verificación.

### Limitaciones de esta evidencia

No había un navegador gráfico disponible en el entorno de ejecución, por lo que las capturas visuales de los tres casos, la matriz y la traza quedan pendientes. No se han inventado ni sustituido por imágenes simuladas. La integración se verificó programáticamente recorriendo las cinco secciones, ejecutando el cálculo y comprobando las tres descargas del caso vigente. La adaptación móvil está implementada mediante columnas flexibles y una regla CSS para pantallas de hasta 640 px, pero no se presenta una captura de dispositivo.
