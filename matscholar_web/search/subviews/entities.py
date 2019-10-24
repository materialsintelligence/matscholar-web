import dash_html_components as html
from matscholar_web.constants import rester, entity_color_map
from matscholar_web.search.common import no_results_html, \
    results_container_class, get_results_label_html

MAX_N_ROWS_FOR_EACH_ENTITY_TABLE = 10


def entities_results_html(entity_query, raw_text):
    results = rester.entities_search(entity_query, text=raw_text,
                                     top_k=MAX_N_ROWS_FOR_EACH_ENTITY_TABLE)
    if results is None or not any([v for v in results.values()]):
        return no_results_html()
    else:
        all_tables = get_all_score_tables(results)
        big_results_label = get_results_label_html("entities")
        all_tables_container = html.Div(
            children=[big_results_label, all_tables],
            className=results_container_class()
        )
        return all_tables_container


def get_all_score_tables(results_dict):
    columns_classes = "columns is-desktop is-centered"

    half = "is-half"
    third = "is-one-third"

    row1 = html.Div(
        [
            get_score_table_for_entity(results_dict["PRO"], "Property", half),
            get_score_table_for_entity(results_dict["APL"], "Application",
                                       half),
        ],
        className=columns_classes
    )

    row2 = html.Div(
        [
            get_score_table_for_entity(results_dict["CMT"], "Characterization",
                                       half),
            get_score_table_for_entity(results_dict["SMT"], "Synthesis", half),
        ],
        className=columns_classes
    )

    row3 = html.Div(
        [
            get_score_table_for_entity(results_dict["DSC"], "Descriptor",
                                       third),
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

    formatted_n_results = min(n_results, MAX_N_ROWS_FOR_EACH_ENTITY_TABLE)
    if formatted_n_results == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE:
        table_label = f"Top {formatted_n_results} entities"
    else:
        table_label = f"All {formatted_n_results} entities"

    color = entity_color_map[entity_type.lower()]
    header_entity_type = html.Span(f"{entity_type}",
                                   className=f"msweb-has-{color}-txt")
    header_table_label = html.Span(f": {table_label}")

    header_entity_type = html.Th([header_entity_type, header_table_label])
    header_score = html.Th("score")
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
    table = html.Table([header] + rows,
                       className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped")
    return html.Div(table, className=f"column {width}")
