from dash.dependencies import Input, Output, State
import json
from matscholar.rest import Rester
from collections import defaultdict
import dash_html_components as html
from matscholar_web.view.summary_app import VALID_FILTERS

rest = Rester()

def gen_output(most_common, entity_type, material, class_name="three column"):
    table = html.Table(
        [html.Tr([html.Th(entity_type), html.Th("score", style={"textAlign": "right", "fontWeight": "normal"})],
                 className="summary-header")] +
        [html.Tr([
            html.Td(html.A(prop, href="/search/{}/{}/{}".format(entity_type.lower(), prop, material))),
            html.Td('{:.2f}'.format(100*score), style={"textAlign": "right"})], style={'color': 'black'})
            for prop, count, score in most_common],
        className="summary-table")
    return html.Div(table, className="summary-div " + class_name, style={"width": "20%"})

def gen_table(results_dict, material=""):
    return html.Div([
                html.Div([
                    gen_output(results_dict["PRO"], "Property", material),
                    gen_output(results_dict["APL"], "Application", material),
                    gen_output(results_dict["CMT"], "Characterization", material),
                    gen_output(results_dict["SMT"], "Synthesis", material)],  className="row"),
                html.Div([
                    gen_output(results_dict["DSC"], "Sample descriptor", material),
                    gen_output(results_dict["SPL"], "Phase", material),
                    gen_output(results_dict["MAT"], "Material", material)], className="row"),
            ])

def bind(app):
    @app.callback(
        Output("summary-results", "children"),
        [Input("summary-btn", "n_clicks")],
        [State(f+'-summary', 'value') for f in VALID_FILTERS])
    def show_filters(n_clicks, *args):
        if n_clicks is not None and any(args):
            query = defaultdict(list)
            for filter, ents in zip(VALID_FILTERS, args):
                if ents:
                    ents = [ent.strip() for ent in ents.split(",")]
                    query[filter] += ents
            dumped = json.dumps(query)
            summary = rest.get_summary(dumped)
            if not all(summary[key] for key in summary):
                # Check if material exists, if not suggest similar materials
                if "material" in query:
                    query = {"material": query["material"]}
                    dumped = json.dumps(query)
                    summary = rest.get_summary(dumped)
                    if not all(summary[key] for key in summary): #If this isnt true the material doesn't exist
                        rester = Rester()
                        similar_mats = rester.get_similar_materials(query['material'][0])
                        mats_as_string = ("{}, "*9 + "{}.").format(*similar_mats)
                        return html.Div("{} is not present in our database. "
                                            "Try these similar materials: {}".format(query["material"][0],
                                                                                      mats_as_string),
                                                                                     style={"color": "black"})
                    else:
                        return html.Div("There are no results to match this query...", style={"color": "black"})
                return html.Div("There are no results to match this query...", style={"color": "black"})
            else:
                return gen_table(summary) if "material" not in query else gen_table(summary, material=query["material"])
        else:
            return ""
