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