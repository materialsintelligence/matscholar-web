import dash_core_components as dcc
import dash_html_components as html

from matscholar_web.common import (
    common_body_style,
    common_header_style,
    common_info_box_html,
    common_stat_style,
    logo_html,
)
from matscholar_web.constants import db_stats


"""
View html blocks for the about app.

Please do not define callback logic in this file.
"""


def app_view_html():
    """
    The entire app view (layout) for the about app.

    Returns:
        (dash_html_components.Div): The entire view for the about app.
    """
    introduction = introduction_html()

    return html.Div([introduction])


def introduction_html():
    """
    The introduction block.

    Returns:
        (dash_html_components.Div): The introduction html block.

    """
    logo = logo_html()
    introduction_subheader_txt = (
        "A scholarly (AI) assistant for materials science \n"
    )
    introduction_body_txt = (
        "Matscholar is a research effort based out of the Lawrence Berkeley "
        "National Lab and led by the "
        "[HackingMaterials](https://hackingmaterials.lbl.gov), "
        "[Persson](https://perssongroup.lbl.gov) "
        "([Materials Project](https://materialsproject.org)) and "
        "[Ceder](https://ceder.berkeley.edu) research groups. The aim of "
        "Matscholar is to organize the world's materials knowlegde by "
        "applying Natural Language Processing (NLP) to materials science "
        "literature. To date, our database contains "
    )

    introduction_body_txt2 = (
        "We are continuing to periodically update "
        "our collections with the latest and greatest advancements in the "
        "field of materials science. You can read more about our work in the "
        "following publications:"
    )

    publication_header_txt = "Publications:"

    reference_1_txt = (
        "Weston, L., Tshitoyan, V., Dagdelen, J., Kononova, O., "
        "Trewartha, A., Persson, K., Ceder, G., Jain, A. (2019) *Named "
        "Entity Recognition and Normalization Applied to Large-Scale "
        "Information Extraction from the Materials Science Literature.* "
        "**J. Chem. Inf. Model.** 2019, 59, 9, 3692-3702 "
        "**[https://doi.org/10.1021/acs.jcim.9b00470]"
        "(https://doi.org/10.1021/acs.jcim.9b00470)**"
    )

    reference_2_txt = (
        "Tshitoyan, V., Dagdelen, J., Weston, L., Dunn, A., Rong, Z., "
        "Kononova, O., Persson, K., Ceder, G., Jain, A. (2019). "
        "*Unsupervised word embeddings "
        "capture latent knowledge from materials science literature.* "
        "**Nature**, 571(7763), 95–98. "
        "**[https://doi.org/10.1038/s41586-019-1335-8]"
        "(https://doi.org/10.1038/s41586-019-1335-8)**"
    )

    why_use_header_txt = "Why use Matscholar?"
    why_use_body_txt = (
        "1. **It's free**: Matscholar is available freely anywhere in the "
        "world. We release our finished NLP codes feely on "
        "[Github](https://github.com/materialsintelligence) "
        "(including the source code for this website). We also provide an "
        "python API for querying our databae which you can find on our "
        "[Github](https://github.com/materialsintelligence/matscholar).\n"
        "2. **It goes beyond what Google Scholar "
        "can do**: Matscholar goes beyond full text searches and uses "
        "specifically-trained *materials-related* entities to search "
        "millions of abstracts.\n 3. **It's (relatively) fast**: And getting "
        "faster! We are actively working on our infrastructure to make "
        "Matscholar faster, more accurate, and more informative."
    )

    funding_header_txt = "Our funding sources"
    funding_body_txt = (
        "Matscholar is supported by the "
        "[Toyota Research Institute](https://www.tri.global) through the "
        "Accelerated Materials Design and Discovery program. Abstract data "
        "was downloaded from the ScienceDirect API between October 2017 and "
        "September 2018, and the Scopus API in July 2019 via "
        "http://api.elsevier.com and http://www.scopus.com. Abstract "
        "data was also downloaded from the SpringerNature API and Royal "
        "Society of Chemistry sources."
    )

    introduction_body_md = dcc.Markdown(introduction_body_txt)
    introduction_body_md2 = dcc.Markdown(introduction_body_txt2)
    why_use_body_md = dcc.Markdown(why_use_body_txt)
    reference_1_md = dcc.Markdown(reference_1_txt)
    reference_2_md = dcc.Markdown(reference_2_txt)
    funding_md = dcc.Markdown(funding_body_txt)

    introduction_subheader = html.Div(
        introduction_subheader_txt, className=common_header_style()
    )
    publication_header = html.Div(
        publication_header_txt, className=common_header_style()
    )
    introduction_body = html.Div(
        introduction_body_md, className=common_body_style()
    )
    introduction_body2 = html.Div(
        introduction_body_md2, className=common_body_style()
    )

    current_stats = current_stats_html()

    reference_1 = html.Div(reference_1_md, className=common_body_style())
    reference_2 = html.Div(reference_2_md, className=common_body_style())

    why_use_header = html.Div(
        why_use_header_txt, className=common_header_style()
    )
    why_use_body = html.Div(why_use_body_md, className=common_body_style())
    why_use_body_container = html.Div(
        why_use_body,
        className="has-margin-right-40 has-margin-left-40 has-margin-top-5 has-margin-bottom-5",
    )
    funding_header = html.Div(
        funding_header_txt, className=common_header_style()
    )
    funding_body = html.Div(funding_md, className=common_body_style())

    elements = [
        logo,
        introduction_subheader,
        introduction_body,
        current_stats,
        introduction_body2,
        publication_header,
        reference_1,
        reference_2,
        why_use_header,
        why_use_body_container,
        funding_header,
        funding_body,
    ]
    container = common_info_box_html(elements)
    return container


def current_stats_html():
    """
    WARNING: Do not edit this unless you know EXACTLY what you're doing.
    This block systematically defines elements used by clientside callbacks.
    Editing this without knowing how it works will likely result in javascript
    headaches.

    Get the html block for the current stats.

    Returns:
        (dash_html_components.Div): The html block for the current stats, including
            counting up animations.

    """
    label_map = {
        "materials": "unique materials",
        "entities": "materials-related entities",
        "abstracts": "analyzed abstracts",
    }

    stats_columns = []

    # WARNING: don't mess with this section unless you know what you're doing!
    # The children of these divs needs to be ints for the javascript to
    # work correctly. Do NOT change the ids without changing the corresponding
    # javascript!
    # The ids currently are count-materials, count-abstracts, count-entities
    # The ids which it reads from are count-*-hidden-ref. The values it updates
    # are count-*. This is to prevent messing up quick reloads and double clicks
    for k, v in label_map.items():
        stat = html.Div(
            "{:,}".format(db_stats[k]),
            id=f"about-count-{k}-cs",
            className=f"is-size-4-desktop {common_stat_style()}",
        )
        stat_static_value = html.Div(
            "{:,}".format(db_stats[k]),
            id=f"about-count-{k}-hidden-ref-cs",
            className="is-hidden",
        )
        stat_descriptor = html.Div(
            f"{v}", className=f"is-size-6-desktop {common_stat_style()}"
        )
        stat_column = html.Div(
            [stat, stat_descriptor, stat_static_value],
            className="flex-column is-one-third",
        )
        stats_columns.append(stat_column)

    stats_columns = html.Div(
        stats_columns, className="columns is-centered is-desktop"
    )

    all_stats = html.Div(
        id="stats-container",
        children=stats_columns,
        className="container has-margin-top-30 has-margin-bottom-30",
    )

    return all_stats
