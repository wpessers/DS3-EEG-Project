import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go

from Visualisatieproject.app import app
from dash.dependencies import Input, Output
from Visualisatieproject.jsondatareader import JsonDataReader
from Visualisatieproject.preprocessing.preprocessing import Preprocessing

electrode_list = ["Anterior Frontal", ["AF3", "AF4"],
                  "Frontal", ["F7", "F3", "F4", "F8"],
                  "Central", ["FC5", "FC6"],
                  "Temporal", ["T7", "T8"],
                  "Posterior", ["P7", "P8"],
                  "Occipital", ["O1", "O2"],
                  "Linguistic", ["F7", "T7"]]

person = "Barbara"
stimulus = "beloof"

@app.callback(
    Output('second-graph', 'figure'),
    [Input('ms-range-heat', 'value')])
def update_second_graph(time):
    print(time)
    df = JsonDataReader.read_to_df(electrode_list[0::2], person, stimulus)
    cordf = df.corr()
    reversedcordf = cordf.iloc[::-1]

    data = [dict(
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
    )]

    layout = dict(height=700)

    return {
        "data": data,
        "layout": layout
    }


@app.callback(
    Output('hidden-person-div', 'children'),
    [Input('person-dropdown', 'value')])
def update_person(value):
    global person
    if value is None:
        return "Nothing changed"
    else:
        print("Selected Person: %s" % value)
        person = value


@app.callback(
    Output('hidden-stimulus-div', 'children'),
    [Input('stimulus-dropdown', 'value')])
def update_stimulus(value):
    global stimulus
    if value is None:
        return "Nothing changed"
    else:
        print("Selected Stimulus: %s" % value)
        stimulus = value


@app.callback(
    Output('my-graph', 'figure'),
    [Input('ms-range', 'value')])
def update_figure(time):
    selected = ['AF3', 'AF4', 'F7', 'F3', 'F4', 'F8', 'FC5', 'FC6', 'T7', 'T8', 'P7', 'P8', 'O1', 'O2']
    text = {
        "AF3": "AF3",
        "AF4": "AF4",
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

    df = JsonDataReader.read_to_df(electrode_list[0::2], person, stimulus)

    dff = df[(df.index >= (time[0] / 7.8125)) & (df.index <= (time[1] / 7.8125))]
    trace = []
    for type in selected:
        trace.append(go.Scatter(x=(dff.index * 7.8125), y=dff[type], name=text[type], mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": trace,
            "layout": go.Layout(title="Evolutie Spanning", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"showgrid": False, "title": "Spanning ( µV )"},
                                xaxis={"showgrid": False, "title": "Tijdstip"})}


@app.callback(
    [Output('fourth-graph', 'figure'),
     Output('h2_title', 'children')],
    [Input('second-graph', 'clickData')])
def on_heatmap_click(data):
    if data is not None:
        df = JsonDataReader.read_to_df(electrode_list[0::2], person, stimulus)

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
               }, "Lineair regression between {} and {}".format(x, y)


@app.callback(
    Output('third-graph', 'figure'),
    [Input('ms-range-third-graph', 'value')])
def update_third_graph(time):
    selected = ['Anterior Frontal', 'Frontal', 'Central', 'Temporal', 'Posterior', 'Occipital', 'Linguistic']
    text = {
        "Anterior Frontal": "Anterior Frontal",
        "Frontal": "Frontal",
        "Central": "Central",
        "Temporal": "Temporal",
        "Posterior": "Posterior",
        "Occipital": "Occipital",
        "Linguistic": "Linguistic"
    }

    df = JsonDataReader.read_to_df(electrode_list[0::2], person, stimulus)
    average_df = pd.DataFrame()
    average_df['Linguistic'] = df[['F7', 'T7']].mean(axis=1)
    average_df['Anterior Frontal'] = df[['AF3', 'AF4']].mean(axis=1)
    average_df['Frontal'] = df[['F7', 'F3', 'F4', 'F8']].mean(axis=1)
    average_df['Central'] = df[['FC5', 'FC6']].mean(axis=1)
    average_df['Temporal'] = df[['T7', 'T8']].mean(axis=1)
    average_df['Posterior'] = df[['P7', 'P8']].mean(axis=1)
    average_df['Occipital'] = df[['O1', 'O2']].mean(axis=1)

    dff = average_df[(average_df.index >= (time[0] / 7.8125)) & (average_df.index <= (time[1] / 7.8125))]
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
                                yaxis={"showgrid": False, "title": "Spanning ( µV )"},
                                xaxis={"showgrid": False, "title": "Tijdstip"})}


@app.callback(
    Output('hidden-div', 'children'),
    [Input('button', 'n_clicks')])
def run_preprocessing(n_clicks):
    print("Preprocessing")
    data_dir = "../res/"

    electrode_list = ["Anterior Frontal", ["AF3", "AF4"],
                      "Frontal", ["F7", "F3", "F4", "F8"],
                      "Central", ["FC5", "FC6"],
                      "Temporal", ["T7", "T8"],
                      "Posterior", ["P7", "P8"],
                      "Occipital", ["O1", "O2"],
                      "Linguistic", ["F7", "T7"]]

    p = Preprocessing(data_dir, electrode_list)
    p.preprocess()

    return "Preprocessing done"
