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

def get_details(dois):
    return html.Details([
        html.Summary('Show dois?'),
        html.Span([html.A("{}; ".format(doi), href="http://www.doi.org/{}".format(doi)) for doi in dois],
                  style={"white-space": "nowrap"})
        ])

def gen_output(result):
    table = html.Table(
        [html.Tr([html.Th("Material"), html.Th("counts"), html.Th("dois")])] +
        [html.Tr([
            html.Td(mat),
            html.Td(count), html.Td(get_details(dois))])
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

def bind(app):
    ### Material Search App Callbacks ###
    @app.callback(
        Output("material_search_output", "children"),
        [Input("material_search_btn", "n_clicks")],
        [State("material_search_input", "value"),
         State("element_filters_input", "value")])
    def get_materials(n_clicks, entities, elements):
        if n_clicks is not None:
            # Extract the data
            entities = split_inputs(entities)
            elements = split_inputs(elements)
            result = rester.materials_search_ents(entities, elements)
            result = [( mat, count, dois) for mat, count, dois in result
                      if (not mat.isupper()) and len(mat) > 2 and "oxide" not in mat]

            # Update the download link
            df = gen_df(result)
            csv_string = df.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
            return html.Div([html.A(
                            "Download data as csv",
                            id="download-link",
                            download="matscholar_data.csv",
                            href=csv_string,
                            target="_blank"),
                gen_output(result)])
    @app.callback(
        [Output("element_filters_input", 'value'), Output("heatmap", "figure")],
        [Input("heatmap", "clickData")],
        [State("element_filters_input", 'value'), State("include-radio", "value")])
    def add_element(clickData, elements, value):

        if clickData is not None:
            # Extract the new element and add
            prefix = "" if value == "include" else "-"
            new_el = clickData["points"][0]["text"].split("<br>")[1]
            new_el = prefix + new_el.split(":")[1].strip()

            # Check for previous elements
            if elements:
                prev_el = elements.split(",")
            else:
                prev_el = []

            # Add the new element
            if prev_el:
                if new_el in prev_el:
                    prev_el.remove(new_el)
                elif "-"+new_el in prev_el:
                    prev_el.remove("-"+new_el)
                    prev_el.append(new_el)
                elif new_el[0] == "-" and any(el == new_el[1:] for el in prev_el):
                    prev_el.remove(new_el[1:])
                    prev_el.append(new_el)
                else:
                    prev_el.append(new_el)
            else:
                prev_el = [new_el]

            return ",".join(prev_el), build_periodic_table(prev_el)

        return "", build_periodic_table()
