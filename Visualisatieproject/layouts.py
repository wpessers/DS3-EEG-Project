import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import colorlover as cl
from Visualisatieproject.callbacks import *
from Visualisatieproject.components import Header

noPage = html.Div([
    # CC Header
    Header(),
    html.P(["404 Page not found"])
], className="page")

index_page = html.Div([
    Header(),
    html.Div(
        [
            html.H1("EEG Data Visualisation"),
            html.Button("Preprocess Data", id="button"),
            dcc.Dropdown(id="selected-value", multi=False, value=[])
        ],
        style={'textAlign': "center"}
    )
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
        [dcc.Graph(id="my-graph")]
    ),
    html.Div(
        [dcc.RangeSlider(id="ms-range", min=0, max=2000, step=7.8125, value=[0, 2000],
                         marks={"200": str(200), "400": str(400), "600": str(600),
                                "800": str(800), "1000": str(1000), "1200": str(1200),
                                "1400": str(1400), "1600": str(1600), "1800": str(1800)})]
    )
], className="page")

graph2 = html.Div([
    Header(),
    html.Div(
        [
            html.H1(id="h1_title", children="Correlation between EEG Data From Barbara")
        ],
        style={"textAlign": "center"}
    ),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(
        [
            dcc.Graph(
                id="second-graph",
                figure=dict(
                    data=[
                        dict(
                            x=reversedcordf.columns.tolist(),
                            y=reversedcordf.index.tolist(),
                            z=reversedcordf.values.tolist(),
                            zmin=-1,
                            zmax=1,
                            type="heatmap",
                            colorscale=[
                                [0, "rgb(140, 0, 10)"],
                                [0.1, "rgb(160, 40, 30)"],
                                [0.2, "rgb(210, 80, 60)"],
                                [0.3, "rgb(238, 132, 106"],
                                [0.4, "rgb(252, 188, 168)"],
                                [0.5, "rgb(250, 250, 250)"],
                                [0.6, "rgb(100, 226, 150"],
                                [0.7, "rgb(50, 182, 110)"],
                                [0.8, "rgb(0, 140, 70)"],
                                [0.9, "rgb(0, 100, 34)"],
                                [1.0, "rgb(0, 60, 0)"]
                            ]
                        )
                    ],
                    layout=dict(
                        height=700
                    )
                )
            )
        ]
    )
], className="page")

graph3 = html.Div([
    Header(),
    html.Div(
        [
            html.H1("EEG Data From Barbara - Group Average")
        ],
        style={'textAlign': "center"}
    ),
    html.Div(
        [dcc.Graph(id="third-graph")]
    ),
    html.Div(
        [dcc.RangeSlider(id="ms-range-third-graph", min=0, max=2000, step=7.8125, value=[0, 2000],
                         marks={"200": str(200), "400": str(400), "600": str(600),
                                "800": str(800), "1000": str(1000), "1200": str(1200),
                                "1400": str(1400), "1600": str(1600), "1800": str(1800)})]
    )
], className="page")
