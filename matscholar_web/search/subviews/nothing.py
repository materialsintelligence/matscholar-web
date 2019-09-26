import dash_html_components as html


def no_selection_html():
    no_selection_text = html.Div(
        f"Please select a search type before searching.",
        className="is-size-4"
    )
    no_selection_container = html.Div(
        no_selection_text,
        className="container has-text-centered has-margin-top-50"
    )
    return no_selection_container
