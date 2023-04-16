from dash import dcc
from dash.html import A, Div, P, H2, Ol, Ul, Li

from constants import *
from items import *
from utils import px

LAYOUT = Div(
    [
        Div(id='header',
            children=[
                Div(
                    P(children="Welcome to the Option Greeks 3D viewer!",
                      style={'font-family': 'Helvetica', 'font-size': '30px', 'font-weight': 'bold', 'color': 'black',
                             'textAlign': 'center', 'margin-top': '40px', 'margin-bottom': '40px'}),
                    id='title',
                    style={'height': '100%', 'width': '60%', 'position': 'absolute'}
                ),
                Div(
                    children=[
                        P(children="The website has been developed by Thomas Compagnoni, MSc student of Finance at Bocconi University.",
                          style={'font-family': 'Helvetica', 'margin-top': '20px', 'margin-bottom': '0px', 'textAlign': 'left',
                                 'font-size': '12px', 'color': 'black'}),
                        P(children=["Check my GitHub projects ",
                                    A('https://github.com/thomas-compagnoni', href='https://github.com/thomas-compagnoni'),
                                    " or follow me on Linkedin ",
                                    A('https://www.linkedin.com/in/thomascompagnoni/', href='https://www.linkedin.com/in/thomascompagnoni/')],
                          style={'font-family': 'Helvetica', 'margin': '0px', 'margin-top': '5px',
                                 'textAlign': 'left', 'font-size': '12px', 'color': 'black'}),
                        P(children="DISCLAIMER: Only for educational purpose.",
                          style={'font-family': 'Helvetica', 'margin-top': '10px', 'textAlign': 'left',
                                 'padding': '0px 0px', 'font-size': '12px', 'color': 'black'})
                    ],
                    id='info',
                    style={'left': '60%', 'height': '100%', 'width': '40%', 'position': 'absolute'}),
            ],
            style={'position': 'relative', 'height': '115px', 'width': '100%'}
            ),

        Div(id='main',
            children=[
                Div(
                    children=variables_menu,
                    id='variables',
                    style={'textAlign': 'center', 'height': px(MAIN_HEIGHT - 20), 'width': '27.5%', 'border': '10px solid #F2DFAA'}
                ),
                Div(
                    children=dcc.Loading(
                        id="loading_output",
                        children=[example_button],
                        type="circle",
                        style={'position': 'absolute', 'top': '260px'}
                    ),
                    id='output',
                    style={'height': px(MAIN_HEIGHT - 20), 'width': '69.75%', 'position': 'absolute', 'top': '0px', 'left': '29%',
                           'border': '10px solid #ADD8E6', "overflow": "hidden"}
                ),
            ],
            style={'position': 'relative', 'height': px(MAIN_HEIGHT), 'width': '100%', 'display': 'inline-block'}
            ),
        Div(id='help',
            children=[
                H2(children='HELP', style={'margin-top': '30px', 'textAlign': 'center'}),
                Ul(children=[
                    Li("Using graphs and matrices, the website aims to help visualizing the behaviour of option's greeks "
                       "as function of one or two variables of the Black-Scholes model.",
                       style={'margin-top': '15px'}),
                    Li("A few quick instructions: ", style={'margin-top': '15px'}),
                    Ol(children=[
                        Li("All of the empty spaces on the left must be filled for the model to work."),
                        Li("The toggle buttons allow to select the variables of interest. "
                           "Choose one for 2D graphs or two for 3D graphs. "
                           "If selected, specify the Min and Max values across which to calculate the greek value.",
                           style={'margin-top': '8px'}),
                        Li("When you click the submit button, the output will appear on the right. "
                           "You can simply switch between graph and matrix by clicking the tab at the top.",
                           style={'margin-top': '8px'}),
                    ],
                        style={'margin-top': '10px'},
                    )
                ],
                    # style={'font-family': 'Helvetica', 'margin-top': '20px',
                    #        'textAlign': 'center', 'list-style-position': 'inside',
                    #        'font-size': '15px', 'color': 'black'}
                    style={'width': '75%', 'marginLeft': 'auto', 'marginRight': 'auto',
                           'font-family': 'Helvetica', 'margin-top': '20px', 'list-style-position': 'inside',
                           'font-size': '15px', 'color': 'black'}
                )
            ],
            style={'position': 'relative', 'height': px(HELP_HEIGHT), 'width': '100%'}
            )
    ],
    id='global',
    style={'height': px(HEIGHT), 'width': '99.2%', 'position': 'absolute'}
)
