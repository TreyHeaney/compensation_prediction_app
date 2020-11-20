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
    html.Div(
        [
            dcc.Markdown(
                """
            
                ## Insights

                This page should work with 3d glasses if you want even deeper insight.

                """,
            ),
        html.Img(src='https://puu.sh/GPjr7/4a879cff53.png'),
        html.Img(src='https://puu.sh/GPjr6/0a7fee22d3.png'),
        ], style={'color': '#FF0000'}
    )
)

column2 = dbc.Col(
    html.Div(
        [
            dcc.Markdown(
                """
            
                ## Insights

                This page should work with 3d glasses if you want even deeper insight.

                """,
            ),
        html.Img(src='https://puu.sh/GPjr8/b757532356.png'),
        html.Img(src='https://puu.sh/GPjr5/ff25e5731f.png'),
        ], style={'color': '#00FFFF'}
    )
)

layout = dbc.Row([column1, column2])