"""Presentación Bootstrap local, aislada de los controles de Streamlit."""

from pathlib import Path
import base64
import re
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


def install_design():
    bootstrap = (ROOT / 'assets/vendor/bootstrap.min.css').read_text(encoding='utf-8')
    bootstrap = bootstrap.replace('@charset "UTF-8";', '').replace(':root', ':scope')
    css = (ROOT / 'assets/clinic.css').read_text(encoding='utf-8')
    # Bootstrap solo afecta nuestros bloques HTML, no el DOM de los widgets.
    st.html('<style>@scope (.clinic-ui) {' + bootstrap + '}</style><style>' + css + '</style>')


def render(markup):
    # st.html elimina SVG inline; se entrega como imagen SVG local embebida.
    def svg_image(match):
        svg = match.group(0).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        encoded = base64.b64encode(svg.encode()).decode()
        return f'<img src="data:image/svg+xml;base64,{encoded}" alt="" width="170" height="140">'
    markup = re.sub(r'<svg\b.*?</svg>', svg_image, markup, flags=re.S)
    st.html('<div class="clinic-ui">' + markup.replace('clinic-ui ', '') + '</div>')


def brand():
    render('''<div class="clinic-ui sidebar-brand">
        <div class="brand-symbol" aria-hidden="true">+</div>
        <div><strong>Cardio<span>Lab</span></strong><small>SIMULACIÓN ACADÉMICA</small></div>
    </div>''')


def hero():
    render('''<section class="clinic-ui clinic-hero">
      <div class="row align-items-center g-4">
        <div class="col-md-8">
          <div class="eyebrow mb-3">APRENDER · EXPLORAR · COMPRENDER</div>
          <h1>La lógica detrás<br>de cada resultado.</h1>
          <p class="hero-copy mt-3 mb-4">Explora un modelo de propensión al infarto con peso y edad.
          Una experiencia guiada para entender la lógica difusa.</p>
          <div class="d-flex flex-wrap gap-2">
            <span class="badge rounded-pill">2 variables de entrada</span>
            <span class="badge rounded-pill">9 reglas difusas</span>
            <span class="badge rounded-pill">Un proceso explicable</span>
          </div>
        </div>
        <div class="col-md-4 hero-art" aria-hidden="true">
          <div class="pulse-disc"><svg viewBox="0 0 220 180" fill="none">
            <path d="M110 149 43 87C-3 39 66 4 110 51c44-47 113-12 67 36Z" fill="#fff" fill-opacity=".85"/>
            <path d="M18 94h49l14-28 21 57 22-77 20 48h57" stroke="#B91C1C" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
          </svg></div>
          <div class="art-label">CARDIOLAB <span> / </span> MODELO ACADÉMICO</div>
        </div>
      </div>
    </section>''')


def notice():
    render('''<div class="clinic-ui academic-note d-flex align-items-start gap-3">
        <span class="note-icon" aria-hidden="true">i</span>
        <p class="mb-0"><strong>Una herramienta para aprender.</strong> El índice es académico:
        no es probabilidad clínica, diagnóstico ni orientación para tratamientos.</p>
    </div>''')


def empty_result():
    render('''<div class="clinic-ui card empty-result text-center">
      <div class="card-body py-4"><div class="empty-symbol mx-auto mb-3" aria-hidden="true">↗</div>
      <h3>Tu resultado comienza aquí</h3>
      <p class="mb-0">Ingresa el peso y la edad, o elige un caso de ejemplo.<br>
      Verás el índice, su nivel y la explicación de cada regla.</p></div>
    </div>''')
