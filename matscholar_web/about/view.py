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
        "Persson ([Materials Project](materialsproject.org)) and " \
        "[Ceder](https://ceder.berkeley.edu) research groups. The aim of " \
        "Matscholar is to organize the world's materials knowlegde by " \
        "applying Natural Language Processing (NLP) to materials science " \
        "literature. To date, we have collected and analyzed " \

    introduction_body_txt2 = \
        "materials science abstracts and we continue to periodically update " \
        "the collection with the latest and greatest advancements in the " \
        "field. You can read more about our work in the following " \
        "publications:" \


    publication_header_txt = "Publications:"


    reference_1_txt = \
        "Weston, L., Tshitoyan, V., Dagdelen, J., Kononova, O., " \
        "Trewartha, A., Persson, K., Ceder, G., Jain, A. (2019) *Named " \
        "Entity Recognition and Normalization Applied to Large-Scale " \
        "Information Extraction from the Materials Science Literature.* " \
        "**J. Chem. Inf. Model.** 2019, 59, 9, 3692-3702" \
        "**[https://doi.org/10.1021/acs.jcim.9b00470]" \
        "(https://doi.org/10.1021/acs.jcim.9b00470)**" \

    reference_2_txt = \
        "Tshitoyan, V., Dagdelen, J., Weston, L., Dunn, A., Rong, Z., " \
        "Kononova, O., … Jain, A. (2019). *Unsupervised word embeddings " \
        "capture latent knowledge from materials science literature.* " \
        "**Nature**, 571(7763), 95–98. " \
        "**[https://doi.org/10.1038/s41586-019-1335-8]" \
        "(https://doi.org/10.1038/s41586-019-1335-8)**"


    current_abstracts  = html.Div(
        id="n-current-abstracts",
        className="is-size-2 has-margin-10 has-text-centered"
    )

    introduction_body_md = dcc.Markdown(introduction_body_txt)
    introduction_body_md2 = dcc.Markdown(introduction_body_txt2)
    reference_1_md = dcc.Markdown(reference_1_txt)
    reference_2_md = dcc.Markdown(reference_2_txt)

    introduction_header = html.Div(introduction_header_txt,
                                   className="is-size-5-desktop has-text-weight-bold has-margin-10")
    publication_header = html.Div(publication_header_txt,
                                   className="is-size-5-desktop has-text-weight-bold has-margin-10")
    introduction_body = html.Div(introduction_body_md,
                                 className="is-size-6-desktop has-margin-5")
    introduction_body2 = html.Div(introduction_body_md2,
                                 className="is-size-6-desktop has-margin-5")

    reference_1 = html.Div(reference_1_md, className="is-size-6-desktop has-margin-5")
    reference_2 = html.Div(reference_2_md, className="is-size-6-desktop has-margin-5")

    introduction_box = html.Div(
        [
            introduction_header,
            introduction_body,
            current_abstracts,
            introduction_body2,
            publication_header,
            reference_1,
            reference_2
        ],
        className="box has-padding-200"
    )

    introduction_column = html.Div(introduction_box, className="column is-half")
    introduction_columns = html.Div(introduction_column,
                                    className="columns is-centered")
    # introduction_container = html.Div(introduction_columns, className="container is-content")
    return introduction_columns
