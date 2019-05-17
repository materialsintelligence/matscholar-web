from dash.dependencies import Input, Output, State
import json
from matscholar.rest import Rester
from collections import defaultdict
import dash_html_components as html

rest = Rester()

# FILTER_DICT = {'Material': 'material',
#                'Property': 'property',
#                'Application': 'application',
#                'Phase': 'phase',
#                'Characterization': 'characterization',
#                'Synthesis': 'synthesis',
#                'Sample descriptor': 'descriptor'}

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
        Output("search_results", "children"),
        [Input("search_btn", "n_clicks")],
        [State("search_filters", "value")])
    def show_filters(n_clicks, filter_val):
        if n_clicks is not None and filter_val:
            filter_vals = [val["value"] for val in filter_val] if filter_val else None
            query = defaultdict(list)
            for filter in filter_vals:
                key, value = filter.split(':')
                query[key].append(value)
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
                                                                                     style={"color":"white"})
                    else:
                        return html.Div("There are no results to match this query...", style={"color":"white"})
                return html.Div("There are no results to match this query...", style={"color":"white"})
            else:
                return gen_table(summary) if "material" not in query else gen_table(summary, material=query["material"])
        else:
            return ''
