import dash_html_components as html
import dash_core_components as dcc


def serve_layout():
    introduction_header_txt = \
        "Matscholar: Your (AI) scholar assistant for inorganic materials " \
        "science \n"
    introduction_body_txt = \
        "Matscholar is a research effort based out of the LBL and led by the " \
        "[HackingMaterials](https://hackingmaterials.lbl.gov), " \
        "Persson ([Materials Project](materialsproject.org)) and " \
        "[Ceder](https://ceder.berkeley.edu) research groups."
    introduction_body_md = dcc.Markdown(introduction_body_txt)
    introduction_header = html.Div(introduction_header_txt, className="is-size-3-desktop has-text-weight-semibold")
    introduction_body = html.Div(introduction_body_md, className="is-size-6-desktop")
    introduction_container = html.Div([introduction_header, introduction_body], className="container has-padding-200")
    return introduction_container
