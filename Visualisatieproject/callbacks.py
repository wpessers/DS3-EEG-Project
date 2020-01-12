import dash
import os
import json
import plotly.graph_objs as go
from Visualisatieproject.app import app
import seaborn as sns
import matplotlib.pyplot as plt
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

df = JsonDataReader.read_to_df(electrode_list[0::2], "Barbara", "beloof")
print(df)

cordf = df.corr()
reversedcordf = cordf.iloc[::-1]
print(reversedcordf)

average_df = pd.DataFrame()
average_df['Linguistic'] = df[['F7', 'T7']].mean(axis=1)
average_df['Anterior Frontal'] = df[['AF3', 'AF4']].mean(axis=1)
average_df['Frontal'] = df[['F7', 'F3', 'F4', 'F8']].mean(axis=1)
average_df['Central'] = df[['FC5', 'FC6']].mean(axis=1)
average_df['Temporal'] = df[['T7', 'T8']].mean(axis=1)
average_df['Posterior'] = df[['P7', 'P8']].mean(axis=1)
average_df['Occipital'] = df[['O1', 'O2']].mean(axis=1)
print(average_df)


@app.callback(
    Output('my-graph', 'figure'),
    [Input('ms-range', 'value')])
def update_figure(time):
    selected = ['AF3', 'AF4', 'F7', 'F3', 'F4', 'F8', 'FC5', 'FC6', 'T7', 'T8', 'P7', 'P8', 'O1', 'O2']
    text = {
        "AF3": "AF3",
        "AF4":"AF4",
        "F7": "F7",
        "F3": "F3",
        "F4": "F4",
        "F8": "F8",
        "FC5": "FC5",
        "FC6": "FC6",
        "T7": "T7",
        "T8": "T8",
        "P7": "P7",
        "P8": "P8",
        "O1": "O1",
        "O2": "O2"
    }

    dff = df[(df.index >= (time[0]/7.8125)) & (df.index <= (time[1]/7.8125))]
    trace = []
    for type in selected:
        trace.append(go.Scatter(x=(dff.index*7.8125), y=dff[type], name=text[type], mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": trace,
            "layout": go.Layout(title="Evolutie Spanning", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"showgrid":False, "title": "Spanning ( µV )"},
                                xaxis={"showgrid": False, "title": "Tijdstip"})}

@app.callback(
    [Output('second-graph', 'figure'),
     Output('h1_title', 'children')],
    [Input('second-graph', 'clickData')])
def on_heatmap_click(data):
    if data is not None:
        x = data['points'][0]['x']
        y = data['points'][0]['y']
        plt.clf()
        lin = sns.regplot(x, y, df)
        lin_x = lin.get_lines()[0].get_xdata()  # x-coordinate of points along the regression line
        lin_y = lin.get_lines()[0].get_ydata()  # y-coordinate
        lin_p = lin.get_children()[1].get_paths()

        p_codes = {1: 'M', 2: 'L', 79: 'Z'}  # dict to get the Plotly codes for commands to define the svg path
        path = ''
        for s in lin_p[0].iter_segments():
            c = p_codes[s[1]]
            xx, yy = s[0]
            path += c + str('{:.5f}'.format(xx)) + ' ' + str('{:.5f}'.format(yy))

        shapes = [dict(type='path',
                       path=path,
                       line=dict(width=0.1, color='rgba(68, 122, 219, 0.25)'),
                       fillcolor='rgba(68, 122, 219, 0.25)')]

        trace1 = {
            'x': df[x],
            'y': df[y],
            'name': 'data points',
            'mode': 'markers',
            'marker': {
                'size': 5
            },
            'type': 'scatter'
        }

        trace2 = {
            "line": {
                "color": "rgb(68, 122, 219)",
                "width": 2
            },
            'name': 'regression line',
            "mode": "lines",
            "type": "scatter",
            'x': lin_x,
            'y': lin_y
        }

        return {
            'data': [trace1, trace2],
            'layout': {
                "height": 700,
                "shapes": shapes,
                'xaxis': {
                    'title': x
                },
                'yaxis': {
                    'title': y
                }
            }
        }, "Lineair regression between {} and {} From Barbara".format(x, y)

@app.callback(
    Output('third-graph', 'figure'),
    [Input('ms-range-third-graph', 'value')])
def update_third_graph(time):
    selected = ['Anterior Frontal', 'Frontal', 'Central', 'Temporal', 'Posterior', 'Occipital', 'Linguistic']
    text = {
        "Anterior Frontal": "Anterior Frontal",
        "Frontal":"Frontal",
        "Central": "Central",
        "Temporal": "Temporal",
        "Posterior": "Posterior",
        "Occipital": "Occipital",
        "Linguistic": "Linguistic"
    }

    dff = average_df[(average_df.index >= (time[0]/7.8125)) & (average_df.index <= (time[1]/7.8125))]
    trace = []
    for type in selected:
        if type == "Linguistic":
            trace.append(go.Scatter(x=(dff.index * 7.8125), y=dff[type], name=text[type], mode='lines',
                                    marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}, "color": "blue"}, ))
        else:
            trace.append(go.Scatter(x=(dff.index * 7.8125), y=dff[type], name=text[type], mode='lines',
                                    marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}, "color": "lightgrey"}, ))

    return {"data": trace,
            "layout": go.Layout(title="Evolutie Spanning", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"showgrid":False, "title": "Spanning ( µV )"},
                                xaxis={"showgrid":False, "title": "Tijdstip"})}