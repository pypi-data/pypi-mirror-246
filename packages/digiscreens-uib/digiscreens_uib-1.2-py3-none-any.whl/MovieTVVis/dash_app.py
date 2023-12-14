import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from src.MovieTVVis import MovieTVVis
import plotly.express as px

app = dash.Dash(__name__, suppress_callback_exceptions=True)
mtv = MovieTVVis.MovieTVVis()
mtv.import_csv("data/movies_dummy_data_lists.csv", sep=';')
available_variables = ["ID", "MovieName", "Year", "Genre", "ProductionCountry", "ProductionCompany", "IMDBScore", "Runtime", "StreamingService", "RentBuyService"]

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Heatmap', children=[
            dcc.Dropdown(
                id='heatmap-x-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
                placeholder='x'
            ),
            dcc.Dropdown(
                id='heatmap-y-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
                placeholder='y'
            ),
            dcc.RadioItems(
                id='relative-values',
                options=[
                    {'label': 'None', 'value': 'none'},
                    {'label': 'X-axis', 'value': 'x'},
                    {'label': 'Y-axis', 'value': 'y'},
                    {'label': 'All', 'value': 'all'}
                ],
            ),
            dcc.Graph(id='heatmap-output')
            
        ]),
        dcc.Tab(label='Pie Chart', children=[
            dcc.Dropdown(
                id='pie-target-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
                placeholder='Target variable'
            ),
            dcc.Dropdown(
                id='pie-relative-values',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                placeholder='Relative values'
            ),
            dcc.Graph(id='pie-chart-output')

        ]),
        dcc.Tab(label='Bar Chart', children=[
            dcc.Dropdown(
                id='bar-target-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
                placeholder='Target variable'
            ),
            dcc.Dropdown(
                id='bar-relative-values',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                placeholder='Relative values'
            ),
            dcc.Graph(id='bar-chart-output')

        ]),
        dcc.Tab(label='Line Chart', children=[
            dcc.Dropdown(
                id='line-x-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
                placeholder='x'
            ),
            dcc.Dropdown(
                id='line-target-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
                placeholder='Target variable'
            ),
            dcc.Dropdown(
                id='line-relative-values',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                placeholder='Relative values'
            ),
            dcc.Graph(id='line-chart-output')

        ]),
        dcc.Tab(label='Scatter Plot', children=[
            dcc.Dropdown(
                id='scatter-x-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
            ),
            dcc.Dropdown(
                id='scatter-y-variable',
                options=[{'label': var, 'value': var} for var in available_variables],
            ),
            dcc.Dropdown(
                id='scatter-trendline',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
            ),
            dcc.Graph(id='scatter-plot-output')

        ])
    ]),
])



@app.callback(
    Output('heatmap-output', 'figure'),
    [
        Input('heatmap-x-variable', 'value'),
        Input('heatmap-y-variable', 'value'),
        Input('relative-values', 'value')
    ]
)
def update_heatmap(x_var, y_var, relative_value):
    fig = mtv.heatmap(x=x_var, y=y_var, relative_values=relative_value)
    return fig


@app.callback(
    Output('pie-chart-output', 'figure'),
    Input('pie-target-variable', 'value'),
    Input('pie-relative-values', 'value')   
)
def update_pie_chart(target_var, relative_value):
    fig = mtv.pie(target=target_var, relative_values=relative_value)
    return fig


@app.callback(
    Output('bar-chart-output', 'figure'),
    [
        Input('bar-target-variable', 'value'),
        Input('bar-relative-values', 'value')
    ]
)
def update_bar_chart(target_var, relative_value):
    fig = mtv.bar(target=target_var, relative_values=relative_value)
    return fig


@app.callback(
    Output('line-chart-output', 'figure'),
    [
        Input('line-x-variable', 'value'),
        Input('line-target-variable', 'value'),
        Input('line-relative-values', 'value')
    ]
)
def update_line_chart(x_var, target_var, relative_value):
    fig = mtv.line(x=x_var, target=target_var, relative_values=relative_value)
    return fig


@app.callback(
    Output('scatter-plot-output', 'figure'),
    [
        Input('scatter-x-variable', 'value'),
        Input('scatter-y-variable', 'value'),
        Input('scatter-trendline', 'value'),
    ]
)
def update_scatter_plot(x_var, y_var, trendline):
    fig = mtv.scatter(x=x_var, y=y_var, trendline=trendline)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)