import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        get_header(),
        html.Br([]),
        get_menu()
    ])


def get_header():
    header = html.Div([
        html.Div([
            html.H5(
                'Data Science 3 EEG Project')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

        dcc.Link('Index   ', href='/index/', className="tab first"),

        dcc.Link('Grafiek 1   ', href='/graph1/', className="tab"),

        dcc.Link('Grafiek 2   ', href='/graph2/', className="tab"),

        dcc.Link('Grafiek 3   ', href='/graph3/', className="tab"),

    ], className="row ")
    return menu