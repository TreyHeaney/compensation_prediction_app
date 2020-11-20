# What's up

# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
import numpy as np
import pandas as pd
import category_encoders
import xgboost
from app import app
from joblib import load

# Our pipeline we pickled
pipeline = load('assets/dump.joblib')
# And an empty dataframe with merely the columns we used
empty_dataframe = load('assets/df.joblib')

@app.callback(
    Output('prediction-content', 'children'),
    [Input('Age', 'value'), 
    Input('Age1stCode', 'value'),
    Input('YearsCode', 'value'),
    Input('YearsCodePro', 'value'),
    Input('Hobbyist', 'value'),
    Input('MainBranch', 'value'),
    Input('EdLevel', 'value'),
    Input('UndergradMajor', 'value'),
    Input('Employment', 'value'),
    Input('NEWOvertime', 'value'),
    Input('Devtype', 'value'),
    Input('LanguageWorkedWith', 'value'),
    Input('DatabaseWorkedWith', 'value'),
    Input('WebframeWorkedWith', 'value'),
    Input('PlatformWorkedWith', 'value'),
    Input('MiscTechWorkedWith', 'value'),
    Input('NEWCollabToolsWorkedWith', 'value'),
    Input('Ethnicity', 'value'),
    Input('WorkWeekHrs', 'value')
    ]
)

def predict(Age, Age1stCode, YearsCode, YearsCodePro, Hobbyist, MainBranch, EdLevel, 
            UndergradMajor, Employment, NEWOvertime, Devtype, LanguageWorkedWith, DatabaseWorkedWith, 
            WebframeWorkedWith, PlatformWorkedWith, MiscTechWorkedWith, NEWCollabToolsWorkedWith,
            Ethnicity, WorkWeekHrs):

    # We cast the variables to a temporary dataframe so we can do column manipulation more easily
    temp_dataframe = pd.DataFrame(columns=['Age', 'Age1stCode', 'YearsCode', 'YearsCodePro', 'Hobbyist', 
                'MainBranch', 'EdLevel', 'UndergradMajor', 'Employment', 'NEWOvertime', 'Devtype', 'LanguageWorkedWith', 
                'DatabaseWorkedWith', 'WebframeWorkedWith', 'PlatformWorkedWith', 'MiscTechWorkedWith', 'NEWCollabToolsWorkedWith', 
                'Ethnicity', 'WorkWeekHrs'
        ],
        data=[[Age, Age1stCode, YearsCode, YearsCodePro, Hobbyist, MainBranch, EdLevel, 
            UndergradMajor, Employment, NEWOvertime, Devtype, LanguageWorkedWith, DatabaseWorkedWith, 
            WebframeWorkedWith, PlatformWorkedWith, MiscTechWorkedWith, NEWCollabToolsWorkedWith,
            Ethnicity, WorkWeekHrs
            ]]
    )

    
    features = empty_dataframe.copy()
    
    # The model takes onehotencoded columns for 'select all' columns but for variables collected with checkboxes we get a list returned ...
    # ...so we loop through it and onehotencode each value in each list.
    values_potentially_containing_lists = [DatabaseWorkedWith, LanguageWorkedWith, WebframeWorkedWith, 
                                           PlatformWorkedWith, MiscTechWorkedWith, NEWCollabToolsWorkedWith,Ethnicity
                                          ]
    for column_set in values_potentially_containing_lists:
        # If one value is recoreded, the checkboxes return only a string...
        if isinstance(column_set, str):
            temp_dataframe[column_set] = 1
        # ...otherwise it returns a list.
        if isinstance(column_set, list):
            for nested_col in column_set:
                temp_dataframe[nested_col] = 1

    # And now we cast all columns onto the dataframe we imported to perserve the order of the columns with minimal headache.
    for col in temp_dataframe.columns:
        if col in features.columns:
            features[col] = temp_dataframe[col]
    
    to_return = int(pipeline.predict(features)[0])
    to_return = f'${to_return}'

    return to_return





# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            # Predictions

            Plug in your info and the model will generate a prediction based of it! 
            Some questions were removed to make it quicker to fill out and because 
            of lack of correlation, so the actual model is slightly more accurate.

            You might notice some non-linear relationships, and this is likely because 
            the high dimensionality of the input data.

            """
        ),
        html.H2('Projected Annual Compensation:', className='mb-5'), 
        html.Div(id='prediction-content', className='lead')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown('### Age'),
        dcc.Slider(
            id='Age', 
            min=17, 
            max=80, 
            step=1, 
            value=17, 
            marks=({n: str(n) for n in range(17,80, 2)}), 
            className='mb-5'
        ),
        dcc.Markdown('### Age when you first programmed'),
        dcc.Slider(
            id='Age1stCode', 
            min=0, 
            max=50, 
            step=1, 
            value=0, 
            marks=({n: str(n) for n in range(0, 51, 2)}), 
            className='mb-5'
        ),
        dcc.Markdown('### Years programming'),
        dcc.Slider(
            id='YearsCode', 
            min=0, 
            max=50, 
            step=1, 
            value=0, 
            marks=({n: str(n) for n in range(0, 51, 2)}), 
            className='mb-5'
        ),
        dcc.Markdown('### Years programming Professionally'),
        dcc.Slider(
            id='YearsCodePro', 
            min=0, 
            max=50, 
            step=1, 
            value=0, 
            marks=({n: str(n) for n in range(0, 51, 2)}), 
            className='mb-5'
        ),
        dcc.Markdown('### Work week hours'),
        dcc.Slider(
            id='WorkWeekHrs', 
            min=0, 
            max=70, 
            step=1, 
            value=0, 
            marks=({n: str(n) for n in range(0, 71, 5)}), 
            className='mb-5'
        ),
        dcc.Markdown('### Do you program as a hobby?'),
        dcc.Dropdown(
            id='Hobbyist',
            options=[
                {'label': 'Yes  ', 'value': 'Yes'},
                {'label': 'No  ', 'value': 'No'},
            ]
        ),

        # Don't feel too bad for me, this was mostly generated with a script

        dcc.Markdown('### Are you a developer by profession?'),
        dcc.Dropdown(
            id='MainBranch',
            options=[
                {'label': 'I am a developer by profession', 'value': 'I am a developer by profession'},
                {'label': 'I am not primarily a developer, but I write code sometimes as part of my work', 'value': 'I am not primarily a developer, but I write code sometimes as part of my work'}
                ]
        ),
        dcc.Markdown('### What is the size of the organization that employs you?'),
        dcc.Dropdown(
            id='OrgSize',
            options=[
                {'label': 'Just me - I am a freelancer, sole proprietor, etc.', 'value': 'Just me - I am a freelancer, sole proprietor, etc.'},
                {'label': '2 to 9 employees', 'value': '2 to 9 employees'},
                {'label': '10 to 19 employees', 'value': '10 to 19 employees'},
                {'label': '20 to 99 employees', 'value': '20 to 99 employees'},
                {'label': '100 to 499 employees', 'value': '100 to 499 employees'},
                {'label': '500 to 999 employees', 'value': '500 to 999 employees'},
                {'label': '1,000 to 4,999 employees', 'value': '1,000 to 4,999 employees'},
                {'label': '5,000 to 9,999 employees', 'value': '5,000 to 9,999 employees'},
                {'label': '10,000 or more employees', 'value': '10,000 or more employees'},
            ]
        ),
        dcc.Markdown('### What is your education level?'),
        dcc.Dropdown(
            id='EdLevel',
            options=[
                {'label': 'I never completed any formal education', 'value': 'I never completed any formal education'},
                {'label': 'Primary/elementary school', 'value': 'Primary/elementary school'},
                {'label': 'Some college/university study without earning a degree', 'value': 'Some college/university study without earning a degree'},
                {'label': 'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)', 'value': 'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)'},
                {'label': 'Associate degree (A.A., A.S., etc.)', 'value': 'Associate degree (A.A., A.S., etc.)'},
                {'label': 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)', 'value': 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)'},
                {'label': 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)', 'value': 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)'},
                {'label': 'Professional degree (JD, MD, etc.)', 'value': 'Professional degree (JD, MD, etc.)'},
                {'label': 'Other doctoral degree (Ph.D., Ed.D., etc.)', 'value': 'Other doctoral degree (Ph.D., Ed.D., etc.)'},
            ]
        ),  
        dcc.Markdown('### What was your undergrad major? (if any)'),
        dcc.Dropdown(
            id='UndergradMajor',
            options=[
                {'label': 'Computer science, computer engineering, or software engineering', 'value': 'Computer science, computer engineering, or software engineering'},
                {'label': 'Mathematics or statistics', 'value': 'Mathematics or statistics'},
                {'label': 'A business discipline (such as accounting, finance, marketing, etc.)', 'value': 'A business discipline (such as accounting, finance, marketing, etc.)'},
                {'label': 'Another engineering discipline (such as civil, electrical, mechanical, etc.)', 'value': 'Another engineering discipline (such as civil, electrical, mechanical, etc.)'},
                {'label': 'A humanities discipline (such as literature, history, philosophy, etc.)', 'value': 'A humanities discipline (such as literature, history, philosophy, etc.)'},
                {'label': 'A health science (such as nursing, pharmacy, radiology, etc.)', 'value': 'A health science (such as nursing, pharmacy, radiology, etc.)'},
                {'label': 'Information systems, information technology, or system administration', 'value': 'Information systems, information technology, or system administration'},
                {'label': 'Web development or web design', 'value': 'Web development or web design'},
                {'label': 'A natural science (such as biology, chemistry, physics, etc.)', 'value': 'A natural science (such as biology, chemistry, physics, etc.)'},
                {'label': 'Fine arts or performing arts (such as graphic design, music, studio art, etc.)', 'value': 'Fine arts or performing arts (such as graphic design, music, studio art, etc.)'},
                {'label': 'I never declared a major', 'value': 'I never declared a major'},
                {'label': 'A social science (such as anthropology, psychology, political science, etc.)', 'value': 'A social science (such as anthropology, psychology, political science, etc.)'},
            ]
        ),
        dcc.Markdown('### What is your current employment status?'),
        dcc.Dropdown(
            id='Employment',
            options=[
                {'label': 'Not employed, and not looking for work', 'value': 'Not employed, and not looking for work'},
                {'label': 'Not employed, but looking for work', 'value': 'Not employed, but looking for work'},
                {'label': 'Student', 'value': 'Student'},
                {'label': 'Employed part-time', 'value': 'Employed part-time'},
                {'label': 'Independent contractor, freelancer, or self-employed', 'value': 'Independent contractor, freelancer, or self-employed'},
                {'label': 'Employed full-time', 'value': 'Employed full-time'},
                {'label': 'Retired', 'value': 'Retired'},
            ]
        ),
        dcc.Markdown('### How often do you work overtime?'),
        dcc.Dropdown(
            id='NEWOvertime',
            options=[
                {'label': 'Never', 'value': 'Never'},
                {'label': 'Rarely: 1-2 days per year or less', 'value': 'Rarely: 1-2 days per year or less'},
                {'label': 'Occasionally: 1-2 days per quarter but less than monthly', 'value': 'Occasionally: 1-2 days per quarter but less than monthly'},
                {'label': 'Sometimes: 1-2 days per month but less than weekly', 'value': 'Sometimes: 1-2 days per month but less than weekly'},
                {'label': 'Often: 1-2 days per week or more', 'value': 'Often: 1-2 days per week or more'},
            ]
        ),
        dcc.Markdown('### What is the primary operating system you use professionally?'),
        dcc.Dropdown(
            id='OpSys',
            options=[
                {'label': 'Windows', 'value': 'Windows'},
                {'label': 'Linux-based', 'value': 'Linux-based'},
                {'label': 'MacOS', 'value': 'MacOS'},
                {'label': 'BSD', 'value': 'BSD'},
            ]
        ),
        dcc.Markdown(' '),
        dcc.Markdown('### What type of developer are you? (Select all that apply)'),
        dcc.Checklist(
            id='Devtype',
            options=[
                    {'label': 'Developer, desktop or enterprise applications  ', 'value': 'Developer, desktop or enterprise applications'},
                    {'label': 'Developer, full-stack  ', 'value': 'Developer, full-stack'},
                    {'label': 'Developer, mobile  ', 'value': 'Developer, mobile'},
                    {'label': 'Designer  ', 'value': 'Designer'},
                    {'label': 'Developer, front-end  ', 'value': 'Developer, front-end'},
                    {'label': 'Developer, back-end  ', 'value': 'Developer, back-end'},
                    {'label': 'Developer, QA or test  ', 'value': 'Developer, QA or test'},
                    {'label': 'DevOps specialist  ', 'value': 'DevOps specialist'},
                    {'label': 'Developer, game or graphics  ', 'value': 'Developer, game or graphics'},
                    {'label': 'Database administrator  ', 'value': 'Database administrator'},
                    {'label': 'Developer, embedded applications or devices  ', 'value': 'Developer, embedded applications or devices'},
                    {'label': 'Engineer, data  ', 'value': 'Engineer, data'},
                    {'label': 'Educator  ', 'value': 'Educator'},
                    {'label': 'System administrator  ', 'value': 'System administrator'},
                    {'label': 'Engineering manager  ', 'value': 'Engineering manager'},             # Are you lost?
                    {'label': 'Product manager  ', 'value': 'Product manager'},
                    {'label': 'Data or business analyst  ', 'value': 'Data or business analyst'},
                    {'label': 'Academic researcher  ', 'value': 'Academic researcher'},
                    {'label': 'Data scientist or machine learning specialist  ', 'value': 'Data scientist or machine learning specialist'},
                    {'label': 'Scientist  ', 'value': 'Scientist'},
                    {'label': 'Senior executive/VP  ', 'value': 'Senior executive/VP'},
                    {'label': 'Engineer, site reliability  ', 'value': 'Engineer, site reliability'},
                    {'label': 'Marketing or sales professional  ', 'value': 'Marketing or sales professional'},
                ],
            style={'display': "inline-block"}
        ),
        dcc.Markdown('### What languages do you utilize professionally?'),
        dcc.Checklist(
            id='LanguageWorkedWith',
            options=[
                {'label': 'C#  ', 'value': 'C#'},
                {'label': 'HTML/CSS  ', 'value': 'HTML/CSS'},
                {'label': 'JavaScript  ', 'value': 'JavaScript'},
                {'label': 'Swift  ', 'value': 'Swift'},
                {'label': 'Objective-C  ', 'value': 'Objective-C'},
                {'label': 'Python  ', 'value': 'Python'},
                {'label': 'Ruby  ', 'value': 'Ruby'},
                {'label': 'SQL  ', 'value': 'SQL'},
                {'label': 'Java  ', 'value': 'Java'},
                {'label': 'PHP  ', 'value': 'PHP'},
                {'label': 'C  ', 'value': 'C'},
                {'label': 'TypeScript  ', 'value': 'TypeScript'},
                {'label': 'Bash/Shell/PowerShell  ', 'value': 'Bash/Shell/PowerShell'},
                {'label': 'Kotlin  ', 'value': 'Kotlin'},
                {'label': 'R  ', 'value': 'R'},
                {'label': 'VBA  ', 'value': 'VBA'},
                {'label': 'Perl  ', 'value': 'Perl'},
                {'label': 'Scala  ', 'value': 'Scala'},
                {'label': 'C++  ', 'value': 'C++'},
                {'label': 'Go  ', 'value': 'Go'},
                {'label': 'Haskell  ', 'value': 'Haskell'},
                {'label': 'Rust  ', 'value': 'Rust'},
                {'label': 'Dart  ', 'value': 'Dart'},
                {'label': 'Julia  ', 'value': 'Julia'},
                {'label': 'Assembly  ', 'value': 'Assembly'},
            ]
        ),
        dcc.Markdown('### What databases do yo utilize professionally?'),
        dcc.Checklist(
            id='DatabaseWorkedWith',
            options=[
                {'label': 'Elasticsearch  ', 'value': 'Elasticsearch'},
                {'label': 'Microsoft SQL Server  ', 'value': 'Microsoft SQL Server'},
                {'label': 'Oracle  ', 'value': 'Oracle'},
                {'label': 'MySQL  ', 'value': 'MySQL'},
                {'label': 'PostgreSQL  ', 'value': 'PostgreSQL'},
                {'label': 'Redis  ', 'value': 'Redis'},
                {'label': 'SQLite  ', 'value': 'SQLite'},
                {'label': 'MariaDB  ', 'value': 'MariaDB'},
                {'label': 'Firebase  ', 'value': 'Firebase'},
                {'label': 'MongoDB  ', 'value': 'MongoDB'},
                {'label': 'IBM DB2  ', 'value': 'IBM DB2'},
                {'label': 'DynamoDB  ', 'value': 'DynamoDB'},
                {'label': 'Cassandra  ', 'value': 'Cassandra'},
                {'label': 'Couchbase  ', 'value': 'Couchbase'},
            ]
        ),
        dcc.Markdown('### What webframes do you utilize professionally?'),
        dcc.Checklist(
            id='WebframeWorkedWith',
            options=[
                {'label': 'ASP.NET  ', 'value': 'ASP.NET'},
                {'label': 'ASP.NET Core  ', 'value': 'ASP.NET Core'},
                {'label': 'Ruby on Rails  ', 'value': 'Ruby on Rails'},
                {'label': 'Flask  ', 'value': 'Flask'},
                {'label': 'jQuery  ', 'value': 'jQuery'},
                {'label': 'Angular  ', 'value': 'Angular'},
                {'label': 'Angular.js  ', 'value': 'Angular.js'},
                {'label': 'Django  ', 'value': 'Django'},
                {'label': 'React.js  ', 'value': 'React.js'},
                {'label': 'Vue.js  ', 'value': 'Vue.js'},
                {'label': 'Gatsby  ', 'value': 'Gatsby'},
                {'label': 'Spring  ', 'value': 'Spring'},
                {'label': 'Express  ', 'value': 'Express'},
                {'label': 'Symfony  ', 'value': 'Symfony'},
                {'label': 'Laravel  ', 'value': 'Laravel'},
                {'label': 'Drupal  ', 'value': 'Drupal'},
            ]
        ),
        dcc.Markdown('### What platforms you you utilize professionally?'),
        dcc.Checklist(
            id='PlatformWorkedWith',
            options=[
                {'label': 'Windows  ', 'value': 'Windows'},
                {'label': 'iOS  ', 'value': 'iOS'},
                {'label': 'AWS  ', 'value': 'AWS'},
                {'label': 'Docker  ', 'value': 'Docker'},
                {'label': 'Linux  ', 'value': 'Linux'},
                {'label': 'MacOS  ', 'value': 'MacOS'},
                {'label': 'Android  ', 'value': 'Android'},
                {'label': 'WordPress  ', 'value': 'WordPress'},
                {'label': 'Raspberry Pi  ', 'value': 'Raspberry Pi'},
                {'label': 'Heroku  ', 'value': 'Heroku'},
                {'label': 'Google Cloud Platform  ', 'value': 'Google Cloud Platform'},
                {'label': 'Kubernetes  ', 'value': 'Kubernetes'},
                {'label': 'Arduino  ', 'value': 'Arduino'},
                {'label': 'Slack Apps and Integrations  ', 'value': 'Slack Apps and Integrations'},
                {'label': 'Microsoft Azure  ', 'value': 'Microsoft Azure'},
                {'label': 'IBM Cloud or Watson  ', 'value': 'IBM Cloud or Watson'},
            ]
        ),
        dcc.Markdown('### Do you utilize any of these misc. technologies?'),
        dcc.Checklist(
            id='MiscTechWorkedWith',
            options=[
                {'label': '.NET  ', 'value': '.NET'},
                {'label': '.NET Core  ', 'value': '.NET Core'},
                {'label': 'React Native  ', 'value': 'React Native'},
                {'label': 'Ansible  ', 'value': 'Ansible'},
                {'label': 'Pandas  ', 'value': 'Pandas'},
                {'label': 'Node.js  ', 'value': 'Node.js'},
                {'label': 'Unity 3D  ', 'value': 'Unity 3D'},
                {'label': 'TensorFlow  ', 'value': 'TensorFlow'},
                {'label': 'Torch/PyTorch  ', 'value': 'Torch/PyTorch'},
                {'label': 'Teraform  ', 'value': 'Teraform'},
                {'label': 'Unreal Engine  ', 'value': 'Unreal Engine'},
                {'label': 'Hadoop  ', 'value': 'Hadoop'},
                {'label': 'Flutter  ', 'value': 'Flutter'},
                {'label': 'Cordova  ', 'value': 'Cordova'},
                {'label': 'Xamarin  ', 'value': 'Xamarin'},
                {'label': 'Keras  ', 'value': 'Keras'},
                {'label': 'Chef  ', 'value': 'Chef'},
                {'label': 'Apache Spark  ', 'value': 'Apache Spark'},
                {'label': 'Puppet  ', 'value': 'Puppet'},
            ]
        ),
        dcc.Markdown('### Do you utilize any of these colab. tools?'),
        dcc.Checklist(
            id='NEWCollabToolsWorkedWith',
            options=[
                {'label': 'Confluence  ', 'value': 'Confluence'},
                {'label': 'Jira  ', 'value': 'Jira'},
                {'label': 'Slack  ', 'value': 'Slack'},
                {'label': 'Microsoft Azure  ', 'value': 'Microsoft Azure'},
                {'label': 'Trello  ', 'value': 'Trello'},
                {'label': 'Github  ', 'value': 'Github'},
                {'label': 'Gitlab  ', 'value': 'Gitlab'},
                {'label': 'Google Suite (Docs, Meet, etc)  ', 'value': 'Google Suite (Docs, Meet, etc)'},
                {'label': 'Microsoft Teams  ', 'value': 'Microsoft Teams'},
                {'label': 'Stack Overflow for Teams  ', 'value': 'Stack Overflow for Teams'},
                {'label': 'Facebook Workplace  ', 'value': 'Facebook Workplace'},
            ]
        ),
        dcc.Markdown('### What is your ethnicity?'),
        dcc.Checklist(
            id='Ethnicity',
            options=[
                {'label': 'White or of European descent  ', 'value': 'White or of European descent'},
                {'label': 'Hispanic or Latino/a/x  ', 'value': 'Hispanic or Latino/a/x'},
                {'label': 'East Asian  ', 'value': 'East Asian'},
                {'label': 'Black or of African descent  ', 'value': 'Black or of African descent'},
                {'label': 'Middle Eastern  ', 'value': 'Middle Eastern'},
                {'label': 'Indigenous (such as Native American, Pacific Islander, or Indigenous Australian)  ', 'value': 'Indigenous (such as Native American, Pacific Islander, or Indigenous Australian)'},
                {'label': 'South Asian  ', 'value': 'South Asian'},
                {'label': 'Multiracial  ', 'value': 'Multiracial'},
                {'label': 'Biracial  ', 'value': 'Biracial'},
                {'label': 'Southeast Asian  ', 'value': 'Southeast Asian'},
            ]
        ),

    ]
)

layout = dbc.Row([column1, column2])