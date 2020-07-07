# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
from datetime import datetime, timedelta
import time
from time import gmtime, strftime
import cufflinks as cf
import plotly.express as px
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

full_df = pd.read_csv('final_with_companies.csv')
full_df['link'] = '<a href="'+full_df['Url']+'">'+full_df['Title']+'</a>'
companies = pd.read_csv('company_date_polarity_2.csv')
companies_list = ['Facebook', 'Google', 'Amazon', 'Apple', 'Samsung', 'Microsoft','Sony', 'Huawei']
companies = companies[companies['company'].isin(companies_list)]
companies['total']=companies['negative']+companies['neutral']+companies['positive']



def get_week(x):
    dt = time.strptime(x[0:10], '%Y-%m-%d')
    return strftime("%Y week#%U", dt)
full_df['week']=full_df['Date'].apply(get_week)
companies['week']=companies['date'].apply(get_week)
#topic_labeled['week']=topic_labeled['Date'].apply(get_week)


app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = html.Div([ html.H1("Dashboard of Sentiment about Artificial Intelligence in Mainstream Media project", style={'textAlign': 'center'}),


                        html.H2('Polarity distribution',
                               style={
                                      'textAlign': 'center'}),
                       dcc.Graph(
                    id='1-graph',
        figure=go.Figure(
    data=[
    {'x':full_df.groupby(['week','Polarity_predict']).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[-1].index.values.tolist(),
    'y': full_df.groupby(['week','Polarity_predict']).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[-1].tolist(),
    'name': 'negative',
     'mode':'lines',
    'line':dict(width=0.5, color='rgb(111, 231, 219)'),
    'stackgroup':'one'
    },
    {'x':full_df.groupby(['week','Polarity_predict']).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[1].index.values.tolist(),
    'y': full_df.groupby(['week','Polarity_predict']).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[1].tolist(),
    'name': 'positive',
    'mode':'lines',
    'line':dict(width=0.5, color='rgb(127, 166, 238)'),
    'stackgroup':'one'},
    {'x':full_df.groupby(['week','Polarity_predict']).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[0].index.values.tolist(),
    'y': full_df.groupby(['week','Polarity_predict']).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[0].tolist(),
    'name': 'neutral',
    'mode':'lines',
    'line':dict(width=0.5, color='rgb(131, 90, 241)'),
    'stackgroup':'one'}
    ],
    layout=go.Layout(template = 'plotly_dark')
)


    ),


html.H2("List of articles selected by week and polarity", style={'textAlign': "center", 'padding-top': 5}),

     html.Div([ 
         dcc.Dropdown(id="select-date", value='2019 week#51', style={'backgroundColor': 'black', 'color': 'black'},
                        options=[{'label': '2019 week#50', 'value': '2019 week#50'}, {'label': '2019 week#51', 'value': '2019 week#51'},
                        {'label': '2019 week#52', 'value': '2019 week#52'}, {'label': '2020 week#00', 'value': '2020 week#00'},
                        {'label': '2020 week#01', 'value': '2020 week#01'}, {'label': '2020 week#02', 'value': '2020 week#02'},
                        {'label': '2020 week#03', 'value': '2020 week#03'}], )],
         style={'textAlign': "center", }),

     html.Div([ 
         dcc.Dropdown(id="select-polarity", value=1, style={'backgroundColor': 'black', 'color': 'black'},
                        options=[{'label': 'positive', 'value': 1}, {'label': 'negative', 'value': -1},
                        {'label': 'neutral', 'value': 0}], )],
         style={'textAlign': "center", }),
                       

html.Div([dcc.Graph(id="datatable")]),


                        html.H2('Number of articles by each topic',
                               style={
                                      'textAlign': 'center'}),
                       dcc.Graph(
                    id='theme-graph',
        figure=go.Figure(
    data=[
    {'x':full_df.groupby('Dominant_Topic').size().sort_values(ascending=False).index.values.tolist(),
    'y': full_df.groupby('Dominant_Topic').size().sort_values(ascending=False).tolist(), 'type': 'bar',
    'marker': {'color': full_df.groupby('Dominant_Topic').size().sort_values(ascending=False).tolist(), 'colorscale': 'Viridis'}}],
    layout=go.Layout(template = 'plotly_dark')
),



    ),

                       html.H2('Topic distribution during the time',
                               style={
                                      'textAlign': 'center'}),
                       dcc.Graph(
                    id='theme-graph-time',
        figure=px.area(full_df.groupby(['week','Dominant_Topic',]).size().groupby(level=0).apply(lambda x: x / float(x.sum())).to_frame().reset_index(), x="week", y=0, color="Dominant_Topic",line_group="Dominant_Topic", color_discrete_sequence=px.colors.sequential.Plasma_r, template = 'plotly_dark')


    ),


                        html.H2("Average positiveness of each topic during the time", style={'textAlign': "center", 'padding-top': 5}),
     html.Div([ 
         dcc.Dropdown(id="select-topic", value='mobile app', style={'backgroundColor': 'black', 'color': 'black'},
                        options=[{'label': 'mobile app', 'value': 'mobile app'}, {'label': 'technology', 'value': 'technology'},
                         {'label': 'social media', 'value': 'social media'}, {'label': 'China', 'value': 'China'},
                       {'label': 'market', 'value': 'market' }, {'label': 'president Trump', 'value': 'president Trump'},
                       {'label': 'human knowledge', 'value': 'human knowledge' }, 
                       {'label': 'facial recognition', 'value': 'facial recognition' }, {'label': 'future', 'value': 'future' },
                       {'label': 'climate change', 'value': 'climate change' }, {'label': 'car driving', 'value':'car driving'  },
                       {'label': 'cloud computing' , 'value': 'cloud computing' } ,{'label': 'pets', 'value':  'pets'} , 
                       {'label': 'university', 'value':  'university'} , {'label': 'bussiness', 'value': 'bussiness' },
                       {'label': 'American presidency', 'value': 'american presidency' }, {'label':'machine learning' , 'value': 'machine learning' },
                       {'label': 'Apple', 'value': 'apple' }], )],
         style={'textAlign': "center", }),
     html.Div([html.Div([dcc.Graph(id="topic-graph", clear_on_unhover=True, )]), ]),

                       html.H2('Number of articles of different polarity by each company',
                               style={
                                      'textAlign': 'center'}),
                       dcc.Graph(
                    id='company-graph',
        figure = go.Figure(
    data=[
    {'x':companies.groupby('company').sum().index.values.tolist(),
    'y': companies.groupby('company').sum()['negative'].tolist(),
    'name': 'negative',
     'type': 'bar'
    },
    {'x':companies.groupby('company').sum().index.values.tolist(),
    'y': companies.groupby('company').sum()['positive'].tolist(),
     'type': 'bar',
    'name': 'positive'
    },
    {'x':companies.groupby('company').sum().index.values.tolist(),
    'y': companies.groupby('company').sum()['neutral'].tolist(),
     'type': 'bar',
    'name': 'neutral'
    }
    ],
    layout=go.Layout(template = 'plotly_dark', barmode= 'stack', xaxis={'categoryorder':'total descending'})
)

    ), 
                        html.H2("Percentage of articles containing name of company", style={'textAlign': "center", 'padding-top': 5}),
     html.Div([
         dcc.Dropdown(id="select-company", value="Facebook", style={'backgroundColor': 'black', 'color': 'black'},
                        options=[{'label': "Facebook", 'value': "Facebook"}, {'label': "Apple", 'value': "Apple"},
                         {'label': "Amazon", 'value': "Amazon"}, 
                        {'label': "Google", 'value': "Google"}, {'label': "Microsoft", 'value': "Microsoft"},
                        {'label': 'Samsung' , 'value': 'Samsung'}, {'label': 'Sony', 'value': 'Sony'}, 
                        {'label': 'Huawei', 'value': 'Huawei'}], )],
         style={'textAlign': "center", }),
     html.Div([html.Div([dcc.Graph(id="companies-graph", clear_on_unhover=True, )]), ]),


                        html.H2('Average positiveness of each source of media',
                               style={
                                      'textAlign': 'center'}),
                       dcc.Graph(
                    id='positiveness-graph',
        figure=go.Figure(
    data=[
    {'x':full_df[['Source', 'Polarity_predict']].groupby('Source').mean().sort_values(by='Polarity_predict', ascending = False).index.values.tolist(),
    'y': full_df[['Source', 'Polarity_predict']].groupby('Source').mean().sort_values(by='Polarity_predict', ascending = False)['Polarity_predict'].tolist(),
    'type':'bar',
    'marker': {'color': full_df[['Source', 'Polarity_predict']].groupby('Source').mean().sort_values(by='Polarity_predict', ascending = False)['Polarity_predict'].tolist(), 'colorscale': 'Viridis'}}],
    layout=go.Layout(template = 'plotly_dark')
)


    )

                    


                            ],
    className="dash-bootstrap"
                         )


@app.callback(
    dash.dependencies.Output("companies-graph", "figure"),
    [dash.dependencies.Input("select-company", "value"),])
def update_graph(selected):

    trace =  {'x':full_df.groupby(['week',selected]).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[1].index.values.tolist(),
    'y': full_df.groupby(['week',selected]).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)[1].tolist(),
    'name': selected}

    layout = go.Layout(template = 'plotly_dark')
    figure2 = {"data": [trace], "layout": layout}

    return figure2

@app.callback(
    dash.dependencies.Output("topic-graph", "figure"),
    [dash.dependencies.Input("select-topic", "value"),])
def update_graph(selected):

    trace =  {'x':full_df[full_df['Dominant_Topic'] == selected][['week','Polarity_predict']].groupby(['week']).mean()['Polarity_predict'].index.values.tolist(),
    'y': full_df[full_df['Dominant_Topic'] == selected][['week','Polarity_predict']].groupby(['week']).mean()['Polarity_predict'].tolist(),
    'name': selected}

    layout = go.Layout(template = 'plotly_dark', yaxis=dict(zeroline=True, zerolinewidth=1, zerolinecolor='Red'))
    figure2 = {"data": [trace], "layout": layout}

    return figure2


@app.callback(
    dash.dependencies.Output("datatable", "figure"),
    [dash.dependencies.Input("select-date", "value"),
    dash.dependencies.Input("select-polarity", "value") ])
def update_datatable2(selected, selected_pol):
    data2=[go.Table(
    header=dict(values=['Article'],
                align='left',
                fill_color='black',
    font=dict(color='white', size=12)),
    cells=dict(values=[full_df[(full_df['Polarity_predict']==selected_pol )& (full_df['week']==selected)].link],
               align='left',
               fill_color='white',
    font=dict(color='white', size=12)))]
    return go.Figure(data=data2, layout=go.Layout(template = 'plotly_dark'))

if __name__ == '__main__':
    app.run_server(debug=True)
