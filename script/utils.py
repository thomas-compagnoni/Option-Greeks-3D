from itertools import repeat

import numpy as np
import pandas as pd

from dash.html import Div
from dash.dash_table import DataTable
from dash import dcc

import plotly.graph_objects as go

from items import tab_style, tabs_styles, tab_selected_style

from black_scholes_functions import *
from constants import *


def px(x):
    return f'{x}px'


def extract_value(on, v, vm, vM):
    if on:
        return vm, vM
    else:
        return v


def build_figure(result, on):
    if len(result) == 2:

        data, x = result
        X = data.index.values
        Y = data.values.flatten()
        fig = go.Figure(data=go.Scatter(x=X, y=Y, mode='lines'))
        fig.update_layout(plot_bgcolor='white',
                          xaxis_title=x,
                          yaxis_title=on
                          )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )

        return dcc.Graph(figure=fig, style={'position': 'relative', 'height': '96%', 'padding': '0% 2% 2%'})

    elif len(result) == 3:
        data, y, x = result
        fig = go.Figure(data=go.Surface(z=data.values, x=data.columns.values, y=data.index.values))
        fig.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
        fig.update_scenes(xaxis_title=x,
                          yaxis_title=y,
                          zaxis_title=on,
                          )
        fig.update_traces(showscale=False)

        return dcc.Graph(figure=fig, config={'scrollZoom': True}, style={'position': 'relative', 'height': '100%'})


def datatable_settings_multiindex(df, flatten_char='_'):
    datatable_col_list = []

    levels = df.columns.nlevels
    if levels == 1:
        for i in df.columns:
            datatable_col_list.append({"name": i, "id": i})
    else:
        columns_list = []
        for i in df.columns:
            col_id = flatten_char.join(i)
            datatable_col_list.append({"name": i, "id": col_id})
            columns_list.append(col_id)
        df.columns = columns_list

    datatable_data = df.to_dict('records')

    return datatable_data, datatable_col_list


def build_matrix(result, dim):
    if dim == 1:

        data, x = result
        slices = [int((data.shape[0] - 1) * x) for x in np.linspace(0, 1, 11)]
        data.index = np.round(data.index, 3).map(str)
        data.index = pd.MultiIndex.from_tuples(list(zip(repeat(x), data.index)))

        matrix = data.iloc[slices].T.round(3).copy()
        matrix = matrix.rename(columns={'index': x})

        matrix, columns = datatable_settings_multiindex(matrix)

        return matrix, columns

    elif dim == 2:
        data, y, x = result
        slices_x = [int((data.shape[0] - 1) * x) for x in np.linspace(0, 1, 11)]
        slices_y = [int((data.shape[1] - 1) * y) for y in np.linspace(0, 1, 11)]

        data.index = np.round(data.index, 3).map(str)
        data.columns = np.round(data.columns, 3).map(str)
        data.columns = pd.MultiIndex.from_tuples(list(zip(repeat(x), data.columns)))

        matrix = data.iloc[slices_x, slices_y].round(3).reset_index().copy()
        matrix = matrix.rename(columns={'': y, 'index': ''})

        matrix, columns = datatable_settings_multiindex(matrix)

        return matrix, columns


def build_table(result, dim):
    matrix, columns = build_matrix(result, dim)
    first_col_id = next(iter(matrix[0]))

    if dim == 1:
        table = DataTable(
            id='table',
            columns=columns,
            data=matrix,
            merge_duplicate_headers=True,
            style_header={
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
        )

        return table

    elif dim == 2:

        table = DataTable(
            id='table',
            columns=columns,
            data=matrix,
            merge_duplicate_headers=True,
            style_header={
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': first_col_id},
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                }
            ]
        )

        return table


def build_tabs(graph, table):
    global GRAPH_HEIGHT

    global tabs_style
    global tab_style
    global tab_selected_style

    tabs = dcc.Tabs(
        children=[dcc.Tab(
            children=Div(
                children=graph,
                id='div_graph',
                style={'height': GRAPH_HEIGHT}
            ),
            label='View Graph',
            id='tab_graph',
            style=tab_style,
            selected_style=tab_selected_style
        ),
            dcc.Tab(
                children=Div(
                    children=table,
                    id='div_matrix',
                    style={'display': 'table', 'width': '80%',
                           'marginLeft': 'auto', 'marginRight': 'auto',
                           'margin-top': '8%', 'margin-bottom': '8%'}
                ),
                label='View Matrix',
                id='tab_matrix',
                style=tab_style,
                selected_style=tab_selected_style
            )
        ],

        id="tabs-graph-matrix",
        style=tabs_styles,
        content_style={'height': '100%'},
        parent_style={'height': '100%'}
    )
    return tabs


def website_output(type, on, S, K, r, v, T):
    dim = sum([1 for x in [S, K, r, v, T] if isinstance(x, tuple)])

    if dim == 1:
        result = sensitivity_2D(type, on, S, K, r, v, T)
        figure = build_figure(result, on)
        table = build_table(result, dim)
        tabs = build_tabs(figure, table)
        return [tabs]
    else:
        result = sensitivity_3D(type, on, S, K, r, v, T)
        figure = build_figure(result, on)
        table = build_table(result, dim)
        tabs = build_tabs(figure, table)
        return [tabs]
