import dash_html_components as html


def get_footer():
    """
    Make the plotly dash footer.

    Returns:
        (dash_html_components.Div): The footer

    """
    note_div = html.Div(
        [
            html.Span(
                "Note: This is an alpha release of Matscholar for the purpose "
                "of collecting feedback."
            )
        ],
    )

    about_matscholar = html.A(
        "About Matscholar",
        href="https://github.com/materialsintelligence/matscholar-web",
        target="_blank"
    )

    privacy_policy = html.A(
        "Privacy Policy",
        href='https://www.iubenda.com/privacy-policy/55585319',
        target="_blank"
    )

    submit_feedback = html.A(
        "Submit Feedback",
        href='https://github.com/materialsintelligence/matscholar-web/issues',
        target="_blank"
    )

    footer_link_tree = html.Div(
        [
            about_matscholar,
            html.Span(" | "),
            privacy_policy,
            html.Span(" | "),
            submit_feedback
        ]
    )

    footer_copyright = html.Div(
        html.Span('Copyright © 2019 - Materials Intelligence')
    )

    footer = html.Div(
        [
            note_div,
            footer_link_tree,
            footer_copyright
        ],
        id="footer_container",
        className="content has-text-centered msweb-footer"
    )

    footer_container = html.Div(footer, className="footer")
    return footer_container
