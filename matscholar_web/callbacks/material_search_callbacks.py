import dash_html_components as html
import urllib
import pandas as pd
from dash.dependencies import Input, Output, State
from matscholar.rest import Rester

# Get the rester on import
rester = Rester()

def split_inputs(input):
    if input is not None:
        return [inp.strip() for inp in input.split(",")]
    else:
        return []

def gen_output(result):
    table = html.Table(
        [html.Tr([html.Th("Material"), html.Th("counts"), html.Th("dois")])] +
        [html.Tr([
            html.Td(mat),
            html.Td(count), html.Td(html.Span("; ".join(dois), style={"white-space": "nowrap"}))]) for mat, count, dois in result],
        style={"width": "100px"})
    return html.Div(table, style={"width": "100px"})

def gen_df(result):
    mats = [mat for mat, _, _ in result]
    counts = [count for _, count, _ in result]
    dois = [" ".join(dois) for _, _, dois in result]
    df = pd.DataFrame()
    df["Material"] = mats
    df["counts"] = counts
    df["dois"] = dois
    return df

def bind(app):
    ### Material Search App Callbacks ###
    @app.callback(
        Output("material_search_output", "children"),
        [Input("material_search_btn", "n_clicks")],
        [State("material_search_input", "value"),
         State("element_filters_input", "value")])
    def get_materials(n_clicks, entities, elements):
        if n_clicks is not None:
            entities = split_inputs(entities)
            elements = split_inputs(elements)
            result = rester.materials_search_ents(entities, elements)
            result = [( mat, count, dois) for mat, count, dois in result
                      if (not mat.isupper()) and len(mat) > 2 and "oxide" not in mat]
            return html.Div([html.A(
                            "Download data as csv",
                            id="download-link",
                            download="matscholar_data.csv",
                            href="",
                            target="_blank"),
                gen_output(result)])
    @app.callback(
        Output("download-link", "href"),
        [Input("material_search_btn", "n_clicks")],
        [State("material_search_input", "value"),
         State("element_filters_input", "value")])
    def update_download_link(n_clicks, entities, elements):
        if n_clicks is not None:
            entities = split_inputs(entities)
            elements = split_inputs(elements)
            result = rester.materials_search_ents(entities, elements)
            result = [(mat, count, dois) for mat, count, dois in result
                      if (not mat.isupper()) and len(mat) > 2 and "oxide" not in mat]
            df = gen_df(result)
            csv_string = df.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
            return csv_string
