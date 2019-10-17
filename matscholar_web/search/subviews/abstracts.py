from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.constants import rester, valid_entity_filters, \
    entity_shortcode_map, entity_color_map_bulma
from matscholar_web.search.util import parse_search_box, \
    results_container_class, no_results_html, get_results_label_html

MAX_N_ABSTRACTS_RETRIEVED = 200  # the number of abstracts retrieved via api
MAX_N_ABSTRACTS = 20  # the number of abstracts actually shown
MAX_ENTITIES_PER_ROW = 3

def abstracts_results_html(search_text):
    entity_query, raw_text = parse_search_box(search_text)
    results = rester.abstracts_search(
        entity_query,
        text=raw_text,
        top_k=MAX_N_ABSTRACTS_RETRIEVED
    )

    if not results:
        return no_results_html()
    else:
        df = pd.DataFrame(results)
        n_raw_results = df.shape[0]

        if df.empty:
            return no_results_html()

        df['authors'] = df['authors'].apply(format_authors)

        n_formatted_results = min(len(df), MAX_N_ABSTRACTS)
        formatted_results = [None] * n_formatted_results

        if n_raw_results >= MAX_N_ABSTRACTS:
            label_txt = \
                f"Showing {n_formatted_results} of many results. For full " \
                f"results, use the "
            label_link = html.A(
                'Matscholar API.',
                href='https://github.com/materialsintelligence/matscholar'
            )
            label = html.Label([label_txt, label_link])
        else:
            label_txt = f"Showing all {n_raw_results} results."
            label = html.Label(label_txt)

        entities_keys = []
        for e in valid_entity_filters:
            color = entity_color_map_bulma[e]
            entity_key = html.Div(e, className=f"button is-{color} is-active")
            entity_key_container = html.Div(entity_key, className="flex-column is-narrow has-margin-5")
            entities_keys.append(entity_key_container)
        entity_key_container = html.Div(entities_keys, className="columns is-multiline has-margin-5")


        for i in range(n_formatted_results):
            formatted_results[i] = format_result(df.iloc[i])
        paper_table = html.Table(formatted_results, className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped")

        big_results_label = get_results_label_html("abstracts")
        return html.Div(
            [big_results_label, label, entity_key_container, paper_table],
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
        className="is-size-4 has-text-link has-text-weight-bold"
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
        className="is-size-5 has-text-info"
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
            color = entity_color_map_bulma[f]
            entity = html.Div(
                e,
                className=f"button is-{color} is-active"
            )
            entity_container = html.Div(entity, className="flex-column is-narrow has-margin-5")
            entities.append(entity_container)

    entities = html.Div(entities, className="columns is-multiline has-margin-5")

    entities_label = html.Div(
        "Extracted entities:",
        className="has-margin-5 has-text-weight-bold"
    )
    paper_div = html.Div(
        [title, authors_journal_and_year, abstract, entities_label, entities],
        className="has-margin-10"
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