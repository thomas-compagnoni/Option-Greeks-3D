from dash import dcc
from dash.html import A, Div, P

from constants import *
from items import *
from utils import px

LAYOUT = Div(
    [
        Div(id='header',
            children=[
                Div(
                    P(children="Welcome to the ultimate Option Greeks 3D Engine!",
                      style={'font-family': 'Helvetica', 'font-size': '30px', 'font-weight': 'bold', 'color': 'black',
                             'textAlign': 'center', 'margin-top': '40px', 'margin-bottom': '40px'}),
                    id='title',
                    style={'height': '100%', 'width': '65%', 'position': 'absolute'}
                ),

                Div(
                    [
                        P(children="The website has been developed by Thomas Compagnoni, MSc student of Finance at Bocconi University.",
                          style={'font-family': 'Helvetica', 'margin-top': '20px', 'margin-bottom': '0px', 'textAlign': 'left',
                                 'font-size': '12px', 'color': 'black'}),
                        P(children=["Check my GitHub projects ",
                                    A('https://github.com/thomas-compagnoni', href='https://github.com/thomas-compagnoni'),
                                    " or follow me on Linkedin ",
                                    A('https://www.linkedin.com/in/thomascompagnoni/', href='https://www.linkedin.com/in/thomascompagnoni/')],
                          style={'font-family': 'Helvetica', 'margin': '0px', 'textAlign': 'left', 'font-size': '12px', 'color': 'black'}),
                        P(children="DISCLAIMER: Only for educational purpose.",
                          style={'font-family': 'Helvetica', 'margin-top': '10px', 'textAlign': 'left',
                                 'padding': '0px 0px', 'font-size': '12px', 'color': 'black'})
                    ],
                    id='info',
                    style={'left': '65%', 'height': '100%', 'width': '35%', 'position': 'absolute'}),
            ],
            style={'height': '115px', 'width': '100%', 'position': 'absolute'}
            ),

        Div(
            [
                Div(
                    children=variables_menu,
                    id='variables',
                    style={'textAlign': 'center', 'height': px(MAIN_HEIGHT - 20), 'width': '27.5%', 'border': '10px solid #F2DFAA'}),

                Div(
                    children=dcc.Loading(
                        id="loading_output",
                        children=[example_button],
                        type="circle",
                        style={'position': 'absolute', 'top': '280px'}
                    ),
                    id='output',
                    style={'height': px(MAIN_HEIGHT - 20), 'width': '69.75%', 'position': 'absolute', 'top': '0px', 'left': '29%',
                           'border': '10px solid #ADD8E6', "overflow": "hidden"}
                ),
            ],
            id='main',
            style={'position': 'relative', 'top': '115px', 'height': px(MAIN_HEIGHT), 'width': '100%', 'display': 'inline-block'}),
    ],
    id='global',
    style={'height': px(HEIGHT), 'width': '99.2%', 'position': 'absolute'}
)
