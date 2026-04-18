"""
Utility functions for Jupyter Notebook environments.
"""
from IPython.display import HTML, display


def setup_scribal_environment(font_size="1.1em"):
    """
    Injects CSS into the Jupyter/Binder environment to correctly render 
    Noto Sans Cuneiform in both Markdown and Code outputs.

    :param font_size: Font size of the text in the output, defaults to "1.1em"
    :type font_size: str, optional
    """    
    style = f"""
    <style>
    /* 1. Font load */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Cuneiform&display=swap');
    
    /* 2. Force MONOSPACED in Python outputs */
    .jp-OutputArea-output pre, 
    .output_subarea pre, 
    .output_text pre,
    .output_stdout pre {{
        font-family: 'Noto Sans Cuneiform', 'Courier New', 'Lucida Console', monospace !important;
        font-size: {font_size};
        line-height: 1.2;
        white-space: pre !important; /* Mantiene espacios y saltos de línea */
    }}

    /* 3. Adjustment for Markdown cells (proportional is fine here) */
    .rendered_html, .jp-RenderedHTMLCommon {{
        font-family: 'Noto Sans Cuneiform', sans-serif !important;
    }}
    </style>
    """
    display(HTML(style))

def print_to_notebook(text:str):
    """
    Print text ensuring monospaced font and cuneiform support in Notebook 
    environments, avoiding misalignment.

    :param text: Text to print
    :type text: str
    """    
    html_output = f"""
    <div style="
        font-family: 'Noto Sans Cuneiform', 'Courier New', monospace !important;
        white-space: pre;
        line-height: 1.2em;
        font-size: 1.1em;
        padding: 10px;
        border-left: 3px solid #ccc;
        display: block;
    ">{text}</div>
    """
    display(HTML(html_output))