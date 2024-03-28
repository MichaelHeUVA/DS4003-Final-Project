# import packages
import pandas as pd
import numpy as np
import seaborn as sns
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
from datetime import datetime

# import stylesheet
stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# read data and preview the first 5 rows
df = pd.read_csv("data.csv")

# create a Dash app
app = Dash(__name__, external_stylesheets=stylesheets)

# get the server
server = app.server


company_size_options = sorted(
    [{"label": size, "value": size} for size in df["Company Size"].unique()],
    key=lambda x: x["label"],
    reverse=True,
)

# create a dictionary to map the index to the formatted year
work_years_format = {
    i: {"label": datetime.strptime(year, "%Y-%m-%d").strftime("%Y")}
    for i, year in enumerate(df["Work Year"].unique())
}

# create a dictionary to map the index to the year
work_years = {i: {"label": year} for i, year in enumerate(df["Work Year"].unique())}

remote_ratios = [
    {"label": str(ratio) + "%", "value": ratio} for ratio in df["Remote Ratio"].unique()
]

experience_levels = [
    {"label": level, "value": level} for level in df["Experience Level"].unique()
]


# change the year slider to display the year instead of the index
def interpolate_years(year_slider):
    return work_years[year_slider]["label"]


# app layout
app.layout = html.Div(
    [
        html.Div([html.H1("Sprint 4: Dashboard V0"), html.P("""""")]),
        html.Div(
            [
                html.Div(
                    [
                        html.Div("Select company size:"),
                        dcc.Dropdown(
                            id="company_size_dropdown",
                            options=company_size_options,
                            value=[size["value"] for size in company_size_options],
                            multi=True,
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.Div("Select year range:"),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=0,
                            max=len(work_years) - 1,
                            value=[0, len(work_years) - 1],
                            marks=work_years_format,
                            step=1,
                        ),
                    ],
                    className="six columns",
                ),
                # html.Div(
                #     [
                #         html.Div("Remote ratio:"),
                #         dcc.Dropdown(
                #             id="remote_ratio_dropdown",
                #             options=remote_ratios,
                #             multi=True,
                #         ),
                #     ],
                #     className="six columns",
                # ),
                # html.Div(
                #     [
                #         html.Div("Experience Level:"),
                #         dcc.Dropdown(
                #             id="experience_level_dropdown",
                #             options=experience_levels,
                #             multi=True,
                #         ),
                #     ],
                #     className="six columns",
                # ),
            ],
            className="row",
        ),
        html.Div([dcc.Loading(dcc.Graph(id="?-graph"), type="cube")]),
    ]
)


# callback to update the graph
@app.callback(
    Output("?-graph", "figure"),
    [
        Input("company_size_dropdown", "value"),
        Input("year_slider", "value"),
    ],
)
def update_graph(company_size_dropdown, year_slider):
    year_slider = list(range(year_slider[0], year_slider[1] + 1))
    year_slider = map(interpolate_years, year_slider)
    filtered_df = df[df["Company Size"].isin(company_size_dropdown)]
    filtered_df = filtered_df[filtered_df["Work Year"].isin(year_slider)]
    filtered_df = filtered_df.sort_values("Company Size", ascending=False)
    filtered_df["Company Size"] = filtered_df["Company Size"].replace(
        {"S": "Small", "M": "Medium", "L": "Large"}
    )
    fig = px.violin(
        filtered_df,
        x="Company Size",
        y="Salary in USD",
        box=True,
        color="Company Size",
        title="Salary distribution by Company Size",
    )
    return fig


# run the app
if __name__ == "__main__":
    app.run_server(debug=True)
