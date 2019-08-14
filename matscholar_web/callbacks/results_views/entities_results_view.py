from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.base import *


def gen_output(most_common, entity_type, query, class_name="three column"):
    table = html.Table(
        [html.Tr([html.Th(entity_type, className="highlighted {}".format(
            highlight_mapping[entity_type.lower()])), html.Th("score", style={"textAlign": "right", "fontWeight": "normal"}, className="highlighted {}".format(
                highlight_mapping[entity_type.lower()]))],
            className="summary-header")] +
        [html.Tr([
            html.Td(ent),
            # html.A(ent, href="/search/?{}".format(query))),
            html.Td('{:.2f}'.format(score), style={"textAlign": "right"})], style={'color': 'black'})
            for ent, count, score in most_common],
        className="summary-table")
    return html.Div(table, className="summary-div " + class_name, style={"width": "20%"})


def gen_table(results_dict, query=None):
    # return html.Div([
    #     html.Div([
    #                 gen_output(results_dict["PRO"], "Property", query),
    #                 gen_output(results_dict["APL"], "Application", query),
    #                 gen_output(results_dict["SMT"], "Synthesis", query)], className="row", style={"width": "130%"}),
    #     html.Div([
    #         gen_output(results_dict["DSC"],
    #                    "Sample descriptor", query),
    #         gen_output(results_dict["MAT"], "Material", query),
    #         gen_output(results_dict["CMT"], "Characterization", query)], className="row", style={"width": "130%"}),
    #     html.Div([gen_output(results_dict["SPL"], "Phase", query)],
    #              className="row", style={"width": "130%"})
    # ])

    return html.Div([
        html.Div([
                    gen_output(results_dict["PRO"], "Property", query),
                    gen_output(results_dict["APL"], "Application", query),
                    gen_output(results_dict["CMT"], "Characterization", query),
                    gen_output(results_dict["SMT"], "Synthesis", query)], className="row"),
        html.Div([
            gen_output(results_dict["DSC"], "Descriptor", query),
            gen_output(results_dict["SPL"], "Phase", query),
            gen_output(results_dict["MAT"], "Material", query)], className="row"),
    ])


def entities_results_html(*args, **kwargs):
    text = str(args[0][0])
    anonymous_formula = [s.strip() for s in args[0][1].split(
        ',')] if not args[0][1] in [None, ''] else []
    element_filters = [s.strip() for s in args[0][2].split(
        ',')] if not args[0][2] in [None, ''] else []
    entities = {f: [s.strip() for s in args[0][i + 3].split(',')] for i, f in enumerate(
        valid_entity_filters) if ((args[0][i + 3] is not None) and (args[0][i + 3].split(',') != ['']))}
    try:
        entities['material'] = entities['material'] + anonymous_formula
    except KeyError:
        entities['material'] = anonymous_formula
    results = rester.entities_search(
        entities, text=text, elements=element_filters, top_k=None)
    if results is not None:
        query = dict()
        for f, fname in [(text, 'text'), (anonymous_formula, 'anonymous_formula'), (element_filters, 'element_filters')]:
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
