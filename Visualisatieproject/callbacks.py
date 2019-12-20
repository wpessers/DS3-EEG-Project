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

df = JsonDataReader.read_to_df(electrode_list[0::2])
print(df)
cordf = df.corr()
reversedcordf = cordf.iloc[::-1]
print(reversedcordf)



@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-value', 'value'), Input('ms-range', 'value')])
def update_figure(selected, time):
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
                                yaxis={"title": "Spanning ( µV )"}, xaxis={"title": "Tijdstip"})}

@app.callback(Output('second-graph', 'figure'), [Input('second-graph', 'clickData')])
def on_heatmap_click(data):
    if data is not None:
        print(data)
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
            "mode": "lines",
            "type": "scatter",
            'x': lin_x,
            'y': lin_y
        }

        return {
            'data': [trace1, trace2],
            'layout': {
                "height": 700,
                "shapes": shapes
            }
        }


    return {
        'data': [dict(
                    x=reversedcordf.columns.tolist(),
                    y=reversedcordf.index.tolist(),
                    z=reversedcordf.values.tolist(),
                    zmin=-1,
                    zmax=1,
                    type="heatmap",
                    colorscale=[
                        [0, "rgb(111, 0, 0)"],
                        [0.1, "rgb(161, 41, 29)"],
                        [0.2, "rgb(208, 82, 59)"],
                        [0.3, "rgb(238, 133, 105)"],
                        #[0.4, "rgb(252, 188, 167)"],
                        [0.5, "rgb(255, 255, 130)"],
                        #[0.6, "rgb(101, 226, 151)"],
                        [0.7, "rgb(49, 183, 109)"],
                        [0.8, "rgb(2, 141, 70)"],
                        [0.9, "rgb(0, 99, 34)"],
                        [1.0, "rgb(0, 60, 0)"]]
        )],
        'layout': dict(height=700)
    }



