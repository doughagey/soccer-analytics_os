import dash_design_kit as ddk
import dash_html_components as html
import pandas as pd
import plotly.express as px

from app import snap


def layout(snapshot_id):
    # This function is called when the snapshot URL is loaded by an end
    # user (displaying the web report) or by the Snapshot Engine's
    # PDF rendering service (when taking a PDF snapshot)
    #
    # The data that was saved by the asynchronous task is loaded and
    # then transformed into a set of `ddk.Report` calls.
    # We're using mock data here just for illustration purposes.
    #
    # You can also save the `ddk.Report` in the task queue instead
    # of just the dataset. Then, you would simply `return snapshot`
    # here. If you saved report, you wouldn't be able to change
    # the layout of the report after it was saved. In this case model,
    # you can update the look and feel of your report in this function
    # _on-the-fly_ when the snapshot is loaded. Note that any changes
    # that you make here won't be reflected in the previously saved PDF
    # version

    snapshot = snap.snapshot_get(snapshot_id)
    figure_1 = snapshot['figure-1']
    figure_2 = snapshot['figure-2']
    figure_3 = snapshot['figure-3']
    return report(figure_1, figure_2, figure_3)


def report(figure_1=None, figure_2=None, figure_3=None):
    # Generate the report a separate function from the snapshot layout
    # so that you can debug the report under a separate URL

    # Check if we're in dev mode, where the report is generated under the
    # /dev URL just to tweak the report layout
    if figure_1 is None:
        figure_1 = px.scatter(df1, x='x1', y='y1')
        figure_2 = px.scatter(df1, x='x2', y='y2')
        figure_3 = px.scatter(df1, x='x2', y='y2')

    return ddk.Report(display_page_numbers=True, children=[

        ddk.Page(
            children=[
                html.Div(
                    'Weekly Report',
                    style={
                        'marginTop': '2in',
                        'fontSize': '28px'
                    }
                ),
                ddk.PageFooter('Not for redistribution')
            ],
            style={
                'backgroundColor': 'var(--accent)',
                'color': 'white'
            }
        ),

        ddk.Page([
            html.H1('Quarterly Earnings'),
            ddk.Block(width=50, margin=5, children=[
                ddk.Graph(figure=figure_1)
            ]),
            ddk.Block(width=50, margin=5, children=[
                ddk.Graph(figure=figure_2)
            ]),

            ddk.Block(width=50, margin=5, children=[
                ddk.Graph(figure=figure_1)
            ]),
            ddk.Block(width=50, margin=5, children=[
                ddk.Graph(figure=figure_2)
            ]),

            ddk.PageFooter("""
                Past Performance Is No Guarantee of Future Results.
            """),
        ]),

        ddk.Page([
            html.H1('Historical Performance'),

            html.P(
                """
                At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis
                praesentium voluptatum deleniti atque corrupti quos dolores et quas.
                """ * 6,
                style={'columnCount': 3}
            ),

            ddk.Block(children=[
                ddk.Graph(figure=figure_3)
            ]),

            ddk.PageFooter('DO NOT DISTRIBUTE')
        ]),

    ])
