from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.base import *


def gen_output(most_common, entity_type, query, class_name="three column"):
    query = [(key, value) for key, value in query.items()]
    table = html.Table(
        [html.Tr([html.Th(entity_type), html.Th("score", style={"textAlign": "right", "fontWeight": "normal"})],
                 className="summary-header")] +
        [html.Tr([
            html.Td(
                html.A(ent, href="/search/{}/{}/{}".format(entity_type.lower(), ent, query))),
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
        gen_output(results_dict["PRO"], "Property", query),
        gen_output(results_dict["APL"], "Application", query),
        gen_output(results_dict["SMT"], "Synthesis", query),
        gen_output(results_dict["DSC"], "Sample descriptor", query),
        gen_output(results_dict["MAT"], "Material", query),
        gen_output(results_dict["CMT"], "Characterization", query),
        gen_output(results_dict["SPL"], "Phase", query)
    ])


def entities_results_html(*args, **kwargs):
    text = str(args[0][0])
    anonymous_formula = args[0][1]
    element_filters = [s.strip() for s in args[0][2].split(
        ',')] if not args[0][2] in [None, ''] else []
    entities = {f: [s.strip() for s in args[0][i + 3].split(',')] for i, f in enumerate(
        valid_entity_filters) if ((args[0][i + 3] is not None) and (args[0][i + 3].split(',') != ['']))}
    results = rester.entities_search(
        entities, text=text, elements=element_filters, top_k=None)
    query = {**entities, **{'element_filters': element_filters}, **{"anonymous_formula": anonymous_formula}, **{"text": text}}
    return gen_table(results, query=query)
