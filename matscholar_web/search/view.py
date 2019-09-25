import dash_html_components as html
import dash_core_components as dcc
from dash_elasticsearch_autosuggest import ESAutosuggest
from os import environ
import urllib

from matscholar_web.constants import valid_entity_filters, entity_shortcode_map, entity_color_map_bulma


def serve_layout(search):
    if search:
        search_dict = urllib.parse.parse_qs(
            search[1:])
    else:
        search_dict = dict()  # print(urllib.parse.parse_qs(path))

    return html.Div([
        entity_display_html(),
        search_bar_and_button(),
        advanced_search_boxes_html(search_dict),
        results_html()])


def entity_display_html():
    live_entity_search = dcc.Input(
        placeholder="Enter a query here directly or with the entity search boxes below...",
        id="text_input",
        className="input is-success has-min-width-100 is-size-4",
        autoFocus=True,
        # n_submit=0
    )
    live_entity_search_container = html.Div(live_entity_search,
                                            className="columns is-centered has-margin-20")
    lesc2 = html.Div(live_entity_search_container, className="container")
    return lesc2


def results_html():
    """
    Html placeholder for results
    """
    my_results_html = html.Div(id="search_results")

    results = dcc.Loading(
        type="cube",
        children=[my_results_html],
    )

    results_container = html.Div(results)

    return results_container



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
    advanced_search_types = dcc.Dropdown(
        id='search_type_dropdown',
        options=[
            {'label': 'Statistics (on named entities/words)', 'value': 'entities'},
            {'label': 'Relevant Papers', 'value': 'abstracts'},
            {'label': 'Similar Materials', 'value': 'materials'},
            {'label': 'Everything', 'value': 'everything'},
            {'label': "Select a search type", "value": "no_selection"}
        ],
        value="no_selection"
    )

    advanced_search_types = html.Div(
        advanced_search_types,
        id='advanced_search_types',
        className="column is-one-fifth"
    )

    return advanced_search_types


def search_bar_and_button():
    button = go_button()
    dropdown = search_type_dropdown()
    button_and_dropdown = html.Div(
        [dropdown, button],
        className="columns is-centered"
    )
    return button_and_dropdown


def advanced_search_boxes_html(search_dict):
    """
    Html for the advanced search boxes.
    Element filters, entity filters, anonymous formula searches
    """
    entity_filters_html = [_entity_filter_box_html(
        f, search_dict) for f in valid_entity_filters]

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
        className="has-margin-bottom-100"
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

    entity_name = html.Span('{}:'.format(entity.capitalize()))

    color = entity_color_map_bulma[entity]
    entity_label = html.Label(entity_name)
    entity_label_container = html.Div(entity_label, className=f"has-text-{color} is-size-5 has-text-weight-semibold")

    # Autosuggest is styled by CSS react classnames ONLY!
    esas = ESAutosuggest(
        fields=['original', 'normalized'],
        endpoint=environ['ELASTIC_HOST'] + "/" +
                 ES_field_dict[entity] + "/_search",
        defaultField='original',
        id=entity + "_filters_input",
        placeholder=placeholders[entity],
        authUser=environ['ELASTIC_USER'],
        authPass=environ['ELASTIC_PASS'],
        searchField="original.edgengram",
        value=prefill,
        # className="input is-success has-max-width-350"
    )

    textbox = html.Div([entity_label_container, esas], className="has-margin-10")
    return textbox
