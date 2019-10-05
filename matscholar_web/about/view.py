import dash_html_components as html
import dash_core_components as dcc

from matscholar_web.constants import db_stats
from matscholar_web.common import divider_html

common_stat_style = "has-margin-right-10 has-margin-left-10 has-text-centered has-text-weight-bold"
common_body_style = "is-size-6-desktop has-margin-5"
common_header_style = "is-size-5-desktop has-text-weight-bold has-margin-5"
common_title_style = "is-size-2-desktop has-text-weight-bold has-margin-5"


def serve_layout():
    introduction = get_introduction()
    journals = get_journals_html()

    return html.Div(
        [
            dcc.Input(id="some_input"),
            html.Div(id='output-clientside'),
            introduction,
            journals,
        ]
    )


def get_introduction():
    introduction_header_txt = "Matscholar"
    introduction_subheader_txt = \
        "A scholarly (AI) assistant for materials science \n"
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

    introduction_header = html.Div(introduction_header_txt,
                                   className=common_title_style)
    introduction_subheader = html.Div(introduction_subheader_txt,
                                      className=common_header_style)
    publication_header = html.Div(publication_header_txt,
                                  className=common_header_style)
    introduction_body = html.Div(introduction_body_md,
                                 className=common_body_style)
    introduction_body2 = html.Div(introduction_body_md2,
                                  className=common_body_style)

    current_stats = get_current_stats_html()

    reference_1 = html.Div(reference_1_md, className=common_body_style)
    reference_2 = html.Div(reference_2_md, className=common_body_style)

    why_use_header = html.Div(why_use_header_txt, className=common_header_style)
    why_use_body = html.Div(why_use_body_md, className=common_body_style)
    why_use_body_container = html.Div(why_use_body,
                                      className="has-margin-right-40 has-margin-left-40 has-margin-top-5 has-margin-bottom-5")
    funding_header = html.Div(funding_header_txt, className=common_header_style)
    funding_body = html.Div(funding_md, className=common_body_style)

    elements = [
        introduction_header,
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
        funding_body
    ]
    container = get_common_box(elements)
    return container


def get_current_stats_html():
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
    for k, v in label_map.items():
        stat = html.Div(
            "{:,}".format(db_stats[k]),
            id=f"count-{k}",
            className=f"is-size-4-desktop {common_stat_style}"
        )
        stat_descriptor = html.Div(f"{v}",
                                   className=f"is-size-6-desktop {common_stat_style}")
        stat_column = html.Div([stat, stat_descriptor],
                               className="flex-column is-one-third")
        stats_columns.append(stat_column)

    stats_columns = html.Div(stats_columns,
                             className="columns is-centered is-desktop")

    all_stats = html.Div(id="stats-container", children=stats_columns,
                         className="container has-margin-top-30 has-margin-bottom-30")

    return all_stats


def get_journals_html():
    journals = db_stats["journals"]
    n_journals = len(journals)

    journal_info_header_txt = "Journals in Matscholar"
    journal_info_subheader_txt = f"Search among {n_journals} scientific journals"
    journals_info_body_txt = \
        f"Matscholar at present contains processed abstracts from " \
        f"{n_journals} peer-reviewed scientific journals from multiple " \
        f"scientific domains, including inorganic materials, polymers, " \
        f"biomaterials, and more."

    journal_info_header = html.Div(journal_info_header_txt,
                                   className=common_title_style)
    journal_info_subheader = html.Div(journal_info_subheader_txt,
                                      className=common_header_style)
    journal_info_body = html.Div(journals_info_body_txt,
                                 className=common_body_style)

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
                              className=common_header_style)

    header_number = html.Th("Number")
    header_name = html.Th("Journal Name")
    header = html.Tr([header_number, header_name])

    rows = [None] * n_journals
    for i, j in enumerate(journals):
        jname = html.Td(j, className="has-text-weight-bold")
        jnumber = html.Td(i)
        rows[i] = html.Tr([jnumber, jname], className="is-size-7")

    jtable = html.Table(
        [header] + rows,
        className="table is-bordered is-hoverable is-narrow is-striped"
    )

    hr_dropdown = divider_html()
    hr_jtable = divider_html()
    jtable_label = html.Div(
        "Browse a full journal list",
        className=common_header_style + "has-margin-top-30"
    )

    elements = [
        journal_info_header,
        journal_info_subheader,
        journal_info_body,
        hr_dropdown,
        dropdown_label,
        dropdown,
        hr_jtable,
        jtable_label,
        jtable
    ]

    container = get_common_box(elements, id="journals")
    return container


def get_common_box(elements, id=None):
    box = html.Div(elements, className="box")
    column = html.Div(box, className="column is-half")
    columns = html.Div(column, className="columns is-centered")
    container = html.Div(columns, className="container", id=id)
    return container
