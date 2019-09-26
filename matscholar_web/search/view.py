import os

import dash_html_components as html
import dash_core_components as dcc
from dash_elasticsearch_autosuggest import ESAutosuggest

from matscholar_web.common import common_warning_html
from matscholar_web.constants import valid_entity_filters, \
    entity_color_map_bulma


def serve_layout():
    return html.Div(
        [
            entity_search_html(),
            search_dropdown_and_button_html(),
            advanced_search_boxes_html(),
            subview_results_container_html()
        ]
    )


def subview_results_container_html():
    """
    Html placeholder for results
    """
    my_results_html = html.Div(id="search_results")
    wrapper = dcc.Loading(
        type="cube",
        children=my_results_html,
    )
    return wrapper


def no_query_warning_html():
    no_query_txt = html.Div(
        f"Please enter a query using the search bar, then hit \"Go\".",
        className="is-size-4"
    )
    no_query_container = html.Div(
        no_query_txt,
        className="container has-text-centered has-margin-top-50"
    )
    return no_query_container


def malformed_query_warning_html(bad_search_txt):
    warning_header_txt = f'Oops, we didn\'t understand that search.'
    warning_body_txt = \
        f'\n Your search was: "{bad_search_txt}"\n. Try the format entity1: ' \
        f'value1, entity2: value2. For example: "material: PbTe, ' \
        f'property: thermoelectric"'
    return common_warning_html(warning_header_txt, warning_body_txt)


def entity_search_html():
    label = html.Label(
        "Search 5,000,000+ materials science papers with named entity "
        "recognition",
        className="is-size-4-desktop has-margin-5"
    )
    label_container = html.Div(label, className="has-text-centered")

    live_entity_search = dcc.Input(
        placeholder="Enter a query here directly or with the entity search boxes below...",
        id="text_input",
        className="input is-info is-medium",
        autoFocus=True,
    )
    live_entity_search_column = html.Div(live_entity_search,
                                            className="column is-half")
    live_entity_search_columns = html.Div([live_entity_search_column], className="columns is-centered")
    live_entity_search_container = html.Div(live_entity_search_columns, className="container")
    lesc2 = html.Div(
        [
            label_container,
            live_entity_search_container
        ]
        ,
        className="container")
    return lesc2


def go_button():
    """Returns the html div for the main search bar and search button
    """
    search_button_html = html.Div(html.Button(
        "Go",
        id="search-btn",
        className="button is-warning is-focused is-size-6"
    ),
        className="column is-narrow"
    )
    return search_button_html


def search_type_dropdown():
    """
    Html for the advanced search types, e.g. sort by abstracts, materials, statistics
    """

    # Note that the values are correct input for the rester's group_by parameter on the search method
    search_dropdown = dcc.Dropdown(
        id='search_type_dropdown',
        options=[
            {'label': 'Statistics (on named entities/words)',
             'value': 'entities'},
            {'label': 'Relevant Papers', 'value': 'abstracts'},
            {'label': 'Similar Materials', 'value': 'materials'},
            {'label': 'Everything', 'value': 'everything'},
            {'label': "Select a search type", "value": "no_selection"}
        ],
        value="no_selection"
    )

    search_dropdown = html.Div(
        search_dropdown,
        className="column is-one-quarter"
    )

    return search_dropdown


def search_dropdown_and_button_html():
    button = go_button()
    dropdown = search_type_dropdown()
    button_and_dropdown = html.Div(
        [dropdown, button],
        className="columns is-centered"
    )
    return button_and_dropdown


def advanced_search_boxes_html():
    """
    Html for the advanced search boxes.
    Element filters, entity filters, anonymous formula searches
    """

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
        className="container"
    )

    return advanced_search_boxes


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
        defaultField='original',
        id=entity + "_filters_input",
        placeholder=placeholders[entity],
        authUser=os.environ['ELASTIC_USER'],
        authPass=os.environ['ELASTIC_PASS'],
        searchField="original.edgengram",
    )

    textbox = html.Div([entity_label_container, esas],
                       className="has-margin-10")
    return textbox
