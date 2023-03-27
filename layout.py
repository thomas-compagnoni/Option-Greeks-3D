import os
from math import log, exp, pow, sqrt

import numpy as np
import pandas as pd
from scipy.stats import norm

from dash import Dash, dcc, html, ctx, DiskcacheManager, CeleryManager
from dash.dependencies import Input, State, Output
from dash.exceptions import PreventUpdate

import dash_daq as daq

import plotly.graph_objects as go


# ********** OPTION ENGINE **********

def sensitivity_3D(type, on, S, K, r, volatility, T, n3D=40):
    variables_lookup = ['Underlying price (S)', 'Strike (K)', 'Risk-free (r)', 'Volatility (σ)', 'Maturity (T)']
    variables = [S, K, r, volatility, T]

    sens_variables = []
    for i, variable in enumerate(variables):
        if isinstance(variable, tuple):
            sens_variables.append([i, variable, variables_lookup[i]])

    sensitivity_matrix = []
    i = sens_variables[0][0]
    j = sens_variables[1][0]
    X = np.linspace(sens_variables[0][1][0], sens_variables[0][1][1], n3D)
    Y = np.linspace(sens_variables[1][1][0], sens_variables[1][1][1], n3D)
    for x in X:
        variables[i] = x
        row = []
        for y in Y:
            variables[j] = y
            if type == 'call':
                c_greeks = call_black_scholes_merton(variables)
            else:
                c_greeks = put_black_scholes_merton(variables)
            row.append(c_greeks[on])
        sensitivity_matrix.append(row)
    output = pd.DataFrame(sensitivity_matrix, index=X, columns=Y)
    return output, sens_variables[0][2], sens_variables[1][2]


def sensitivity_2D(type, on, S, K, r, volatility, T, n2D=500):
    variables_lookup = ['Underlying price (S)', 'Strike (K)', 'Risk-free (r)', 'Volatility (σ)', 'Maturity (T)']
    variables = [S, K, r, volatility, T]

    sens_variable = None
    for i, variable in enumerate(variables):
        if isinstance(variable, tuple):
            sens_variable = [i, variable, variables_lookup[i]]

    Y = []
    i = sens_variable[0]
    X = np.linspace(sens_variable[1][0], sens_variable[1][1], n2D)
    for x in X:
        variables[i] = x
        if type == 'call':
            c_greeks = call_black_scholes_merton(variables)
        else:
            c_greeks = put_black_scholes_merton(variables)
        Y.append(c_greeks[on])
    return pd.DataFrame(Y, index=X), sens_variable[2]


def call_black_scholes_merton(*args):
    S, K, r, volatility, T = args[0]

    d1 = (log(S / K) + (r + pow(volatility, 2) / 2) * T) / (volatility * sqrt(T))
    d2 = d1 - volatility * sqrt(T)

    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)

    Nd1_ = norm.pdf(d1)

    c_greeks = {'price': S * Nd1 - K * exp(-r * T) * Nd2,
                'delta': Nd1,
                'theta': - (S * Nd1_ * volatility) / (2 * sqrt(T)) - r * K * exp(-r * T) * Nd2,
                'gamma': Nd1_ / (S * volatility * sqrt(T)),
                'vega': S * sqrt(T) * Nd1_,
                'rho': K * T * exp(-r * T) * Nd2
                }

    return c_greeks


def put_black_scholes_merton(*args):
    S, K, r, volatility, T = args[0]

    d1 = (log(S / K) + (r + pow(volatility, 2) / 2) * T) / (volatility * sqrt(T))
    d2 = d1 - volatility * sqrt(T)

    Nd1 = norm.cdf(-d1)
    Nd2 = norm.cdf(-d2)

    Nd1_ = norm.pdf(d1)

    c_greeks = {'price': K * exp(-r * T) * Nd2 - S * Nd1,
                'delta': -Nd1,
                'theta': - (S * Nd1_ * volatility) / (2 * sqrt(T)) + r * K * exp(-r * T) * Nd2,
                'gamma': Nd1_ / (S * volatility * sqrt(T)),
                'vega': S * sqrt(T) * Nd1_,
                'rho': -K * T * exp(-r * T) * Nd2
                }

    return c_greeks


# ******** ITEMS ********

price = [html.P('Underlying price (S)',
                style={'font-family': 'Arial', 'font-size': '15px', 'position': 'relative', 'top': 'px', 'margin': 'auto'}),
         html.Div(
             children=dcc.Input(
                 id='price',
                 type='number',
                 placeholder='Insert the Underlying price (S)',
                 debounce=True,
                 style={'width': '90%', 'height': '20px', 'textAlign': 'center', 'display': 'inline-block',
                        'position': 'absolute', 'left': '7%', 'top': '25px'}),
             id='price_'),
         html.Div(
             children=[
                 dcc.Input(
                     id='price_min',
                     type='number',
                     placeholder='Min Price (S)',
                     debounce=True,
                     style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                            'position': 'absolute', 'left': '7%', 'top': '25px'}),
                 dcc.Input(
                     id='price_max',
                     type='number',
                     placeholder='Max Price (S)',
                     debounce=True,
                     style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                            'position': 'absolute', 'left': '56%', 'top': '25px'})],
             id='price_minmax',
             style={'display': 'none'})
         ]

strike = [html.P('Strike (K)',
                 style={'font-family': 'Arial', 'font-size': '15px', 'position': 'relative', 'top': 'px', 'margin': 'auto'}),
          html.Div(
              children=dcc.Input(
                  id='strike',
                  type='number',
                  placeholder='Insert the Strike (K)',
                  debounce=True,
                  style={'width': '90%', 'height': '20px', 'textAlign': 'center',
                         'position': 'absolute', 'left': '7%', 'top': '25px'}),
              id='strike_'),
          html.Div(
              children=[
                  dcc.Input(
                      id='strike_min',
                      type='number',
                      placeholder='Min Strike (K)',
                      debounce=True,
                      style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                             'position': 'absolute', 'left': '7%', 'top': '25px'}),
                  dcc.Input(
                      id='strike_max',
                      type='number',
                      placeholder='Max Strike (K)',
                      debounce=True,
                      style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                             'position': 'absolute', 'left': '56%', 'top': '25px'})],
              id='strike_minmax',
              style={'display': 'none'})
          ]

rf = [html.P('Risk-free (r)',
             style={'font-family': 'Arial', 'font-size': '15px', 'position': 'relative', 'top': 'px', 'margin': 'auto'}),
      html.Div(
          children=dcc.Input(
              id='rf',
              type='number',
              placeholder='Insert the Risk-free (r)',
              debounce=True,
              style={'width': '90%', 'height': '20px', 'textAlign': 'center',
                     'position': 'absolute', 'left': '7%', 'top': '25px'}),
          id='rf_'),
      html.Div(
          children=[
              dcc.Input(
                  id='rf_min',
                  type='number',
                  placeholder='Min Risk-free (r)',
                  debounce=True,
                  style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                         'position': 'absolute', 'left': '7%', 'top': '25px'}),
              dcc.Input(
                  id='rf_max',
                  type='number',
                  placeholder='Max Risk-free (r)',
                  debounce=True,
                  style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                         'position': 'absolute', 'left': '56%', 'top': '25px'})],
          id='rf_minmax',
          style={'display': 'none'})
      ]

sigma = [html.P('Volatility (σ)',
                style={'font-family': 'Arial', 'font-size': '15px', 'position': 'relative', 'top': 'px', 'margin': 'auto'}),
         html.Div(
             children=dcc.Input(
                 id='sigma',
                 type='number',
                 placeholder='Insert the Volatility (σ)',
                 debounce=True,
                 style={'width': '90%', 'height': '20px', 'textAlign': 'center',
                        'position': 'absolute', 'left': '7%', 'top': '25px'}),
             id='sigma_'),
         html.Div(
             children=[
                 dcc.Input(
                     id='sigma_min',
                     type='number',
                     placeholder='Min Volatility (σ)',
                     debounce=True,
                     style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                            'position': 'absolute', 'left': '7%', 'top': '25px'}),
                 dcc.Input(
                     id='sigma_max',
                     type='number',
                     placeholder='Max Volatility (σ)',
                     debounce=True,
                     style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                            'position': 'absolute', 'left': '56%', 'top': '25px'})],
             id='sigma_minmax',
             style={'display': 'none'})]

maturity = [html.P('Maturity (T)',
                   style={'font-family': 'Arial', 'font-size': '15px', 'position': 'relative', 'top': 'px', 'margin': 'auto'}),
            html.Div(
                children=dcc.Input(
                    id='maturity',
                    type='number',
                    placeholder='Insert the Maturity (T)',
                    debounce=True,
                    style={'width': '90%', 'height': '20px', 'textAlign': 'center',
                           'position': 'absolute', 'left': '7%', 'top': '25px'}),
                id='maturity_'),
            html.Div(
                children=[
                    dcc.Input(
                        id='maturity_min',
                        type='number',
                        placeholder='Min Maturity (T)',
                        debounce=True,
                        style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                               'position': 'absolute', 'left': '7%', 'top': '25px'}),
                    dcc.Input(
                        id='maturity_max',
                        type='number',
                        placeholder='Max Maturity (T)',
                        debounce=True,
                        style={'width': '41%', 'height': '20px', 'textAlign': 'center',
                               'position': 'absolute', 'left': '56%', 'top': '25px'})],
                id='maturity_minmax',
                style={'display': 'none'})]

button_style_on = {'position': 'relative', 'top': '440px',
                   'border': 'none', 'border-radius': '4px', 'height': '40px', 'width': '80%', 'padding': '0px 45px',
                   'font-size': '20px', 'background-color': '#008CBA', 'color': 'white',
                   'cursor': 'pointer'}

button_style_off = {'position': 'relative', 'top': '440px',
                    'border': 'none', 'border-radius': '4px', 'height': '40px', 'width': '80%', 'padding': '0px 45px',
                    'font-size': '20px', 'background-color': '#008CBA', 'color': 'white'}

variables_menu = [
    # html.H3('Insert the variables required below'),

    dcc.Dropdown(
        id="type",
        options=[
            {"label": "Call Option", "value": "call"},
            {"label": "Put Option", "value": "put"}],
        placeholder="Select the option type",
        style={'position': 'relative', 'top': '15px', 'padding': '0px 35px', 'font-size': '15px'}),

    dcc.Dropdown(
        id="result",
        options=[
            {"label": "Price", "value": "price"},
            {"label": "Delta", "value": "delta"},
            {"label": "Theta", "value": "theta"},
            {"label": "Gamma", "value": "gamma"},
            {"label": "Vega", "value": "vega"},
            {"label": "Rho", "value": "rho"},
        ],
        placeholder="Select which option's greek to show",
        style={'position': 'relative', 'top': '25px', 'padding': '0px 35px', 'font-size': '15px'}),

    html.Div(
        children=price,
        id='price_div',
        style={'width': '21.7%', 'height': '60px', 'position': 'absolute', 'top': '160px'}),

    daq.BooleanSwitch(
        id='price_switch',
        color="green",
        style={'position': 'absolute', 'top': '185px', 'left': '23.5%'}),

    html.Div(
        children=strike,
        id='strike_div',
        style={'width': '21.7%', 'height': '60px', 'position': 'absolute', 'top': '230px'}),

    daq.BooleanSwitch(
        id='strike_switch',
        color="green",
        style={'position': 'absolute', 'top': '255px', 'left': '23.5%'}),

    html.Div(
        children=rf,
        id='rf_div',
        style={'width': '21.7%', 'height': '60px', 'position': 'absolute', 'top': '300px'}),

    daq.BooleanSwitch(
        id='rf_switch',
        color="green",
        style={'position': 'absolute', 'top': '325px', 'left': '23.5%'}),

    html.Div(
        children=sigma,
        id='sigma_div',
        style={'width': '21.7%', 'height': '60px', 'position': 'absolute', 'top': '370px'}),

    daq.BooleanSwitch(
        id='sigma_switch',
        color="green",
        style={'position': 'absolute', 'top': '395px', 'left': '23.5%'}),

    html.Div(
        children=maturity,
        id='maturity_div',
        style={'width': '21.7%', 'height': '60px', 'position': 'absolute', 'top': '440px'}),

    daq.BooleanSwitch(
        id='maturity_switch',
        color="green",
        style={'position': 'absolute', 'top': '465px', 'left': '23.5%'}),

    html.Button(
        children='Submit',
        id='submit',
        n_clicks=0,
        style=button_style_on
    )
]

example_button = html.Button(
    children='SHOW ME AN EXAMPLE',
    id='example',
    n_clicks=0,
    style={'position': 'absolute', 'top': '38%', 'left': '35%',
           'border': '3px solid blue', 'border-radius': '12px', 'background-color': 'white', 'height': '24%', 'width': '30%',
           'font-size': '22px', 'color': 'blue',
           'cursor': 'pointer'})

# ********* LAYOUT *********

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

graph_background = go.Figure(go.Surface())
graph_background.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0}, height=580)
graph_background = dcc.Graph(figure=graph_background, style={'display': 'none'})

app.layout = html.Div(
    [
        html.Div(
            html.P(children="Welcome to the ultimate Option Greeks 3D Engine!",
                   style={'font-family': 'Helvetica', 'textAlign': 'center', 'padding': '4px 0px',
                          'font-size': '30px', 'font-weight': 'bold', 'color': 'black'}),
            id='title',
            style={'position': 'absolute', 'top': '1px', 'height': '110px', 'width': '70%'}),
        html.Div(
            [
                html.P(children="The website has been developed by Thomas Compagnoni, MSc student of Finance at Bocconi University.",
                       style={'font-family': 'Helvetica', 'margin-top': '15px', 'margin-bottom': '0px', 'textAlign': 'left',
                              'font-size': '12px', 'color': 'black'}),
                html.P(children=["Check my GitHub projects ",
                                 html.A('https://github.com/thomas-compagnoni', href='https://github.com/thomas-compagnoni'),
                                 " or follow me on Linkedin ",
                                 html.A('https://www.linkedin.com/in/thomascompagnoni/', href='https://www.linkedin.com/in/thomascompagnoni/')],
                       style={'font-family': 'Helvetica', 'margin': '0px', 'textAlign': 'left', 'font-size': '12px', 'color': 'black'}),
                html.P(children="DISCLAIMER: Only for educational purpose.",
                       style={'font-family': 'Helvetica', 'margin-top': '10px', 'textAlign': 'left', 'padding': '0px 0px', 'font-size': '12px', 'color': 'black'})
            ],
            id='info',
            style={'position': 'absolute', 'top': '1px', 'left': '65%', 'height': '110px', 'width': '30%'}),
        html.Div(
            [
                html.Div(
                    children=variables_menu,
                    id='variables',
                    style={'textAlign': 'center', 'height': '580px', 'width': '27.5%', 'border': '10px solid #F2DFAA'}),
                html.Div(
                    dcc.Loading(
                        id="loading",
                        children=[example_button, graph_background],
                        type="graph",
                        style={'position': 'absolute', 'top': '200px'}
                    ),
                    id='graph_div',
                    style={'height': '580px', 'width': '69.75%', 'position': 'absolute', 'top': '0px', 'left': '29%',
                           'border': '10px solid #ADD8E6', "overflow": "hidden"}
                ),
            ],
            id='algo',
            style={'position': 'relative', 'top': '104px', 'height': '600px', 'width': '100%', 'display': 'inline-block'}),
    ]
)


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
        fig.update_layout(margin={'l': 90, 'r': 50, 'b': 0, 't': 110},
                          height=550,
                          plot_bgcolor='white',
                          xaxis_title=x,
                          yaxis_title=on,
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

        return fig

    elif len(result) == 3:
        data, y, x = result
        fig = go.Figure(data=go.Surface(z=data.values, x=data.columns.values, y=data.index.values))
        fig.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
                          height=610
                          )
        fig.update_scenes(xaxis_title=x,
                          yaxis_title=y,
                          zaxis_title=on,
                          )
        fig.update_traces(showscale=False)
        return fig


@app.callback(
    Output(component_id='loading', component_property='children'),
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
            fig = build_figure(result, on)
            return dcc.Graph(figure=fig, style={'position': 'relative', 'top': '-30px'})
        else:
            result = sensitivity_3D(type, on, S, K, r, v, T)
            fig = build_figure(result, on)
            return dcc.Graph(figure=fig, config={'scrollZoom': True}, style={'position': 'relative', 'top': '-30px'})
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
