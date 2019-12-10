import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from Visualisatieproject.callbacks import *
from Visualisatieproject.components import Header

noPage = html.Div([
    # CC Header
    Header(),
    html.P(["404 Page not found"])
], className="page")

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
            dcc.Dropdown(id="selected-value", multi=True,
                         value=["AF3", "AF4", "F7", "F3", "F4", "F8", "FC5", "FC6", "T7", "T8", "P7", "P8", "O1", "O2"],
                         options=[{"label": "AF3", "value": "AF3"},
                                  {"label": "AF4", "value": "AF4"},
                                  {"label": "F7", "value": "F7"},
                                  {"label": "F3", "value": "F3"},
                                  {"label": "F4", "value": "AF4"},
                                  {"label": "F8", "value": "AF8"},
                                  {"label": "FC5", "value": "FC5"},
                                  {"label": "FC6", "value": "FC6"},
                                  {"label": "T7", "value": "T7"},
                                  {"label": "T8", "value": "T8"},
                                  {"label": "P7", "value": "P7"},
                                  {"label": "P8", "value": "P8"},
                                  {"label": "O1", "value": "O1"},
                                  {"label": "O2", "value": "O2"}])
        ],
        className="row", style={"display": "block", "width": "100%", "margin-left": "auto",
                                "margin-right": "auto"}
    ),
    html.Div(
        [dcc.Graph(id="my-graph")]
    ),
    html.Div(
        [dcc.RangeSlider(id="ms-range", min=0, max=256, step=1, value=[0, 256],
                         marks={"16": str(16), "32": str(32), "48": str(48),
                                "64": str(64), "80": str(80), "96": str(96),
                                "112": str(112), "128": str(128), "144": str(144),
                                "160": str(160), "176": str(176), "192": str(192),
                                "208": str(208), "224": str(224), "240": str(240),
                                "256": str(256)})]
    )
], className="page")

graph2 = html.Div([
    Header(),
    html.Div(
        [
            html.H1("Correlation between EEG Data From Barbara")
        ],
        style={"textAlign": "center"}
    ),
    html.Div(
        [
            dcc.Graph(id="second-graph",
                      figure={
                          "data": [{
                              "x": reversedcordf.columns.tolist(),
                              "y": reversedcordf.index.tolist(),
                              "z": reversedcordf.values.tolist(),
                              "type": "heatmap"
                              # todo: colorscale
                          }],
                          "layout": {
                              "height": 700
                          }

                      })
        ]
    )
], className="page")
