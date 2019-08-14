import dash_html_components as html
import dash_materialsintelligence as dmi
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from matscholar_web.base import *
from matscholar_web.callbacks.results_views.abstracts_results_view import abstracts_results_html
from matscholar_web.callbacks.results_views.materials_results_view import materials_results_html
from matscholar_web.callbacks.results_views.entities_results_view import entities_results_html


def bind(app):
    @app.callback(
        [Output("abstracts_results", "style"), Output(
            "materials_results", "style"), Output("statistics_results", "style")],
        [Input("advanced_search_types_radio", "value")],
        [State("advanced_search_types_radio", "value")]
    )
    def toggle_search_type(radio_in, radio_val):
        """
        Toggle the search type using the search type buttons
        """
        visible_style = {'width': '75%',
                         'float': 'right', 'display': 'inline-block'}
        hidden_style = {"display": "none"}
        if radio_val == "abstracts":
            return visible_style, hidden_style, hidden_style
        elif radio_val == "materials":
            return hidden_style, visible_style, hidden_style
        else:
            return hidden_style, hidden_style, visible_style

    @app.callback(
        Output('abstracts_results', 'children'),
        [Input('search-btn', 'n_clicks')],
        [State("advanced_search_types_radio", "value"),
         State("text_input", "value"),
         State("anonymous_formula_input", "value"),
         State("element_filters_input", "value")] +
        [State(f + '_filters_input', "value") for f in valid_entity_filters]
    )
    def show_abstracts_results(*args, **kwargs):
        """
        Perform a search for abstracts and display the results
        """
        print(args)
        print(kwargs)
        if args[0] is not None:
            if args[1] == 'abstracts':
                return abstracts_results_html(list(args)[2:])

    @app.callback(
        Output('materials_results', 'children'),
        [Input('search-btn', 'n_clicks')],
        [State("advanced_search_types_radio", "value"),
         State("text_input", "value"),
         State("anonymous_formula_input", "value"),
         State("element_filters_input", "value")] +
        [State(f + '_filters_input', 'value') for f in valid_entity_filters]
    )
    def show_materials_results(*args, **kwargs):
        if args[0] is not None:
            if args[1] == 'materials':
                return materials_results_html(list(args)[2:])

    @app.callback(
        Output('entities_results', 'children'),
        [Input('search-btn', 'n_clicks')],
        [State("advanced_search_types_radio", "value"),
         State("text_input", "value"),
         State("anonymous_formula_input", "value"),
         State("element_filters_input", "value")] +
        [State(f + '_filters_input', 'value') for f in valid_entity_filters]
    )
    def show_entities_results(*args, **kwargs):
        if args[0] is not None:
            if args[1] == 'entities':
                return entities_results_html(list(args)[2:])
