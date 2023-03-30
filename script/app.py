import os
from math import log, exp, pow, sqrt

import numpy as np
import pandas as pd
from scipy.stats import norm

from dash import Dash, dcc, html, ctx, DiskcacheManager, CeleryManager, dash_table
from dash.dependencies import Input, State, Output
from dash.exceptions import PreventUpdate

import dash_daq as daq

import plotly.graph_objects as go
from itertools import repeat

from black_scholes_functions import *
from items import *
from layout import *
from utils import *

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery

    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)

else:
    # Diskcache for non-production apps when developing locally
    import diskcache

    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, background_callback_manager=background_callback_manager, prevent_initial_callbacks=True)
server = app.server

@app.callback(
    Output(component_id='price_', component_property='style'),
    Output(component_id='price_minmax', component_property='style'),
    Input(component_id='price_switch', component_property='on'))
def update_output(on):
    if on:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}


@app.callback(
    Output(component_id='strike_', component_property='style'),
    Output(component_id='strike_minmax', component_property='style'),
    Input(component_id='strike_switch', component_property='on'))
def update_output(on):
    if on:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}


@app.callback(
    Output(component_id='rf_', component_property='style'),
    Output(component_id='rf_minmax', component_property='style'),
    Input(component_id='rf_switch', component_property='on'))
def update_output(on):
    if on:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}


@app.callback(
    Output(component_id='sigma_', component_property='style'),
    Output(component_id='sigma_minmax', component_property='style'),
    Input(component_id='sigma_switch', component_property='on'))
def update_output(on):
    if on:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}


@app.callback(
    Output(component_id='maturity_', component_property='style'),
    Output(component_id='maturity_minmax', component_property='style'),
    Input(component_id='maturity_switch', component_property='on'))
def update_output(on):
    if on:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}


@app.callback(
    [Output(component_id='price_switch', component_property='on'),
     Output(component_id='strike_switch', component_property='on'),
     Output(component_id='rf_switch', component_property='on'),
     Output(component_id='sigma_switch', component_property='on'),
     Output(component_id='maturity_switch', component_property='on'),
     Output(component_id='type', component_property='value'),
     Output(component_id='result', component_property='value'),
     Output(component_id='price_min', component_property='value'),
     Output(component_id='price_max', component_property='value'),
     Output(component_id='strike', component_property='value'),
     Output(component_id='rf', component_property='value'),
     Output(component_id='sigma', component_property='value'),
     Output(component_id='maturity_min', component_property='value'),
     Output(component_id='maturity_max', component_property='value'),
     Output(component_id='submit', component_property='n_clicks'),
     Output(component_id='example', component_property='style')
     ],
    Input(component_id='example', component_property='n_clicks'),
    background=True,
    running=[(Output("example", "disabled"), True, False)]
)
def example(n_clicks):
    return True, False, False, False, True, 'call', 'theta', 10, 100, 50, 0.02, 0.25, 0.1, 3, 1, {'display': 'none'}

@app.callback(
    Output(component_id='loading', component_property='children'),
    Output(component_id='tab_matrix', component_property='children'),
    Input(component_id='submit', component_property='n_clicks'),
    State(component_id='type', component_property='value'),
    State(component_id='result', component_property='value'),

    State(component_id='price_switch', component_property='on'),
    State(component_id='price', component_property='value'),
    State(component_id='price_min', component_property='value'),
    State(component_id='price_max', component_property='value'),

    State(component_id='strike_switch', component_property='on'),
    State(component_id='strike', component_property='value'),
    State(component_id='strike_min', component_property='value'),
    State(component_id='strike_max', component_property='value'),

    State(component_id='rf_switch', component_property='on'),
    State(component_id='rf', component_property='value'),
    State(component_id='rf_min', component_property='value'),
    State(component_id='rf_max', component_property='value'),

    State(component_id='sigma_switch', component_property='on'),
    State(component_id='sigma', component_property='value'),
    State(component_id='sigma_min', component_property='value'),
    State(component_id='sigma_max', component_property='value'),

    State(component_id='maturity_switch', component_property='on'),
    State(component_id='maturity', component_property='value'),
    State(component_id='maturity_min', component_property='value'),
    State(component_id='maturity_max', component_property='value'),
    background=True,
    running=[(Output("submit", "style"), button_style_off, button_style_on),
             (Output("submit", "children"), 'Loading...', 'Submit'),
             (Output("submit", "disabled"), True, False)]
)
def graph(n_clicks, type, on,
          onS, S, Sm, SM,
          onK, K, Km, KM,
          onr, r, rm, rM,
          onv, v, vm, vM,
          onT, T, Tm, TM):
    S = extract_value(onS, S, Sm, SM)
    K = extract_value(onK, K, Km, KM)
    r = extract_value(onr, r, rm, rM)
    v = extract_value(onv, v, vm, vM)
    T = extract_value(onT, T, Tm, TM)

    if all([type, on, S, K, r, v, T]):

        dim = sum([1 for x in [S, K, r, v, T] if isinstance(x, tuple)])

        if dim == 1:
            result = sensitivity_2D(type, on, S, K, r, v, T)
            figure = build_figure(result, on)
            table = build_table(result, dim)
            return figure, table
        else:
            result = sensitivity_3D(type, on, S, K, r, v, T)
            figure = build_figure(result, on)
            table = build_table(result, dim)
            return figure, table
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
