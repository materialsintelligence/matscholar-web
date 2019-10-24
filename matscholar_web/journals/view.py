import dash_html_components as html
import dash_core_components as dcc

from matscholar_web.constants import db_stats
from matscholar_web.common import divider_html, common_info_box_html, \
    common_header_style, common_body_style, common_title_style


def serve_layout():
    journals = get_journals_html()

    return html.Div(
        [
            journals,
        ]
    )


def get_journals_html():
    """

    Returns:

    """
    journals = db_stats["journals"]
    n_journals = "{:,}".format(len(journals))

    journal_info_header_txt = "Journals in Matscholar"
    journal_info_subheader_txt = f"Search among {n_journals} scientific journals"
    journals_info_body_txt = \
        f"Matscholar at present contains processed abstracts from " \
        f"{n_journals} peer-reviewed scientific journals from multiple " \
        f"scientific domains, including inorganic materials, polymers, " \
        f"biomaterials, and more. You can search for which journals we " \
        f"have parsed at least one paper from using the search box below."

    journal_info_header = html.Div(journal_info_header_txt,
                                   className=common_title_style())
    journal_info_subheader = html.Div(journal_info_subheader_txt,
                                      className=common_header_style())
    journal_info_body = html.Div(journals_info_body_txt,
                                 className=common_body_style())

    jkeys = [{"label": v, "value": str(i)} for i, v in enumerate(journals)]
    dropdown = dcc.Dropdown(
        placeholder="Search for your favorite journal...",
        options=jkeys,
        className="is-size-6 has-margin-bottom-50",
        clearable=False,
        multi=True,
        optionHeight=25
    )
    dropdown_label = html.Div("Search our collection",
                              className=common_header_style())

    hr_dropdown = divider_html()

    elements = [
        journal_info_header,
        journal_info_subheader,
        journal_info_body,
        hr_dropdown,
        dropdown_label,
        dropdown,
    ]

    container = common_info_box_html(elements, id="journals")
    return container
