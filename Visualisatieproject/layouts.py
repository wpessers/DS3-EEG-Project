import dash_html_components as html
import dash_core_components as dcc
from Visualisatieproject.callbacks import *
from Visualisatieproject.components import Header

noPage = html.Div([
    # CC Header
    Header(),
    html.P(["404 Page not found"])
    ], className="container")

graph1 = html.Div([
    Header(),
    html.Div(
        [
            html.H1("EEG Data From Barbara")
        ],
        style={'textAlign': "center"}
    ),
    html.Div(
        [
            dcc.Dropdown(id="selected-value", multi=True, value=['AF3'],
                         options=[{"label": "AF3", "value": "AF3"}])
        ],
        className="row", style={"display": "block", "width": "60%", "margin-left": "auto",
                                "margin-right": "auto"}
    ),
    html.Div(
        [dcc.Graph(id="my-graph")]
    ),
    html.Div(
        [dcc.RangeSlider(id="ms-range", min=0, max=256, step=1, value=[0, 2000],
                         marks={"16": str(16), "32": str(32), "48": str(48),
                                "64": str(64), "80": str(80), "96": str(96),
                                "112": str(112), "128": str(128), "144": str(144),
                                "160": str(160), "176": str(176), "192": str(192),
                                "208": str(208), "224": str(224), "240": str(240),
                                "256": str(256)})]
    )
], className="container")