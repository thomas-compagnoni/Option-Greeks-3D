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
                    children=[
                        dcc.Tabs(id="tabs-graph-matrix",
                                 children=[
                                     dcc.Tab(label='View Graph',
                                             children=dcc.Loading(
                                                 id="loading",
                                                 children=[example_button, graph_background],
                                                 type="graph",
                                                 style={'position': 'absolute', 'top': '200px', }
                                             ),
                                             style={'padding': '0', 'line-height': '40px'}
                                             ),
                                     dcc.Tab(label='View Matrix',
                                             id='tab_matrix',
                                             style={'padding': '0', 'line-height': '40px'}),
                                 ],
                                 style={'height': '40px'},
                                 content_style={'height': '100%'},
                                 parent_style={'height': '100%'}
                                 ),
                    ],
                    id='graph_div',
                    style={'height': '580px', 'width': '69.75%', 'position': 'absolute', 'top': '0px', 'left': '29%',
                           'border': '10px solid #ADD8E6', "overflow": "hidden"}
                ),
            ],
            id='algo',
            style={'position': 'relative', 'top': '104px', 'height': '600px', 'width': '100%', 'display': 'inline-block'}),
    ]
)
