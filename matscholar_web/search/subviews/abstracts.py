from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.constants import rester, valid_entity_filters, \
    entity_shortcode_map
from matscholar_web.search.util import parse_search_box, \
    results_container_class, no_results

MAX_N_ABSTRACTS = 100

def abstracts_results_html(search_text):
    entity_query = parse_search_box(search_text)
    results = rester.abstracts_search(
        entity_query,
        text=None,
        top_k=MAX_N_ABSTRACTS
    )

    if not results:
        return no_results()
    else:
        df = pd.DataFrame(results)

        if df.empty:
            return no_results()

        df['authors'] = df['authors'].apply(format_authors)

        n_formatted_results = min(len(df), MAX_N_ABSTRACTS)
        formatted_results = [None] * n_formatted_results

        if n_formatted_results > MAX_N_ABSTRACTS:
            label_txt = \
                f"Showing {n_formatted_results} of > {MAX_N_ABSTRACTS} " \
                f"results. For full results, use the "
            label_link = html.A(
                'Matscholar API.',
                href='https://github.com/materialsintelligence/matscholar'
            )
            label = html.Label([label_txt, label_link])
        else:
            label_txt = f"Showing all {n_formatted_results} results."
            label = html.Label(label_txt)

        for i in range(n_formatted_results):
            formatted_results[i] = format_result(df.iloc[i])
        paper_table = html.Table(formatted_results, className="table")

        return html.Div(
            [label, paper_table],
            className=results_container_class()
        )


def format_result(result):
    """
    Takes in one row of a dataframe and formats it for display in the
    search results table.
    Title of the paper is the first line
    Author 1, Author 2... - Title of Journal, Year - Publisher
    First 200 characters of abstract.
    Entities
    Args:
        result: Row of dataframe to be formatted for display.
    Returns:
        html.Div of formatted result
    """

    title_link = html.A(
        result['title'],
        href=result["link"],
        target="_blank",
    )

    title = html.Div(
        title_link,
        className="is-size-4 has-text-info"
    )

    # Format the 2nd line "authors - journal, year" with ellipses for overflow
    characters_remaining = 90  # max line length
    characters_remaining -= 5  # spaces, '-', and ','

    year = result['year']
    characters_remaining -= 4

    journal = result['journal']
    if len(journal) > 20:
        journal = journal if len(journal) < 33 else journal[0:30] + "..."
    characters_remaining -= len(journal)

    authors = result["authors"]
    full_author_list = authors.split(", ")
    num_authors = len(full_author_list)
    reduced_author_list = []
    while len(full_author_list) > 0:
        author = full_author_list.pop(0)
        if characters_remaining > len(author):
            reduced_author_list.append(author)
            characters_remaining -= len(author) + 2
    authors = ", ".join(reduced_author_list)
    if len(reduced_author_list) < num_authors:
        authors += "..."

    ajy = "{} - {}, {}".format(authors, journal, year)
    authors_journal_and_year = html.Div(
        ajy,
        className="is-size-5 has-text-success"
    )

    abstract_txt = result["abstract"]
    abstract = html.Div(abstract_txt, className="is-size-6")

    label_mapping = {
        "material": "MAT_summary",
        "application": "APL_summary",
        "property": "PRO_summary",
        "phase": "SPL_summary",
        "synthesis": "SMT_summary",
        "characterization": "CMT_summary",
        "descriptor": "DSC_summary"}

    entities = []
    for f in valid_entity_filters:
        for e in result[label_mapping[f]]:
            entity = html.Div(e, className="column is-narrow has-margin-5")
            entities.append(entity)

    entities_label = html.Div(
        "Extracted entities:",
        className="column is-narrow has-margin-5"
    )
    entities = html.Div([entities_label] + entities, className="columns has-max-width-350")
    entities_container = html.Div(entities, className="container")


    paper_div = html.Div(
        [title, authors_journal_and_year, abstract, entities_container]
    )

    table_cell = html.Td(paper_div)
    return html.Tr(table_cell)


def format_authors(author_list):
    if isinstance(author_list, (list, tuple)):
        return ", ".join([format_authors(author) for author in author_list])
    else:
        if ", " in author_list:
            author_list = author_list.split(", ")
            author_list.reverse()
            author_list = " ".join(author_list)
        elif "," in author_list:
            author_list = author_list.split(",")
            author_list.reverse()
            author_list = " ".join(author_list)
        return author_list


def highlight_material(body, material):
    highlighted_phrase = html.Mark(material)
    if len(material) > 0 and material in body:
        chopped = body.split(material)
        newtext = []
        for piece in chopped[:-1]:
            newtext.append(piece)
            newtext.append(highlighted_phrase)
        newtext.append(chopped[-1])
        return newtext
    return body
