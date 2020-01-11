import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import pybaseball as pb
import plotly.express as px

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
  dcc.Markdown(children="## Plotly Express Data Sets"),
  html.Br(),
  html.Br(),
  dcc.Markdown(children="### Plotly Express comes with several data sets built-in."),
  dcc.Dropdown(
    id="dropdown",
    options=[
    {'label': 'gapminder', 'value': 'gapminder'},
    {'label': 'tips', 'value': 'tips'},
    {'label': 'iris', 'value': 'iris'},
    {'label': 'wind', 'value': 'wind'},
    {'label': 'election', 'value': 'election'},
    {'label': 'carshare', 'value': 'carshare'}],
    value='gapminder'),
  dcc.Markdown(id='blurb'),
  dcc.Graph(id='graph'),
])

@app.callback(
    [Output(component_id='blurb', component_property='children'),
            Output(component_id='graph', component_property='figure')],
    [Input('dropdown', 'value')])
def update_output_graph(value):
    if value == "gapminder":
        blurb = """ Each row represents a country on a given year.
            https://www.gapminder.org/data/
            Returns:
                A `pandas.DataFrame` with 1704 rows and the following columns: `['country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap',
            'iso_alpha', 'iso_num']`.
        """
        df = px.data.gapminder()
        fig = px.scatter(df, x="gdpPercap", y="lifeExp",             animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country", facet_col="continent",
           log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90])
        fig.update_layout(title="gdp per cap vs life expectancy over time")
        
    if value == "iris":
        blurb = """
            Each row represents a flower.
            https://en.wikipedia.org/wiki/Iris_flower_data_set
            Returns:
                A `pandas.DataFrame` with 150 rows and the following columns: `['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species',
            'species_id']`.
        """
        df = px.data.iris()
        fig = px.density_contour(df, x="sepal_width", y="sepal_length", color="species", marginal_x="rug", marginal_y="histogram")
        
    if value == "tips":
        blurb =  """
            Each row represents a restaurant bill.
            https://vincentarelbundock.github.io/Rdatasets/doc/reshape2/tips.html
            Returns:
                A `pandas.DataFrame` with 244 rows and the following columns: `['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']`.
        """
        df = px.data.tips()
        fig = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group", facet_row="time", facet_col="day",
            category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})
        fig.update_layout(title="tips by gender, day of week, and mealtime")
        
    if value == "election":
        blurb = """
            Each row represents voting results for an electoral district in the 2013 Montreal mayoral election.
            Returns:
                A `pandas.DataFrame` with 58 rows and the following columns: `['district', 'Coderre', 'Bergeron', 'Joly', 'total', 'winner', 'result']`.
        """
        df = px.data.election()
        fig = px.scatter_ternary(df, a="Joly", b="Coderre", c="Bergeron", color="winner", size="total", hover_name="district", size_max=15, color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"} )
        
    if value == "wind":
        blurb =  """
            Each row represents a level of wind intensity in a cardinal direction, and its frequency.
            Returns:
                A `pandas.DataFrame` with 128 rows and the following columns: `['direction', 'strength', 'frequency']`.
        """
        df = px.data.wind()
        fig = px.scatter_polar(df, r="frequency", theta="direction", color="strength", symbol="strength",
                    color_discrete_sequence=px.colors.sequential.Plasma_r)
    
    if value == "carshare":
        blurb = """
            Each row represents the availability of car-sharing services near the centroid of a zone in Montreal.
            Returns:
                A `pandas.DataFrame` with 249 rows and the following columns: `['centroid_lat', 'centroid_lon', 'car_hours', 'peak_hour']`.
        """
        df = px.data.carshare()
        fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10, mapbox_style="open-street-map")
        
    fig.update_yaxes(automargin=True)
        
    return blurb, fig

if __name__ == '__main__':
    app.run_server(debug=True)