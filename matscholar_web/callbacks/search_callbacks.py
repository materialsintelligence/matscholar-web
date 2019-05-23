import dash_html_components as html
import dash_materialsintelligence as dmi
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from matscholar import Rester
import matscholar
import pandas as pd

rester = Rester()
VALID_FILTERS = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]
max_results = 10000

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

def generate_nr_results(n, search=None, material=None, filters=None):
    if n == 0:
        return "No Results"
    elif n == max_results:
        return 'Showing {} of >{:,} results'.format(max_results, n)
    else:
        return 'Showing {} of {:,} results'.format(min(max_results, n), n)

def results_html(results,
                   columns=('title', 'authors', 'year', 'journal', 'abstract'),
                   max_rows=max_results):
    if results is not None:
        print("{} search results".format(len(results)))
        print(results)
        df = pd.DataFrame(results)
    else:
        pd.DataFrame()
    if not df.empty:
        format_authors = lambda author_list: ", ".join(author_list)
        df['authors'] = df['authors'].apply(format_authors)
        def word_limit(abstract):
            try:
                return abstract[:200]
            except IndexError:
                return abstract
        df['abstract'] = df['abstract'].apply(word_limit)
        hm = highlight_material
        return [html.Label(generate_nr_results(len(results)), id="number_results"), html.Table(
            # Header
            [html.Tr([html.Th(col) for col in columns])] +
            # Body
            [html.Tr([
                html.Td(html.A(str(df.iloc[i][col]),
                               href=df.iloc[i]["link"], target="_blank")) if col == "title"
                # else html.Td(
                #     hm(str(df.iloc[i][col]), df.iloc[i]['to_highlight'] if materials else search)) if col == "abstract"
                else html.Td(df.iloc[i][col]) for col in columns])
                for i in range(min(len(df), max_rows))],
            id="table-element")]
    return html.Div([html.Label(generate_nr_results(len(results)), id="number_results"),
            html.Table(id="table-element")])

def bind(app):
    @app.callback(
        Output('results', 'children'),
        [Input('search-btn','n_clicks')],
        [State('search-input','value')]+[State(f+'-filters', 'value') for f in VALID_FILTERS])
    def show_results(*args,**kwargs):
        if list(args)[0] is not None:
            text = str(args[1])
            filters = {f: [s.strip() for s in args[i+2].split(',')] for i,f in enumerate(VALID_FILTERS) if ((list(args)[i+2] is not None) and (args[i+2].split(',') != ['']))}
            results = rester.search_text_with_ents(text,filters)
            return results_html(results)
