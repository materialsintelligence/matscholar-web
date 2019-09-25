from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.constants import rester, valid_entity_filters, \
    entity_shortcode_map, entity_color_map
from matscholar_web.search.util import parse_search_box, no_results

MAX_N_ROWS_FOR_EACH_ENTITY_TABLE = 10


def entities_results_html(search_text):
    entity_query = parse_search_box(search_text)
    results = rester.entities_search(entity_query, text=None, top_k=None)
    if results is None or not any([v for v in results.values()]):
        return no_results()
    else:
        all_tables = get_all_score_tables(results)
        all_tables_container = html.Div(all_tables, className="container has-margin-top-20 has-margin-bottom-20")
        return all_tables_container


def get_all_score_tables(results_dict):
    columns_classes = "columns is-desktop is-centered"

    half = "is-one-half"
    third = "is-one-third"

    row1 = html.Div(
        [
            get_score_table_for_entity(results_dict["PRO"], "Property", half),
            get_score_table_for_entity(results_dict["APL"], "Application", half),
        ],
        className=columns_classes
    )

    row2 = html.Div(
        [
            get_score_table_for_entity(results_dict["CMT"], "Characterization", half),
            get_score_table_for_entity(results_dict["SMT"], "Synthesis", half),
        ],
        className=columns_classes
    )

    row3 = html.Div(
        [
            get_score_table_for_entity(results_dict["DSC"], "Descriptor", third),
            get_score_table_for_entity(results_dict["SPL"], "Phase", third),
            get_score_table_for_entity(results_dict["MAT"], "Material", third)
        ],
        className=columns_classes
    )

    row4 = html.Div(
        [
        ],
        className=columns_classes
    )
    return html.Div([row1, row2, row3, row4])


def get_score_table_for_entity(most_common, entity_type, width):
    n_results = len(most_common)
    header_style = "msweb-entity-result-table-blue"
    header_entity_type = html.Th(f"{entity_type}: ({n_results} entities)", className=header_style)
    header_score = html.Th("score", className=header_style)
    header = html.Tr([header_entity_type, header_score])

    rows = [None] * n_results

    row_number = 0
    for ent, count, score in most_common:
        entity = html.Td(ent, className="has-width-50")
        score = html.Td('{:.2f}'.format(score), className="has-width-50")
        rows[row_number] = html.Tr([entity, score])
        row_number += 1
        if row_number == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE - 1:
            break
    table = html.Table([header] + rows, className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped")
    return html.Div(table, className=f"column {width}")





