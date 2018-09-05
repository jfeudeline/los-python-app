# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import queries

app = dash.Dash()
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Hackathon Linked Open Statistics'),

    html.H2(children='Un exemple minimal avec Python'),
  

    html.Div(children='Population totale des communes'),

    html.Label('Département'),
    dcc.Dropdown(
        id = 'dep_id',
        options=queries.liste_departements(),
        value=queries.liste_departements()[0]['value']
    ),

    html.Label('Commune'),
    dcc.Dropdown(
        id = 'com_id',
        value=[],
        multi=True
    ),

    

    dcc.Graph(
        id='graphpop'
       )
])




@app.callback(
    Output(component_id='com_id', component_property='options'),
    [Input(component_id='dep_id', component_property='value')]
)
def update_liste_communes(departement):
    return queries.liste_communes(departement)


@app.callback(
    Output(component_id='graphpop', component_property='figure'),
    [Input(component_id='com_id', component_property='value')]
)
def update_data(communes):
    return {
            'data': [queries.population(codecom) for codecom in communes],
            'layout': {'title': 'Population totale'}
    }
    

if __name__ == '__main__':
    app.run_server(debug=True)