import os

import dash_html_components as html
import dash_core_components as dcc
from dash_elasticsearch_autosuggest import ESAutosuggest

from matscholar_web.common import get_logo_html
from matscholar_web.common import common_warning_html, \
    common_null_warning_html, divider_html
from matscholar_web.constants import valid_search_filters, \
    search_filter_color_map, db_stats, example_searches

"""
View html blocks for the search app.

Please do not define callback logic in this file.
"""


def app_view_html():
    """
    The entire app view (layout) for the search app.

    Returns:
        (dash_html_components.Div): The entire view for the search app.
    """

    return html.Div(
        [
            get_logo_html(),
            search_bar_and_go_html(),
            advanced_search_html(),
            subview_results_container_html()
        ],
    )


def subview_results_container_html():
    """
    The placeholder html block for results. This is updated via callback.

    WANRING: for the loading animation to work correctly, it must be the direct
    parent of an html block which is being updated via callback.

    Args:
        None

    Returns:
        (dash_html_components.Div): The results container.

    """
    my_results_html = html.Div(id="search_results")
    wrapper = dcc.Loading(
        type="cube",
        children=my_results_html,
        className="msweb-fade-in"
    )
    return wrapper


def no_query_warning_html():
    """
    The html block when no query is entered.

    Returns:
        (dash_html_components.Div): The html block when no query is entered.
    """
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
    n_abstracts = "{:,}".format(db_stats["abstracts"])

    n_abstracts_hidden_ref = html.Span(
        id="count-search-hidden-ref",
        children=n_abstracts,
        className="is-hidden"
    )

    n_abstracts_link = dcc.Link(
        id="count-search",
        children=f"{n_abstracts}",
        href="/about",
        className="msweb-fade-in msweb-ubuntu"
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

    search_bar = dcc.Input(
        placeholder=example_searches[-1],
        id="text_input",
        className="input is-info is-medium",
        autoFocus=True,
    )

    sized = "is-size-7"
    tooltip_spans = [html.Span("Keywords: ", className=sized)]
    for k in valid_search_filters:
        color = search_filter_color_map[k]
        tooltip_span = html.Span(k,
                                 className=f"msweb-is-{color}-txt {sized} has-text-weight-bold")
        tooltip_spans.append(tooltip_span)
        tooltip_spans.append(html.Span(", "))

    tooltip_spans.pop(-1)

    search_bar_tooltip = html.Div(
        tooltip_spans,
        className=f"tooltip-text has-margin-0"
    )
    search_bar_html = html.Div(
        [label_container, search_bar, search_bar_tooltip],
        className="flex-column is-narrow tooltip")

    go_button = html.Button(
        "Go",
        id="search-btn",
        className="button is-info is-focused is-medium"
    )
    go_html = html.Div(
        go_button,
        className="flex-column is-narrow has-margin-left-10 has-margin-right-10"
    )

    example_search_button = html.Button(
        "Example",
        id="example-search-btn",
        className="button is-light is-focused is-medium"
    )
    example_search_html = html.Div(
        example_search_button,
        className="flex-column is-narrow has-margin-left-10 has-margin-right-10"
    )

    go_and_example_columns = html.Div(
        [
            go_html,
            example_search_html,
            n_abstracts_hidden_ref
        ],
        className="columns is-centered has-margin-top-10 has-margin-bottom-20"
    )

    search_bar_centered = html.Div(
        search_bar_html,
        className="columns is-centered has-margin-bottom-10"
    )

    bar_and_go_container = html.Div(
        [
            search_bar_centered,
            go_and_example_columns
        ],
        className="container"
    )

    example_search_container = example_searches_html()
    bar_and_go_and_label_container = html.Div(
        [
            example_search_container,
            bar_and_go_container
        ]
        ,
        className="container")
    return bar_and_go_and_label_container


def example_searches_html():
    separator = " | "
    examples_as_string = [e + separator for e in example_searches]
    examples_hidden_ref = html.Span(
        id="search-examples-hidden-ref",
        children=examples_as_string,
        className="is-hidden"
    )
    return examples_hidden_ref


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
                           valid_search_filters]

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

    summary_txt = "Guided search fields"
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


def entity_filter_box_html(field):
    """
    Text filter boxes with ES autosuggest for entity filters.

    Args:
        field (str): Entity type
        prefill_filters (list of str): prefill values
    """
    placeholders = {
        "material": "PbTe, graphite,...",
        "property": "dielectric constant, melting point,...",
        "application": "cathode, catalyst,...",
        "descriptor": "thin film, nanoparticle,...",
        "characterization": "x-ray diffraction, EDS...",
        "synthesis": "sol - gel, firing,...",
        "phase": "perovskite, wurtzite,...",
        "text": "nanoparticle synthesis..."
    }

    ES_field_dict = {
        "material": "materials",
        "property": "properties",
        "application": "applications",
        "descriptor": "descriptors",
        "characterization": "characterization_methods",
        "synthesis": "synthesis_methods",
        "phase": "structure_phase_labels",
        "text": "matscholar_production.entries"
    }

    tooltip_texts = {
        "material": "Material stoichiometries and common names.",
        "property": "Names of measurable materials phenomena.",
        "application": "Commercial and research uses for materials.",
        "descriptor": "Ways to describe bulk materials.",
        "characterization": "Methods for characterizing materials.",
        "synthesis": "Names of procedures for synthesizing materials.",
        "phase": "Proper and common names of phases (nanoscale).",
        "text": "Raw text search to supplement the entity search."
    }

    color = search_filter_color_map[field]
    common_entity_style = f"msweb-is-{color}-txt is-size-5 has-text-weight-semibold"
    entity_txt = '{}:'.format(field.capitalize())
    entity_name = html.Div(entity_txt, className=f"{common_entity_style}")

    tooltip_txt = tooltip_texts[field]
    entity_label_tooltip = html.Div(
        tooltip_txt,
        className=f"tooltip-text is-size-7  has-margin-5"
    )

    # Autosuggest is styled by CSS react classnames ONLY!
    esas = ESAutosuggest(
        fields=['original', 'normalized'],
        endpoint=os.environ['ELASTIC_HOST'] + "/" +
                 ES_field_dict[field] + "/_search",
        defaultField='normalized',
        id=field + "_filters_input",
        placeholder=placeholders[field],
        authUser=os.environ['ELASTIC_USER'],
        authPass=os.environ['ELASTIC_PASS'],
        searchField="original.edgengram",
    )
    # esas = dcc.Input(id=field + "_filters_input")

    textbox = html.Div(
        [entity_name, esas, entity_label_tooltip],
        className="has-margin-right-10 has-margin-left-10 tooltip"
    )
    return textbox
