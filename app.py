# import packages
import pandas as pd
import numpy as np
import seaborn as sns
from dash import Dash, html, dcc, Output, Input, callback
import plotly.express as px
from datetime import datetime

# import stylesheet
stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# read data and preview the first 5 rows
df = pd.read_csv("./data/cleaned_data.csv")

# create a Dash app
app = Dash(
    __name__, external_stylesheets=stylesheets, suppress_callback_exceptions=True
)

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


def interpolate_experience_levels(level):
    if level == "EN":
        return "Entry"
    elif level == "MI":
        return "Mid"
    elif level == "SE":
        return "Senior"
    elif level == "EX":
        return "Executive"


experience_levels = [
    {"label": interpolate_experience_levels(level), "value": level}
    for level in df["Experience Level"].unique()
]


# change the year slider to display the year instead of the index
def interpolate_years(year_slider):
    return work_years[year_slider]["label"]


# app layout
app.layout = html.Div(
    [
        html.Div([html.H1("Name")]),
        dcc.Tabs(
            id="tabs-example-graph",
            value="graphs",
            children=[
                dcc.Tab(label="Graphs", value="graphs"),
                dcc.Tab(label="About", value="about"),
            ],
            className="",
        ),
        html.Div(id="tabs-content-example-graph"),
    ]
)


# callback to update the graph
@app.callback(
    Output("salary-vs-company-size-graph", "figure"),
    [
        Input("company_size_dropdown", "value"),
        Input("year_slider", "value"),
    ],
)
def update_graph_1(company_size_dropdown, year_slider):
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


@app.callback(
    Output("salary-vs-experience-level-graph", "figure"),
    [
        Input("experience_level_dropdown", "value"),
    ],
)
def update_graph_2(experience_level_dropdown):
    # Filter the DataFrame based on the selected experience levels
    filtered_df = df[df["Experience Level"].isin(experience_level_dropdown)]

    # Define the order of experience levels
    experience_order = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"}

    # Replace the abbreviations with the full form
    filtered_df["Experience Level"] = filtered_df["Experience Level"].map(
        experience_order
    )

    # Now, when you plot, the Experience Levels will be in the correct order
    fig = px.violin(
        filtered_df,
        x="Experience Level",
        y="Salary in USD",
        box=True,
        color="Experience Level",
        title="Salary distribution by Experience Level",
        category_orders={"Experience Level": ["Entry", "Mid", "Senior", "Executive"]},
    )

    return fig


@callback(
    Output("tabs-content-example-graph", "children"),
    Input("tabs-example-graph", "value"),
)
def render_content(tab):
    if tab == "graphs":
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Select company size:"),
                                dcc.Dropdown(
                                    id="company_size_dropdown",
                                    options=company_size_options,
                                    value=[
                                        size["value"] for size in company_size_options
                                    ],
                                    multi=True,
                                ),
                            ],
                            className="two columns",
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
                            className="three columns",
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
                        html.Div(
                            [
                                html.Div("Experience Level:"),
                                dcc.Dropdown(
                                    id="experience_level_dropdown",
                                    value=[
                                        level["value"] for level in experience_levels
                                    ],
                                    options=experience_levels,
                                    multi=True,
                                ),
                            ],
                            className="four columns",
                        ),
                    ],
                    className="center row",
                ),
                html.Div(
                    [
                        dcc.Loading(
                            dcc.Graph(
                                id="salary-vs-experience-level-graph", className="graph"
                            ),
                            type="cube",
                        ),
                        dcc.Loading(
                            dcc.Graph(id="salary-vs-company-size-graph"), type="cube"
                        ),
                    ],
                    className="graph-container",
                ),
            ]
        )
    elif tab == "about":
        return html.Div([html.P("""Description""")])


# run the app
if __name__ == "__main__":
    app.run_server(debug=True)
