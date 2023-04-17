import os

from dash import Dash, DiskcacheManager, CeleryManager
from dash.dependencies import Input, State, Output
from dash.exceptions import PreventUpdate

from constants import *
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

app_title = 'Option Greeks 3D visualizer'
app_description = 'View and learn Option Greeks!'
app_image = 'https://i.postimg.cc/Rhk4nNy2/website-3-1.jpg'

meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    {"name": "author", "content": "Thomas Compagnoni"},
    {"property": "twitter:card", "content": "summary_large_image"},
    {"property": "twitter:title", "content": app_title},
    {"property": "twitter:description", "content": app_description},
    {"property": "twitter:image", "content": app_image},
    {"property": "twitter:image:width", "content": "1200"},
    {"property": "twitter:image:height", "content": "619"},
    {"property": "og:title", "content": app_title},
    {"property": "og:type", "content": "website"},
    {"property": "og:description", "content": app_description},
    {"property": "og:image", "content": app_image},
    {"property": "og:image:width", "content": "1200"},
    {"property": "og:image:height", "content": "619"}
]

app = Dash(__name__,
           meta_tags=meta_tags,
           background_callback_manager=background_callback_manager,
           prevent_initial_callbacks=True)

server = app.server
app.layout = LAYOUT
app.title = 'OptionGreeks3D'


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
     Output(component_id='price', component_property='value'),
     Output(component_id='strike_min', component_property='value'),
     Output(component_id='strike_max', component_property='value'),
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
    return False, True, False, False, True, 'call', 'theta', 50, 10, 100, 0.02, 0.25, 0.1, 3, 1, {'display': 'none'}


@app.callback(
    Output(component_id='loading_output', component_property='children'),
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
    running=[(Output("submit", "children"), 'Loading...', 'Submit'),
             (Output("submit", "disabled"), True, False),
             (Output("submit", "style"), button_style_off, button_style)]
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

    try:
        tabs = website_output(type, on, S, K, r, v, T)
        return tabs
    except Exception:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
