"""The first page when you open the website"""

# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Can I predict your salary?

            This is an interface for a simple predictive model I built around the 2020 stack overflow developer survey.

            Enter your info, and the model will generate predictions!

            """
        ),
        dcc.Link(dbc.Button('Make Predictions', color='primary'), href='/predictions'),
    ],
    md=4,
)


column2 = dbc.Col(
    [
        html.Img(src='https://puu.sh/GWzUU/cf76028cd8.png'),
        dcc.Markdown('How far off you can expect the model to be according to your true compensation.')
    ]
)

layout = dbc.Row([column1, column2])