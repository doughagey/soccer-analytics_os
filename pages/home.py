from dash.dependencies import Input, Output
import dash_design_kit as ddk
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

from app import app
from ids import IDS

df = px.data.iris()

def layout():
    return html.Div([

        ddk.ControlCard(
            width=100,
            orientation='horizontal',
            children=[
                ddk.ControlItem(
                    label='Species',
                    children=dcc.Dropdown(
                        id='species',
                        options=[
                            {'label': i, 'value': i}
                            for i in df['species_id'].unique()
                        ],
                        value=df['species_id'].unique()[0]
                    )
                ),
            ]

        ),

        ddk.Block(
            width=100,
            id=IDS['SNAPSHOT_ID'],
            children=[
                ddk.Card(
                    width=100,
                    children=ddk.Graph(id=IDS['GRAPH-1'], style={'height': '800px'})
                ),
                ddk.Card(
                    width=50,
                    children=ddk.Graph(id=IDS['GRAPH-2'])
                ),
                ddk.Card(
                    width=50,
                    children=ddk.Graph(id=IDS['GRAPH-3'])
                ),
            ]
        )

    ])



@app.callback(
    [Output(IDS['GRAPH-1'], 'figure'), Output(IDS['GRAPH-2'], 'figure'), Output(IDS['GRAPH-3'], 'figure')],
    [Input('species', 'value')])
def update_graph(value):
    dff = df[df['species_id'] == value]
    figure_1 = px.scatter_matrix(
        dff,
        dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"]
    )

    figure_2 = px.scatter(
        dff, x="sepal_width", y="sepal_length",
        marginal_y="violin", marginal_x="violin")

    figure_3 = px.density_contour(dff, x="sepal_width", y="sepal_length")

    return [figure_1, figure_2, figure_3]
