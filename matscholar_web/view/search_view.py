import dash_html_components as html
import dash_core_components as dcc
from dash_elasticsearch_autosuggest import ESAutosuggest
from matscholar_web.base import *
from os import environ

import dash_elasticsearch_autosuggest


def serve_layout():

    return html.Div([search_bar_and_button_html(), advanced_search_boxes_html(), advanced_search_types_html(), results_html()])
    """
    Basic view: search bar with 'go' button. Advanced search hidden somewhere.

    On search:
    Advanced search side bar

    papers, materials, statistics bar
    results
    """


def search_bar_and_button_html():
    """Returns the html div for the main search bar and search button
    """

    search_bar_html = html.Div(dcc.Input(
        id="text_input",
        type="text",
        autofocus=True,
        placeholder="Enter search terms...",
        style={"width": "100%"}),
        style={"display": "table-cell", "width": "100%"})

    search_button_html = html.Div(html.Button(
        "Search",
        className="button-search",
        id="search-btn"),
        style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"})

    search_bar_and_button = html.Div([search_bar_html, search_button_html], className="row", style={
                                     "display": "table", "marginTop": "10px"})

    return search_bar_and_button


def results_html():
    """
    Html placeholder for results
    """
    abstracts_results_html = html.Div(id='abstracts_results')
    materials_results_html = html.Div(id='materials_results')
    statistics_results_html = html.Div(id='entities_results')

    results = dcc.Loading(
        id="loading-1", children=[abstracts_results_html, materials_results_html, statistics_results_html])

    return results


def advanced_search_types_html():
    """
    Html for the advanced search types, e.g. sort by abstracts, materials, statistics
    """

    # Note that the values are correct input for the rester's group_by parameter on the search method
    advanced_search_types = dcc.RadioItems(
        id='advanced_search_types_radio',
        options=[
            {'label': 'Statistics', 'value': 'entities'},
            {'label': 'Papers', 'value': 'abstracts'},
            {'label': 'Materials', 'value': 'materials'}
        ],
        labelStyle={'display': 'inline-block'},
        value='entities'
    )

    advanced_search_types = html.Div(
        advanced_search_types,
        id='advanced_search_types')

    return advanced_search_types


def advanced_search_boxes_html():
    """
    Html for the advanced search boxes.
    Element filters, entity filters, anonymous formula searches
    """

    filters_label_html = html.Label("Filter by...")

    anonymous_formula_filter_html = html.Div([html.Label("Anonymous Formula:"),
                                              dcc.Input(
        id="anonymous_formula_input",
        type="text",
        autofocus=True,
        placeholder="ABC3, AB2O4,...",
        value=None)],
        style={'width': '240px'}
    )

    element_filter_html = html.Div([html.Label("Elements:"),
                                    dcc.Input(
        id="element_filters_input",
        type="text",
        autofocus=True,
        placeholder="O, -Pb,...",
        value=None)],
        style={'width': '240px'}
    )

    entity_filters_html = [_entity_filter_box_html(
        f) for f in valid_entity_filters]

    advanced_search_boxes = html.Div(
        [filters_label_html, anonymous_formula_filter_html,
            element_filter_html] + entity_filters_html,
        style={'width': '25%', 'float': 'left', 'display': 'inline-block'}, id='advanced_search_boxes')

    return advanced_search_boxes


def _entity_filter_box_html(entity, prefill_filters=None):
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
                    "characterization": "photoluminescence, x-ray diffraction,...",
                    "synthesis": "sol - gel, firing,...",
                    "phase": "perovskite, wurtzite,..."}

    ES_field_dict = {"material": "materials", "property": "properties", "application": "applications", "descriptor": "descriptors",
                     "characterization": "characterization methods", "synthesis": "synthesis methods", "phase": "structure phase labels"}

    if not prefill_filters:
        value = ""
    else:
        value = ",".join(prefill_filters) if len(
            prefill_filters) > 1 else prefill_filters[0]
    textbox = html.Div([html.Label('{}:'.format(entity.capitalize())),
                        ESAutosuggest(
        fields=['original', 'normalized'],
        endpoint=environ['ELASTIC_HOST'] + "/" +
        ES_field_dict[entity] + "/_search",
        defaultField='original',
        id=entity + "_filters_input",
        placeholder=placeholders[entity],
        authUser=environ['ELASTIC_USER'],
        authPass=environ['ELASTIC_PASS'],
        searchField="original.edgengram",
        value=value)
    ],
        style={'padding': 5, 'width': '25%'}
    )
    return textbox
