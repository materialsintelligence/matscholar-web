from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import copy
import urllib
from matscholar_web.constants import rester, valid_entity_filters, \
    entity_shortcode_map

MAX_N_ROWS_FOR_EACH_ENTITY_TABLE = 10

def gen_output(most_common, entity_type, class_name="three column"):
    entity_shortcode = entity_shortcode_map[entity_type.lower()]
    header_entity_type = html.Th(entity_type, className="highlighted {}".format(entity_shortcode))
    header_score = html.Th("score", className="highlighted {}".format(entity_shortcode))
    header = html.Tr([header_entity_type, header_score])

    rows = [None] * len(most_common)

    row_number = 0
    for ent, count, score in most_common:
        entity = html.Td(ent)
        score = html.Td('{:.2f}'.format(score))
        rows[row_number] = [entity, score]
        row_number += 1
        if row_number == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE - 1:
            break

    table = html.Table([header] + rows)
    return html.Div(table)


def gen_table(results_dict):
    return html.Div([
        html.Div([
            gen_output(results_dict["PRO"], "Property"),
            gen_output(results_dict["APL"], "Application"),
            gen_output(results_dict["CMT"], "Characterization"),
            gen_output(results_dict["SMT"], "Synthesis")]),
        html.Div([
            gen_output(results_dict["DSC"], "Descriptor"),
            gen_output(results_dict["SPL"], "Phase"),
            gen_output(results_dict["MAT"], "Material")]),
    ])




# def entities_results_html(n_clicks, dropdown_value, search_text):
#     print(n_clicks, dropdown_value, search_text)
#     return "No results"


def entities_results_html(n_clicks, dropdown_value, search_text):

    #{'material': ['PbTe'], 'property': ['dielectric constants'], 'application': ['cathode ray tube'], 'descriptor': ['thin film'], 'characterization': ['photoluminescence'], 'synthesis': ['firing'], 'phase': ['wurtzite']}

    # n_clicks =

    entities_text_list = search_text.split(",")
    entity_query = {k: [] for k in valid_entity_filters}
    entities_as_text = []
    for et in entities_text_list:
        for k in valid_entity_filters:
            entity_type_key = f"{k}:"
            if entity_type_key in et:
                query_entity_term = copy.deepcopy(et)
                query_entity_term = query_entity_term.replace(entity_type_key, "").strip()
                entity_query[k].append(query_entity_term)
                entities_as_text.append(query_entity_term)
    text = ", ".join(entities_as_text)

    entity_query = {k: v for k, v in entity_query.items() if v}

    print(entity_query)
    print(text)

    results = rester.entities_search(entity_query, text=None, top_k=None)

    print(results)

    if results is None or not any([v for v in results.values()]):
        no_results = html.Div(f"No results found!", className="column is-size-2")
        no_results_container = html.Div(no_results, className="columns is-centered")
        return no_results_container
    else:
        return gen_table(results)
