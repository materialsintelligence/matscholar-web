import dash_html_components as html
import dash_core_components as dcc

valid_filters = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]

def search_filter_box_html(label, filters=None, material=False):
    placeholders = {"material": "PbTe, graphite,...",
                    "property": "dielectric constant, melting point,...",
                    "application": "cathode, catalyst,...",
                    "descriptor": "thin film, nanoparticle,...",
                    "characterization": "photoluminescence, x-ray diffraction,...",
                    "synthesis":"sol - gel, firing,...",
                    "phase": "perovskite, wurtzite,..."}
    if not filters:
        value = None
    else:
        if not material:
            value = filters["ent"]
        else:
            materials = eval(filters["materials"])
            value = ",".join(materials) if len(materials) > 1 else materials[0]
    textbox = html.Div([html.Label('{}:'.format(label)),
        dcc.Input(
            id=label+"-filters",
            type="text",
            autofocus=True,
            placeholder=placeholders[label],
            value=value,
            style={"width": "100%"})
        ],
        style={'padding':5}
        )
    return textbox

def search_bar_html():
    return html.Div([
        html.Div(dcc.Input(
            id="search-input",
            type="text",
            autofocus=True,
            placeholder="Text search...",
            style={"width": "100%"}),
            style={"display": "table-cell", "width": "100%"}),
        html.Div(html.Button(
            "Search",
            className="button-search",
            id="search-btn"),
            style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"})],
            className="row", style={"display": "table", "marginTop": "10px"}
        )

def serve_layout(path):
    filters = None
    if path is not None and len(path) > len("/search"):
        path = path[len("/search")+1::]
        path = path.replace("%20", " ")
        ent_type, ent, materials = path.split("/")
        filters = {
            "ent_type": ent_type,
            "ent": ent,
            "materials": materials
        }

    search_bar = search_bar_html()
    filter_boxes = [html.Div(html.Label("Filters"))]
    if not filters:
        filter_boxes += [search_filter_box_html(label) for label in valid_filters]
    else:
        for label in valid_filters:
            if label == filters["ent_type"]:
                filter_boxes.append(search_filter_box_html(label, filters))
            elif label == "material":
                filter_boxes.append(search_filter_box_html(label, filters, material=True))
            else:
                filter_boxes.append(search_filter_box_html(label))

    filter_boxes_and_results = html.Div([html.Div(filter_boxes,style={'width': '25%', 'float': 'left', 'display': 'inline-block'}),html.Div(id='results',style={'width': '75%', 'float': 'right', 'display': 'inline-block'})])
    layout = html.Div([search_bar, filter_boxes_and_results])
    return layout

