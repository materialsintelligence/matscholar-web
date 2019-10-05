import os
import json

import dash_html_components as html
import dash_core_components as dcc

from matscholar_web.constants import rester


def serve_layout():
    introduction = get_introduction()

    return html.Div(
        [
            introduction
        ]
    )


def get_introduction():
    introduction_header_txt = \
        "Matscholar: A scholarly (AI) assistant for inorganic materials " \
        "science \n"
    introduction_body_txt = \
        "Matscholar is a research effort based out of the Lawrence Berkeley " \
        "National Lab and led by the " \
        "[HackingMaterials](https://hackingmaterials.lbl.gov), " \
        "[Persson](https://perssongroup.lbl.gov) " \
        "([Materials Project](https://materialsproject.org)) and " \
        "[Ceder](https://ceder.berkeley.edu) research groups. The aim of " \
        "Matscholar is to organize the world's materials knowlegde by " \
        "applying Natural Language Processing (NLP) to materials science " \
        "literature. To date, our database contains "

    introduction_body_txt2 = \
        "We are continuing to periodically update " \
        "our collections with the latest and greatest advancements in the " \
        "field of materials science. You can read more about our work in the " \
        "following publications:"

    publication_header_txt = "Publications:"

    reference_1_txt = \
        "Weston, L., Tshitoyan, V., Dagdelen, J., Kononova, O., " \
        "Trewartha, A., Persson, K., Ceder, G., Jain, A. (2019) *Named " \
        "Entity Recognition and Normalization Applied to Large-Scale " \
        "Information Extraction from the Materials Science Literature.* " \
        "**J. Chem. Inf. Model.** 2019, 59, 9, 3692-3702 " \
        "**[https://doi.org/10.1021/acs.jcim.9b00470]" \
        "(https://doi.org/10.1021/acs.jcim.9b00470)**"

    reference_2_txt = \
        "Tshitoyan, V., Dagdelen, J., Weston, L., Dunn, A., Rong, Z., " \
        "Kononova, O., Persson, K., Ceder, G., Jain, A. (2019). " \
        "*Unsupervised word embeddings " \
        "capture latent knowledge from materials science literature.* " \
        "**Nature**, 571(7763), 95–98. " \
        "**[https://doi.org/10.1038/s41586-019-1335-8]" \
        "(https://doi.org/10.1038/s41586-019-1335-8)**"

    why_use_header_txt = "Why use Matscholar?"
    why_use_body_txt = \
        "1. **It's free**: Matscholar is available freely anywhere in the " \
        "world. We release our finished NLP codes feely on " \
        "[Github](https://github.com/materialsintelligence) " \
        "(including the source code for this website). We also provide an " \
        "python API for querying our databae which you can find on our " \
        "[Github](https://github.com/materialsintelligence/matscholar).\n" \
        "2. **It goes beyond what Google Scholar " \
        "can do**: Matscholar goes beyond full text searches and uses " \
        "specifically-trained *materials-related* entities to search " \
        "millions of abstracts.\n 3. **It's (relatively) fast**: And getting " \
        "faster! We are actively working on our infrastructure to make " \
        "Matscholar faster, more accurate, and more informative."

    funding_header_txt = "Our funding sources"
    funding_body_txt = \
        "Matscholar is supported by Toyota Research Institute through the " \
        "Accelerated Materials Design and Discovery program. Abstract data " \
        "was downloaded from the ScienceDirect API between October 2017 and " \
        "September 2018, and the Scopus API in July 2019 via " \
        "http://api.elsevier.com and http://www.scopus.com. Abstract " \
        "data was also downloaded from the SpringerNature API and Royal " \
        "Society of Chemistry sources."

    introduction_body_md = dcc.Markdown(introduction_body_txt)
    introduction_body_md2 = dcc.Markdown(introduction_body_txt2)
    why_use_body_md = dcc.Markdown(why_use_body_txt)
    reference_1_md = dcc.Markdown(reference_1_txt)
    reference_2_md = dcc.Markdown(reference_2_txt)
    funding_md = dcc.Markdown(funding_body_txt)

    body_style = "is-size-6-desktop has-margin-5"
    header_style = "is-size-5-desktop has-text-weight-bold has-margin-10"

    introduction_header = html.Div(introduction_header_txt,
                                   className=header_style)
    publication_header = html.Div(publication_header_txt,
                                  className=header_style)
    introduction_body = html.Div(introduction_body_md,
                                 className=body_style)
    introduction_body2 = html.Div(introduction_body_md2,
                                  className=body_style)

    current_stats = get_current_stats_html()

    reference_1 = html.Div(reference_1_md, className=body_style)
    reference_2 = html.Div(reference_2_md, className=body_style)

    why_use_header = html.Div(why_use_header_txt, className=header_style)
    why_use_body = html.Div(why_use_body_md, className=body_style)
    why_use_body_container = html.Div(why_use_body,
                                      className="has-margin-right-40 has-margin-left-40 has-margin-top-5 has-margin-bottom-5")
    funding_header = html.Div(funding_header_txt, className=header_style)
    funding_body = html.Div(funding_md, className=body_style)

    introduction_box = html.Div(
        [
            introduction_header,
            introduction_body,
            current_stats,
            introduction_body2,
            publication_header,
            reference_1,
            reference_2,
            why_use_header,
            why_use_body_container,
            funding_header,
            funding_body
        ],
        className="box has-padding-200"
    )

    introduction_column = html.Div(introduction_box, className="column is-half")
    introduction_columns = html.Div(introduction_column,
                                    className="columns is-centered")
    # introduction_container = html.Div(introduction_columns, className="container is-content")
    return introduction_columns


def get_journal_breakdown():
    rester.get_journals()


def get_current_stats_html():
    thisdir = os.path.abspath(os.path.dirname(__file__))
    target = os.path.abspath(
        os.path.join(
            thisdir,
            "../assets/data/db_statistics.json"
        )
    )
    with open(target, "r") as f:
        stats = json.load(f)

    label_map = {
        "materials": "unique materials",
        "entities": "materials-related entities",
        "abstracts": "analyzed abstracts"
    }

    stats_columns = []

    # Warning: don't mess with this section unless you know what you're doing!
    # The children of these divs needs to be ints for the javascript to
    # work correctly. Do NOT change the ids without changing the corresponding
    # javascript!
    # The ids currently are count-materials, count-abstracts, count-entities
    common_styling = "has-margin-5 has-text-centered has-text-weight-bold"
    for k, v in label_map.items():
        stat = html.Div(
            stats[k],
            id=f"count-{k}",
            className=f"is-size-3 {common_styling}"
        )
        stat_descriptor = html.Div(f"{v}", className=f"is-size-5 {common_styling}")
        stat_column = html.Div([stat, stat_descriptor], className="column is-one-third")
        stats_columns.append(stat_column)

    stats_columns = html.Div(stats_columns, className="columns is-centered")

    all_stats = html.Div(stats_columns, className="container has-margin-top-30 has-margin-bottom-30")
    return all_stats
