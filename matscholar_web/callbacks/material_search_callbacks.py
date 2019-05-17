import dash_html_components as html
import urllib
import pandas as pd
from dash.dependencies import Input, Output, State
from matscholar.rest import Rester
from matscholar_web.static.periodic_table.periodic_table import build_periodic_table

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
            html.Td(count), html.Td(html.Span("; ".join(dois), style={"white-space": "nowrap"}))])
            for mat, count, dois in result],
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

class PeriodicTable(object):

    def __init__(self):
        self.periodic_table = build_periodic_table()
        self.positive_elements = []
        self.negative_elements = []
        self.clicks = None

    def add_positive_element(self, el):
        self.positive_elements.append(el)
        self.periodic_table = build_periodic_table(self.positive_elements, self.negative_elements)

    def add_negative_element(self, el):
        self.negative_elements.append(el)
        self.periodic_table = build_periodic_table(self.positive_elements, self.negative_elements)

    def get_element_string(self):
        pos_el = [el for el, _, _ in self.positive_elements]
        if self.negative_elements:
            neg_el = ["-{}".format(el) for el, _, _ in self.negative_elements]
        else:
            neg_el = ""
        pos_string = ",".join(pos_el)
        neg_string = ",".join(neg_el)
        if pos_string:
            return "{},{}".format(pos_string, neg_string)
        else:
            return pos_string + neg_string

    def clear_table(self):
        self.positive_elements = []
        self.negative_elements = []
        self.periodic_table = build_periodic_table()

# Build the periodic table
pt = PeriodicTable()

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
    @app.callback(
        [Output("element_filters_input", 'value'), Output("heatmap", "figure")],
        [Input("heatmap", "clickData"),
         Input("clear-btn", "n_clicks")],
        [State("include-radio", "value")])
    def add_element(clickData, n_clicks, value):

        if n_clicks is not None and n_clicks != pt.clicks:
            pt.clicks = n_clicks
            pt.clear_table()
            return pt.get_element_string(), pt.periodic_table

        if clickData is not None:
            # Extract the new element and and update pt
            element = clickData["points"][0]["text"].split("<br>")[1]
            element = element.split(":")[1].strip()
            x = clickData["points"][0]["y"]
            y = clickData["points"][0]["x"]
            if value == "include":
                pt.add_positive_element((element, x, y))
            else:
                pt.add_negative_element((element, x, y))

            return pt.get_element_string(), pt.periodic_table

        return pt.get_element_string(), pt.periodic_table







