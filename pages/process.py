# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Process

            The model we used here is a simple ridge regression boosted with a shallow random forest (random stumps)
            built around the 2020 Stack Overflow Developer Survey results. The preprocessing for the data was implemented
            mostly in pandas/sklearn, and the final predictor was from XGBoost, which is to say I programmed 
            0.01% of it.

            The whole project is covered more in-depth here 
            https://data-sci-ish.blogspot.com/2020/11/a-predictive-model-for-developer.html

            """
        ),

    ],
)

column2 = dbc.Col([
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/6/69/XGBoost_logo.png'),
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1200px-Scikit_learn_logo_small.svg.png',
            style={'height':'50%', 'width':'50%'}),
    html.Img(src='https://puu.sh/GPijH/279a52a228.png',
            style={'height':'50%', 'width':'50%'})
    ],
)

layout = dbc.Row([column1, column2])