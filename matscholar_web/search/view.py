import os

import dash_html_components as html
import dash_core_components as dcc
from dash_elasticsearch_autosuggest import ESAutosuggest

from matscholar_web.common import common_warning_html, \
    common_null_warning_html, divider_html
from matscholar_web.constants import valid_entity_filters, \
    entity_color_map_bulma, db_stats, example_searches


def serve_layout():
    return html.Div(
        [
            search_bar_and_go_html(),
            advanced_search_html(),
            subview_results_container_html()
        ],
    )


def subview_results_container_html():
    """
    Html placeholder for results
    """
    my_results_html = html.Div(id="search_results")
    wrapper = dcc.Loading(
        type="cube",
        children=my_results_html,
        className="msweb-fade-in"
    )
    return wrapper


def no_query_warning_html():
    null_txt = \
        f"Please enter a query using the search bar, then hit Enter or \"Go\"."
    return common_null_warning_html(null_txt)


def malformed_query_warning_html(bad_search_txt):
    warning_header_txt = f'Oops, we didn\'t understand that search.'
    warning_body_txt = \
        f'\n Your search was: "{bad_search_txt}"\n. Try the format entity1: ' \
        f'value1, entity2: value2. For example: "material: PbTe, ' \
        f'property: thermoelectric"'
    return common_warning_html(warning_header_txt, warning_body_txt)


def search_bar_and_go_html():
    search_bar = dcc.Input(
        placeholder="Enter a query here directly or with the entity search boxes below...",
        id="text_input",
        className="input is-info is-medium",
        autoFocus=True,
    )
    search_bar_html = html.Div(search_bar, className="column is-half")

    go_button = html.Button(
        "Go",
        id="search-btn",
        className="button is-warning is-focused is-medium"
    )

    go_html = html.Div(
        go_button,
        className="column is-narrow"
    )

    n_abstracts = "{:,}".format(db_stats["abstracts"])

    n_abstracts_hidden_ref = html.Span(
        id="count-search-hidden-ref",
        children=n_abstracts,
        className="is-hidden"
    )

    n_abstracts_link = dcc.Link(
        id="count-search",
        children=f"{n_abstracts}",
        href="/about#journals",
        className="msweb-fade-in"
    )

    label = html.Label(
        [
            "Search ",
            n_abstracts_link,
            " materials science abstracts with named entity recognition"
        ],
        className="is-size-4-desktop has-margin-5"
    )
    label_container = html.Div(label, className="has-text-centered")
    bar_and_go_columns = html.Div([search_bar_html, go_html, n_abstracts_hidden_ref],
                                  className="columns is-centered")

    bar_and_go_container = html.Div(bar_and_go_columns, className="container")

    example_search_container = example_searches_html()
    bar_and_go_and_label_container = html.Div(
        [
            label_container,
            example_search_container,
            bar_and_go_container
        ]
        ,
        className="container")
    return bar_and_go_and_label_container


def example_searches_html():

    common_text_style = "is-small"
    prefix = html.Span("Try an example search: ", className=common_text_style)

    separator = " | "
    examples_as_string = [e + separator for e in example_searches]
    examples_hidden_ref = html.Span(
        id="search-examples-hidden-ref",
        children=examples_as_string,
        className="is-hidden"
    )

    examples_displayed = html.Span(
        id="search-examples",
        children=example_searches[0],
        className=common_text_style
    )

    example_search_container = html.Div(
        [
            prefix,
            examples_displayed,
            examples_hidden_ref
        ],
        className="container is-pulled-left"
    )
    return example_search_container

def advanced_search_html():
    """
    Html for the advanced search boxes.
    Element filters, entity filters, anonymous formula searches
    """
    hr = divider_html()
    dropdown = dcc.Dropdown(
        id='search_type_dropdown',
        options=[
            {'label': 'Search for: Statistics (on named entities/words)',
             'value': 'entities'},
            {'label': 'Search for: Relevant Papers', 'value': 'abstracts'},
            {'label': 'Search for: Summary of Materials', 'value': 'materials'},
            {'label': 'Search for: Everything', 'value': 'everything'},
        ],
        value="everything"
    )
    dropdown_column = html.Div(dropdown, className="column is-fullwidth")
    dropdown_columns = html.Div(
        [dropdown_column],
        className="columns is-centered"
    )
    dropdown_container = html.Div(dropdown_columns,
                                  className="container has-margin-5")

    entity_filters_html = [entity_filter_box_html(f) for f in
                           valid_entity_filters]

    entity_filter_row_1 = html.Div(entity_filters_html[0:3],
                                   className="columns is-centered")
    entity_filter_row_2 = html.Div(entity_filters_html[3:6],
                                   className="columns is-centered")
    entity_filter_row_3 = html.Div(entity_filters_html[6:9],
                                   className="columns is-centered")
    entity_filter_rows = [entity_filter_row_1, entity_filter_row_2,
                          entity_filter_row_3]

    advanced_search_boxes = html.Div(
        entity_filter_rows,
        id='advanced_search_boxes',
        className="container has-margin-top-10"
    )

    summary_txt = "Advanced search options"
    summary = html.Summary(summary_txt, className="has-text-centered is-size-6")
    hidden_column = html.Details(
        [hr, dropdown_container, summary, advanced_search_boxes],
        className="column is-half"
    )

    hidden_columns = html.Div(hidden_column, className="columns is-centered")
    hidden_container = html.Div(
        [
            hidden_columns
        ],
        className="container"
    )

    return hidden_container


def entity_filter_box_html(entity):
    """
    Text filter boxes with ES autosuggest for entity filters.

    Args:
        entity (str): Entity type
        prefill_filters (list of str): prefill values
    """
    placeholders = {"material": "PbTe, graphite,...",
                    "property": "dielectric constant, melting point,...",
                    "application": "cathode, catalyst,...",
                    "descriptor": "thin film, nanoparticle,...",
                    "characterization": "x-ray diffraction, EDS...",
                    "synthesis": "sol - gel, firing,...",
                    "phase": "perovskite, wurtzite,..."}

    ES_field_dict = {"material": "materials", "property": "properties",
                     "application": "applications", "descriptor": "descriptors",
                     "characterization": "characterization_methods",
                     "synthesis": "synthesis_methods",
                     "phase": "structure_phase_labels"}

    entity_name = html.Span('{}:'.format(entity.capitalize()))

    color = entity_color_map_bulma[entity]
    entity_label = html.Label(entity_name)
    entity_label_container = html.Div(entity_label,
                                      className=f"has-text-{color} is-size-5 has-text-weight-semibold")

    # Autosuggest is styled by CSS react classnames ONLY!
    esas = ESAutosuggest(
        fields=['original', 'normalized'],
        endpoint=os.environ['ELASTIC_HOST'] + "/" +
                 ES_field_dict[entity] + "/_search",
        defaultField='normalized',
        id=entity + "_filters_input",
        placeholder=placeholders[entity],
        authUser=os.environ['ELASTIC_USER'],
        authPass=os.environ['ELASTIC_PASS'],
        searchField="original.edgengram",
    )

    textbox = html.Div([entity_label_container, esas],
                       className="has-margin-10")
    return textbox
