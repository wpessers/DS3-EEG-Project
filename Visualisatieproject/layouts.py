import dash_html_components as html
import dash_core_components as dcc

from Visualisatieproject.callbacks import *
from Visualisatieproject.components import Header
from Visualisatieproject.jsondatareader import JsonDataReader


people = JsonDataReader.get_people()
stimuli = JsonDataReader.get_stimuli()

noPage = html.Div([
    # CC Header
    Header(),
    html.P(["404 Page not found"])
], className="page")

index_page = html.Div([
    Header(),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(id='hidden-person-div', style={'display':'none'}),
    html.Div(id='hidden-stimulus-div', style={'display':'none'}),
    html.Div(
        [
            html.H1("EEG Data Visualisation"),
            html.H2("Maak de data klaar voor gebruik:"),
            html.Button("Preprocess Data", id="button")
        ],
        style={'textAlign': "center", "marginBottom": 75}
    ),
    html.H2("Selecteer een persoon en stimulus om hun bijhorende EEG-Visualisatie te zien", style={"textAlign": "center"}),
    html.Div(
            [
                html.H4("Selecteer een persoon:"),
                dcc.Dropdown(id="person-dropdown", multi=False, options=people)
            ], style={"textAlign": "center", "width": "75%", "display": "inline-block"}),
    html.Div(
            [
                html.H4("Selecteer een stimulus:"),
                dcc.Dropdown(id="stimulus-dropdown", multi=False, options=stimuli)
            ], style={"textAlign": "center", "width": "75%", "display": "inline-block", "marginTop": 20})
], className="page", style={"textAlign": "center"})

graph1 = html.Div([
    Header(),
    html.Div(
        [
            html.H1("EEG Evolution over time")
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
            html.H1(id="h1_title", children="Correlation between EEG Data")
        ],
        style={"textAlign": "center"}
    ),
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Div([dcc.Graph(id="second-graph")]),
    html.Div(
        [
            html.H1(id="h2_title", children="Linear regression - Click a cell on the graph above!")
        ],
        style={"textAlign": "center"}
    ),
    html.Div([dcc.Graph(id="fourth-graph")]),
    html.Div(
        [dcc.RangeSlider(id="ms-range-heat", min=0, max=2000, step=7.8125, value=[0, 2000],
                         marks={"200": str(200), "400": str(400), "600": str(600),
                                "800": str(800), "1000": str(1000), "1200": str(1200),
                                "1400": str(1400), "1600": str(1600), "1800": str(1800)})],
        style={'display': 'none'}
    )
], className="page")

graph3 = html.Div([
    Header(),
    html.Div(
        [
            html.H1("EEG Data - Group Average")
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
