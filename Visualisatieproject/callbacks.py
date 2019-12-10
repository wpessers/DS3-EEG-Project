import dash
import os
import plotly.graph_objs as go
from Visualisatieproject.app import app
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
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
cordf = df.corr()
reversedcordf = cordf.iloc[::-1]
print(cordf)
print(reversedcordf)

@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-value', 'value'), Input('ms-range', 'value')])
def update_figure(selected, time):
    text = {
        "AF3": "AF3",
    }
    print(selected)

    dff = df[(df.index >= time[0]) & (df.index <= time[1])]
    trace = []
    for type in selected:
        trace.append(go.Scatter(x=dff.index, y=dff[type], name=text[type], mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": trace,
            "layout": go.Layout(title="Evolutie Spanning", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"title": "Spanning ( µV )"}, xaxis={"title": "Tijdstip"})}

