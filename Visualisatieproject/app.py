import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

from Visualisatieproject.jsondatareader import JsonDataReader

electrode_list = ["Anterior Frontal", ["AF3", "AF4"],
                  "Frontal", ["F7", "F3", "F4", "F8"],
                  "Central", ["FC5", "FC6"],
                  "Temporal", ["T7", "T8"],
                  "Posterior", ["P7", "P8"],
                  "Occipital", ["O1", "O2"],
                  "Linguistic", ["F7", "T7"]]

df = JsonDataReader.read_to_df(electrode_list[0::2])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
        [
            html.H1("EEG Data From Barbara")
        ],
        style={'textAlign': "center"}
    ),
    html.Div(
        [
            dcc.Dropdown(id="selected-value", multi=True, value="AF3",
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


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-value', 'value'), Input('ms-range', 'value')])
def update_figure(selected, time):
    text = {
        "AF3": "AF3",
    }
    dff = df[(df.index >= time[0]) & (df.index <= time[1])]
    trace = []
    for type in selected:
        trace.append(go.Scatter(x=dff.index, y=dff[type], name=text[type], mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": trace,
            "layout": go.Layout(title="Evolutie Spanning", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"title": "Spanning ( µV )"}, xaxis={"title": "Tijdstip"})}


if __name__ == '__main__':
    app.run_server(debug=True)
