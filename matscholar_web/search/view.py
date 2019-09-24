import dash_html_components as html
import dash_core_components as dcc
from dash_elasticsearch_autosuggest import ESAutosuggest
from matscholar_web.constants import valid_entity_filters, highlight_mapping
from os import environ
import urllib
import json
from collections import defaultdict
import dash_elasticsearch_autosuggest
import ast


def serve_layout(search):
    if search:
        search_dict = urllib.parse.parse_qs(
            search[1:])
    else:
        search_dict = dict()  # print(urllib.parse.parse_qs(path))

    return html.Div([search_bar_and_button_html(search_dict),
                     advanced_search_types_html(),
                     advanced_search_boxes_html(search_dict),
                     entity_display_html(),
                     results_html()])
    """
    Basic view: search bar with 'go' button. Advanced search hidden somewhere.

    On search:
    Advanced search side bar

    papers, materials, statistics bar
    results
    """


def entity_display_html():
    div = html.Div([html.H3(id='live_entity_display')], className="row")
    return div


def search_bar_and_button_html(search_dict):
    """Returns the html div for the main search bar and search button
    """

    search_bar_html = html.Div(dcc.Input(
        id="text_input",
        type="text",
        autoFocus=True,
        value=search_dict.get('text'),
        placeholder="Enter search terms...",
        style={"width": "100%"}),
        style={"display": "table-cell", "width": "100%"})

    search_button_html = html.Div(html.Button(
        "Search",
        className="button-search",
        id="search-btn"),
        style={"display": "table-cell", "verticalAlign": "top",
               "paddingLeft": "10px"})

    # search_bar_and_button = html.Div([search_bar_html,
    #                                   search_button_html],
    #                                  className="row", style={
    #         "display": "table", "marginTop": "10px"})
    # return search_bar_and_button
    return search_button_html


def results_html():
    """
    Html placeholder for results
    """

    abstracts_results_html = html.Div(id='abstracts_results')
    materials_results_html = html.Div(id='materials_results')
    statistics_results_html = html.Div(id='entities_results')

    results = dcc.Loading(
        id="loading-1",
        children=[abstracts_results_html, materials_results_html,
                  statistics_results_html])

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


def advanced_search_boxes_html(search_dict):
    """
    Html for the advanced search boxes.
    Element filters, entity filters, anonymous formula searches
    """

    filters_label_html = html.Label("Filter by...")

    anonymous_formula_filter_html = html.Div([html.Label("Anonymous Formula:"),
                                              dcc.Input(
                                                  id="anonymous_formula_input",
                                                  type="text",
                                                  autoFocus=True,
                                                  placeholder="*Te, *1*2O4,...",
                                                  value=search_dict.get(
                                                      'anonymous_formula'))],
                                             style={'width': '240px'}
                                             )

    element_filter_html = html.Div([html.Label("Elements:"),
                                    dcc.Input(
                                        id="element_filters_input",
                                        type="text",
                                        autoFocus=True,
                                        placeholder="O, -Pb,...",
                                        value=search_dict.get(
                                            'element_filters'))],
                                   style={'width': '240px'}
                                   )

    entity_filters_html = [_entity_filter_box_html(
        f, search_dict) for f in valid_entity_filters]

    # advanced_search_boxes = html.Div(
    #     [filters_label_html, anonymous_formula_filter_html,
    #      element_filter_html] + entity_filters_html,
    #     style={'width': '25%', 'float': 'left', 'display': 'inline-block'},
    #     id='advanced_search_boxes')

    advanced_search_boxes = html.Div(
        entity_filters_html,
        # style={'width': '25%', 'float': 'left', 'display': 'inline-block'},
        style={"display": "table", "align": "center"},
        id='advanced_search_boxes',
        className="row"
    )

    return advanced_search_boxes


def _entity_filter_box_html(entity, search_dict):
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

    ES_field_dict = {"material": "materials", "property": "properties",
                     "application": "applications", "descriptor": "descriptors",
                     "characterization": "characterization methods",
                     "synthesis": "synthesis methods",
                     "phase": "structure phase labels"}

    try:
        prefill = str(search_dict.get(entity)[0])
    except TypeError:
        prefill = None
    textbox = html.Div([html.Label(html.Span('{}:'.format(entity.capitalize()),
                                             className="highlighted {}".format(
                                                 highlight_mapping[entity])),
                                   style={"display": "table"},
                                   className="row"),
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
                            value=prefill)
                        ],
                       style={"float": "left"}
                       # style={'padding': 5, 'width': '25%'}
                       # style={"diplay":"table", "padding": 5},
                       # className="row"
                       )
    return textbox
