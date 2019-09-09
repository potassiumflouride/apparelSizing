import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# import data from excel, to be changed to calling data from database when data is loaded
df = pd.read_csv('../aggregated_datav2.csv')

app.layout = html.Div([
    html.P('Choose a measurement to view its distribution', id = 'test-text'),
    html.Div([
        dcc.Dropdown(
            id = 'column-selector',
            options = [{'label': x, 'value': x} for x in list(df.columns)],
            value = df.columns[0]
        ),
        html.Div(
            dcc.Graph(
                figure = px.scatter(
                    df,
                    x = 'Customer Age',
                    y = df.columns[0],
                    color = 'Customer Gender',
                    size = 'Customer Weight',
                    hover_data=['Customer Weight']
                ),
                id = 'col-scatter'
            ),
            style = {'width': '49%', 'display': 'inline-block', 'horizontal-align': 'left'}
        ),
        html.Div(
            dcc.Graph(
                figure = ff.create_distplot(
                    hist_data = [
                        df[(~np.isnan(df[df.columns[0]])) & (df['Customer Gender'] == 'Male')][df.columns[0]].values,
                        df[(~np.isnan(df[df.columns[0]])) & (df['Customer Gender'] == 'Female')][df.columns[0]].values
                    ],
                    group_labels = ['Male', 'Female'],
                    curve_type = 'normal'
                # )
                # .update_layout
                #         title = go.layout.xaxis.Title(
                #             text = df.columns[0]
                #         )
                #     )
                ),
                id = 'col-histogram'
            ),
            style = {'width': '49%', 'display': 'inline-block', 'horizontal-align': 'right'}
        )
    ]),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id = 'intermediate-value', style = {'display': 'none'})
])

# @app.callback(
#     dash.dependencies.Output('test-text', 'children'),
#     [dash.dependencies.Input('column-selector', 'value')]
# )
# def test(value):
#     return value



@app.callback(
    Output('intermediate-value', 'children'),
    [Input('column-selector', 'value')]
)
def store_col_input(col_name):
    return col_name

@app.callback(
    Output('col-histogram', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_histogram(col_name):
    return ff.create_distplot(
        hist_data = [
            df[(~np.isnan(df[col_name])) & (df['Customer Gender'] == 'Male')][col_name].values,
            df[(~np.isnan(df[col_name])) & (df['Customer Gender'] == 'Female')][col_name].values
        ],
        group_labels = ['Male', 'Female'],
        curve_type = 'normal'
    )

@app.callback(
    Output('col-scatter', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_scatter(col_name):
    return px.scatter(
        df,
        x = 'Customer Age',
        y = col_name,
        color = 'Customer Gender',
        size = 'Customer Weight',
        hover_data=['Customer Weight']
    )

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=True)
    # app.run_server(debug = True)
    # app.run_server()