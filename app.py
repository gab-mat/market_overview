import dash
import os
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Sample excel
sample_data = {
    "Commodity": ["Gold", "Silver", "Oil", "Natural Gas"] * 10,
    "Date": pd.date_range("2023-01-01", periods=40, freq="D"),
    "Price": [
        1850 + i * 5 for i in range(10)
    ] + [24 + i * 0.5 for i in range(10)] + [75 + i for i in range(10)] + [3.5 + i * 0.1 for i in range(10)],
}

# load data from the sample excel
#
#
#


commodity_df = pd.DataFrame(sample_data)




# External stylesheets
external_stylesheets = [
    {"href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap", "rel": "stylesheet"},
    dbc.themes.BOOTSTRAP,
]

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = "Commodity Dashboard"

# Sidebar layout
sidebar = html.Div(
    [
        html.H2("My App", className="display-4", style={"textAlign": "center", "font-variant": "small-caps"}),
        html.Hr(),
        html.H3("Commodities Analysis", className="display-8", style={"textAlign": "center"}),
        dbc.Nav(
            [
                dbc.NavLink("Page 1", href="/", active="exact"),
                dbc.NavLink("Page 2", href="/page2_url", active="exact"),
            ],
            vertical=True,
            pills=True,
            style={"font-size": 18, "textAlign": "center"},
        ),
    ],
    className="sidebar_style",
)

# Content layout
CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "1.8rem",
    "padding": "1.8rem 0.9rem",
}

# Page 1 content with 4 graphs in a 2x2 layout
page1_content = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph1", style={"height": "360px"}), width=6),
                dbc.Col(dcc.Graph(id="graph2", style={"height": "360px"}), width=6),
            ],
            className="mb-3",  # Adjusted margin-bottom for spacing
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph3", style={"height": "360px"}), width=6),
                dbc.Col(dcc.Graph(id="graph4", style={"height": "360px"}), width=6),
            ]
        ),
    ],
    style={"padding": "1.8rem"},
)

# Page 2 content (placeholder)
page2_content = html.Div("Page 2 content")

# Main layout
content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Callbacks
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def render_page_content(pathname):
    if pathname == "/":
        return page1_content
    elif pathname == "/page2_url":
        return page2_content
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised."),
        ]
    )


@app.callback(
    [Output("graph1", "figure"), Output("graph2", "figure"), Output("graph3", "figure"), Output("graph4", "figure")],
    Input("url", "pathname"),
)
def update_graphs(pathname):
    if pathname == "/":
        fig1 = px.line(
            commodity_df[commodity_df["Commodity"] == "Gold"], x="Date", y="Price", title="Gold Prices"
        )
        fig2 = px.line(
            commodity_df[commodity_df["Commodity"] == "Silver"], x="Date", y="Price", title="Silver Prices"
        )
        fig3 = px.line(
            commodity_df[commodity_df["Commodity"] == "Oil"], x="Date", y="Price", title="Oil Prices"
        )
        fig4 = px.line(
            commodity_df[commodity_df["Commodity"] == "Natural Gas"], x="Date", y="Price", title="Natural Gas Prices"
        )
        return fig1, fig2, fig3, fig4
    # Skip updates if not on the correct page
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


app = Dash(__name__)
server = app.server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
