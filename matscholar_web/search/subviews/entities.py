from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.constants import rester, valid_entity_filters, \
    entity_shortcode_map


def gen_output(most_common, entity_type, query, class_name="three column"):
    table = html.Table(
        [html.Tr([html.Th(entity_type, className="highlighted {}".format(
            entity_shortcode_map[entity_type.lower()])),
                  html.Th("score", style={"textAlign": "right", "fontWeight": "normal"},
                          className="highlighted {}".format(
                              entity_shortcode_map[entity_type.lower()]))],
                 className="summary-header")] +
        [html.Tr([
            html.Td(ent),
            # html.A(ent, href="/search/?{}".format(query))),
            html.Td('{:.2f}'.format(score), style={"textAlign": "right"})], style={'color': 'black'})
            for ent, count, score in most_common],
        className="summary-table")
    return html.Div(html.Div(table, className="summary-div " + class_name,
                             style={"width": "20%", "display":"block"}))


def gen_table(results_dict, query=None):
    return html.Div([
        html.Div([
            gen_output(results_dict["PRO"], "Property", query),
            gen_output(results_dict["APL"], "Application", query),
            gen_output(results_dict["CMT"], "Characterization", query),
            gen_output(results_dict["SMT"], "Synthesis", query)]),
        html.Div([
            gen_output(results_dict["DSC"], "Descriptor", query),
            gen_output(results_dict["SPL"], "Phase", query),
            gen_output(results_dict["MAT"], "Material", query)]),
    ])




def entities_results_html(n_clicks, dropdown_value, search_text, *entities):
    print(n_clicks, dropdown_value, search_text, *entities)
    return "No results"

def entities_results_html(*args):


    print("Now we're in entities results html!")
    text = str(args[0][0])
    entities = {f: [s.strip() for s in args[0][i + 3].split(',')] for i, f in enumerate(
        valid_entity_filters) if ((args[0][i + 3] is not None) and (args[0][i + 3].split(',') != ['']))}

    print("We lookin for results!")
    results = rester.entities_search(entities, text=text, top_k=None)

    print(f"WE got some results baby!: {results}")

    if results is not None:
        query = dict()
        for f, fname in [(text, 'text')]:
            if f is not None and f != [] and f != 'None':
                query[fname] = f
        for f in valid_entity_filters:
            try:
                query[f] = entities[f]
            except KeyError:
                pass
        query = urllib.parse.urlencode(query)
        return gen_table(results, query=query)
    else:
        return "No Results"
