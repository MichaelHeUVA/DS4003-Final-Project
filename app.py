# import packages
import pandas as pd
from dash import Dash, html, dcc, Output, Input, callback, dash_table
from dash_iconify import DashIconify
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

number_of_countries = len(df["Company Location"].unique())


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


tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#056ab9",
    "color": "white",
    "padding": "6px",
    "fontWeight": "bold",
}

tabs_styles = {"height": "44px"}

tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
}

# app layout
app.layout = html.Div(
    [
        html.Div([html.H1("Salary Analysis of Data Scientists", className="white")]),
        dcc.Tabs(
            id="tabs-example-graph",
            value="graphs",
            children=[
                dcc.Tab(
                    label="Graphs",
                    value="graphs",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Data Table",
                    value="datatable",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="About",
                    value="about",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
            ],
            className="black",
            style=tabs_styles,
        ),
        html.Div(id="tabs-content"),
    ],
)


@callback(
    Output("tabs-content", "children"),
    Input("tabs-example-graph", "value"),
)
def render_content(tab):
    if tab == "graphs":
        return html.Div(
            [
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
                    className="year-container",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Loading(
                                    dcc.Graph(id="countries-pie-chart"),
                                    type="cube",
                                ),
                            ],
                            className="pie-chart",
                        ),
                        html.Div(
                            [
                                dcc.Loading(
                                    dcc.Graph(id="remote-pie-chart"),
                                    type="cube",
                                ),
                            ],
                            className="pie-chart",
                        ),
                        html.Div(
                            [
                                dcc.Loading(
                                    dcc.Graph(id="employment-type-pie-chart"),
                                    type="cube",
                                ),
                            ],
                            className="pie-chart",
                        ),
                    ],
                    className="pie-chart-container",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Loading(
                                    dcc.Graph(
                                        id="salary-vs-experience-level-graph",
                                    ),
                                    type="cube",
                                ),
                                html.Div(
                                    [
                                        html.Div("Experience Level:"),
                                        dcc.Dropdown(
                                            id="experience_level_dropdown",
                                            value=[
                                                level["value"]
                                                for level in experience_levels
                                            ],
                                            options=experience_levels,
                                            style={"opacity": "100%"},
                                            multi=True,
                                        ),
                                    ],
                                    className="five columns",
                                ),
                            ],
                            className="graph-container",
                        ),
                        html.Div(
                            [
                                dcc.Loading(
                                    dcc.Graph(id="salary-vs-company-size-graph"),
                                    type="cube",
                                ),
                                html.Div(
                                    [
                                        html.Div("Select company size:"),
                                        dcc.Dropdown(
                                            id="company_size_dropdown",
                                            options=company_size_options,
                                            value=[
                                                size["value"]
                                                for size in company_size_options
                                            ],
                                            multi=True,
                                        ),
                                    ],
                                    className="five columns",
                                ),
                            ],
                            className="graph-container",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div("Select number of countries:"),
                                        dcc.Slider(
                                            id="number_of_countries_slider",
                                            min=1,
                                            max=number_of_countries,
                                            value=25,
                                            marks={
                                                i: str(i)
                                                for i in range(
                                                    1, number_of_countries + 1
                                                )
                                                if i % 2 == 0
                                            },
                                            step=1,
                                        ),
                                    ],
                                    className="",
                                ),
                                html.Div(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="median-salary-in-USD-vs-company-location"
                                            ),
                                            type="cube",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="center90",
                ),
                html.Div(
                    [
                        dcc.Loading(
                            dcc.Graph(id="most-frequent-job-titles"), type="cube"
                        )
                    ],
                    className="center90 margin",
                ),
            ]
        )
    elif tab == "datatable":
        return html.Div(
            dash_table.DataTable(
                id="datatable",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
            ),
            className="black",
        )

    elif tab == "about":
        return html.Div(
            [
                html.H3("Why I chose this dataset?"),
                html.P(
                    """Choosing this data science salary dataset for the term project was motivated by its significance to current job market trends, its relevance to a wide audience in the field of data science, and the rich analytical opportunities it presents. It offers a comprehensive global perspective on aspects like salary trends, employment types, and experience levels across different geographies. This not only allows for an extensive comparative and trend analysis over time but also provides practical insights useful for both job seekers and employers."""
                ),
                html.H3("Provenance of the dataset"),
                html.P(
                    """The collection methodology for the Data Science Salaries Dataset involves gathering salary information from diverse sources such as industry surveys, job postings, employer reports, and recruitment agencies. Data is typically collected through surveys, online job platforms, and direct communication with companies. Information on job titles, locations, experience levels, skills required, and additional benefits is systematically recorded. The dataset undergoes validation and quality checks to ensure accuracy and reliability."""
                ),
                html.Div(
                    [
                        html.A(
                            [
                                DashIconify(
                                    icon="devicon:kaggle",
                                    width=50,
                                    height=50,
                                ),
                            ],
                            target="_blank",
                            href="https://www.kaggle.com/datasets/zain280/data-science-salaries",
                        ),
                        html.A(
                            [
                                DashIconify(
                                    icon="ion:logo-github",
                                    width=50,
                                    height=50,
                                ),
                            ],
                            href="https://github.com/MichaelHeUVA/plotly-dash",
                            target="_blank",
                            className="github",
                        ),
                    ],
                    className="flex",
                ),
            ],
            className="about",
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
    fig.update_layout(
        {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"}
    )
    fig.update_layout(font=dict(color="white"))
    return fig


@app.callback(
    Output("salary-vs-experience-level-graph", "figure"),
    [
        Input("experience_level_dropdown", "value"),
        Input("year_slider", "value"),
    ],
)
def update_graph_2(experience_level_dropdown, year_slider):
    year_slider = list(range(year_slider[0], year_slider[1] + 1))
    year_slider = map(interpolate_years, year_slider)
    filtered_df = df[df["Work Year"].isin(year_slider)]
    filtered_df = filtered_df[
        filtered_df["Experience Level"].isin(experience_level_dropdown)
    ]
    experience_order = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"}
    filtered_df["Experience Level"] = filtered_df["Experience Level"].map(
        experience_order
    )

    fig = px.violin(
        filtered_df,
        x="Experience Level",
        y="Salary in USD",
        box=True,
        color="Experience Level",
        title="Salary distribution by Experience Level",
        category_orders={"Experience Level": experience_order.values()},
    )

    fig.update_layout(
        {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(255, 255, 255, 0)"}
    )
    fig.update_layout(font=dict(color="white"))
    return fig


@app.callback(
    Output("median-salary-in-USD-vs-company-location", "figure"),
    [
        Input("year_slider", "value"),
        Input("number_of_countries_slider", "value"),
    ],
)
def update_graph_3(year_slider, number_of_companies_slider):
    year_slider = list(range(year_slider[0], year_slider[1] + 1))
    year_slider = map(interpolate_years, year_slider)
    filtered_df = df[df["Work Year"].isin(year_slider)]
    filtered_df = (
        filtered_df.groupby("Company Location")["Salary in USD"].median().reset_index()
    ).sort_values("Salary in USD", ascending=False)
    filtered_df = filtered_df.head(number_of_companies_slider)

    fig = px.bar(
        filtered_df,
        x="Company Location",
        y="Salary in USD",
        title="Median salary in USD by Company Location",
        text_auto=".2s",
    )
    fig.update_traces(
        textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )
    fig.update_layout(
        {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"}
    )
    fig.update_layout(font=dict(color="white"))
    return fig


@app.callback(
    Output("most-frequent-job-titles", "figure"),
    Input("year_slider", "value"),
)
def update_graph_4(year_slider):
    year_slider = list(range(year_slider[0], year_slider[1] + 1))
    year_slider = map(interpolate_years, year_slider)
    filtered_df = df[df["Work Year"].isin(year_slider)]
    job_titles = (
        filtered_df["Job Title"].value_counts().head(10).sort_values(ascending=True)
    )
    fig = px.bar(
        x=job_titles.values,
        y=job_titles.index,
        orientation="h",
        title="Top 10 Most Frequent Job Titles",
        labels={"x": "Number of job titles", "y": "Job Title"},
    )
    fig.update_layout(
        {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"}
    )
    fig.update_layout(font=dict(color="white"))
    return fig


@app.callback(
    Output("countries-pie-chart", "figure"),
    [
        Input("year_slider", "value"),
    ],
)
def update_pie_chart(year_slider):
    year_slider = list(range(year_slider[0], year_slider[1] + 1))
    year_slider = map(interpolate_years, year_slider)
    filtered_df = df[df["Work Year"].isin(year_slider)]
    country_counts = filtered_df["Company Location"].value_counts()
    fig = px.pie(
        values=country_counts.values,
        names=country_counts.index,
        title="Country Distribution of Companies",
        labels={"names": "Country", "values": "Number of companies"},
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"}
    )
    fig.update_layout(font=dict(color="white"))
    return fig


@app.callback(
    Output("remote-pie-chart", "figure"),
    [
        Input("year_slider", "value"),
    ],
)
def update_pie_chart2(year_slider):
    year_slider = list(range(year_slider[0], year_slider[1] + 1))
    year_slider = map(interpolate_years, year_slider)
    filtered_df = df[df["Work Year"].isin(year_slider)]
    remote_counts = filtered_df["Remote Ratio"].value_counts()
    fig = px.pie(
        values=remote_counts.values,
        names=remote_counts.index,
        title="Remote Ratio Distribution",
        labels={"names": "Remote Ratio", "values": "Number of companies"},
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"}
    )
    fig.update_layout(font=dict(color="white"))
    return fig


@app.callback(
    Output("employment-type-pie-chart", "figure"),
    [
        Input("year_slider", "value"),
    ],
)
def update_pie_chart3(year_slider):
    year_slider = list(range(year_slider[0], year_slider[1] + 1))
    year_slider = map(interpolate_years, year_slider)
    filtered_df = df[df["Work Year"].isin(year_slider)]
    employment_type_counts = filtered_df["Employment Type"].value_counts()
    fig = px.pie(
        values=employment_type_counts.values,
        names=employment_type_counts.index,
        title="Employment Type Distribution",
        labels={"names": "Employment Type", "values": "Number of companies"},
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"}
    )
    fig.update_layout(font=dict(color="white"))
    return fig


# run the app
if __name__ == "__main__":
    app.run_server(debug=True)
