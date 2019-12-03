import dash_html_components as html
from Visualisatieproject.components import Header

noPage = html.Div([
    # CC Header
    Header(),
    html.P(["404 Page not found"])
    ], className="no-page")