"""
Utility functions for Jupyter Notebook environments.
"""
from IPython.display import HTML, display

def setup_scribal_environment_old(font_size="1.1em"):
    """
    Injects CSS into the Jupyter/Binder environment to correctly render 
    Noto Sans Cuneiform in both Markdown and Code outputs.
    """
    style = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Cuneiform&display=swap');
    
    /* Global notebook and markdown font */
    .rendered_html, .jp-RenderedHTMLCommon, .jp-RenderedText {{
        font-family: 'Noto Sans Cuneiform', 'DejaVu Sans', sans-serif !important;
    }}

    /* Python print() and stdout output (crucial for tables) */
    .jp-OutputArea-output pre, 
    .jp-RenderedText pre, 
    .output_subarea pre, 
    .output_text pre,
    .jp-OutputArea-output code {{
        font-family: 'Noto Sans Cuneiform', 'Courier New', monospace !important;
        font-size: {font_size};
    }}

    /* Editor cuneiform support */
    .jp-Editor .CodeMirror, .CodeMirror-code {{
        font-family: 'Noto Sans Cuneiform', monospace !important;
    }}
    </style>
    """
    display(HTML(style))
    print("--- MesoMath Scribal Environment Ready ---")

def setup_scribal_environment(font_size="1.1em"):
    style = f"""
    <style>
    /* 1. Carga de la fuente */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Cuneiform&display=swap');
    
    /* 2. Forzar MONOESPACIADO en los outputs de Python */
    .jp-OutputArea-output pre, 
    .output_subarea pre, 
    .output_text pre,
    .output_stdout pre {{
        font-family: 'Noto Sans Cuneiform', 'Courier New', 'Lucida Console', monospace !important;
        font-size: {font_size};
        line-height: 1.2;
        white-space: pre !important; /* Mantiene espacios y saltos de línea */
    }}

    /* 3. Ajuste para celdas Markdown (proporcional está bien aquí) */
    .rendered_html, .jp-RenderedHTMLCommon {{
        font-family: 'Noto Sans Cuneiform', sans-serif !important;
    }}
    </style>
    """
    display(HTML(style))
