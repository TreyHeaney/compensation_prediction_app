# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Can I predict your salary?

            I've built a simple predictive model around the 2020 Stack Overflow Developer Survey results and have deployed this app so you can make predictions. 

            Type in your info and see if I can predict your salary, or maybe just see what the average salary is for someone with certain qualifications.

            """
        ),
        dcc.Link(dbc.Button('Make Predictions', color='primary'), href='/predictions')
    ],
    md=4,
)


column2 = dbc.Col(
    [
        html.Img(src='https://puu.sh/GFlhh/38bdbc19fa.png')
    ]
)

layout = dbc.Row([column1, column2])