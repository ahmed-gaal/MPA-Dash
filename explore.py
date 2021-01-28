import pandas as pd
import cufflinks
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

df = pd.read_csv('new.csv')
gross = pd.read_csv('gross.csv')

available_indicators = df['Month'].unique()
available_columns = df.columns
gross_columns = gross.columns

layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[{
                            'label': i, 'value': i
                        } for i in available_columns],
                        value='Total_Revenue'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Dropdown(
                        id='yaxis-column',
                        options=[{
                            'label': i, 'value': i
                        } for i in available_indicators],
                        value='Month'
                    ),
                    dcc.RadioItems(
                        id='yaxis-type',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),

                dcc.Graph(
                    id='indicator-graphic',
                    config={
                        'displaylogo': False,
                        'showTips': True
                    }
                )
            ]), width=6
        ),
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column2',
                        options=[{
                            'label': i, 'value': i
                        } for i in available_columns],
                        value='Albayrak_Share'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type2',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(
                    id='sunburst_graphic',
                    config={
                        'showTips': True,
                        'displaylogo': False
                    }
                )
            ]), width=6
        )
    ], className='row'),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column3',
                        options=[{
                            'label': i, 'value': i
                        } for i in gross_columns],
                        value='Service Revenue'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type3',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(
                id='gross-graphic',
                config={
                    'showTips': True,
                    'displaylogo': False
                }
            )
            ]), width=6
        ),
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column4',
                        options=[{
                            'label': i, 'value': i
                        } for i in gross_columns],
                        value='Net Revenue'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type4',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(
                id='pie-chart',
                config={
                    'showTips': True,
                    'displaylogo': False
                }
            )
            ]), width=6
        )
    ])
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'))
def update_graph(xaxis_column, yaxis_column, xaxis_type):
    dff = df[df['Month'] == yaxis_column]
    fig = dff.iplot(
        asFigure=True, kind='bar', x='Date', barmode='stack',
        y=xaxis_column, yTitle='Amount in USD', colorscale='piyg',
        interpolation='spline', subplots=True, subplot_titles=True,
        theme='white', gridcolor='white'
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})

    return fig


@app.callback(
    Output('sunburst_graphic', 'figure'),
    Input('xaxis-column2', 'value'),
    Input('xaxis-type2', 'value')
)
def sunburst_graph(xaxis_column, xaxis_type):
    fig = px.sunburst(
        df, path=['Year', 'Month', 'Day'], values=xaxis_column,
        color=xaxis_column, color_continuous_scale='RdBu'
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})
    
    return fig


@app.callback(
    Output('gross-graphic', 'figure'),
    Input('xaxis-column3', 'value'),
    Input('xaxis-type3', 'value'))
def update_graph_one(xaxis_column, xaxis_type):
    fig = gross.iplot(
        asFigure=True, kind='scatter', x='Month', mode='lines+markers',
        y=xaxis_column, xTitle='2018', yTitle='Amount in USD',
        colorscale='prgn', subplots=True, subplot_titles=True, theme='white',
        gridcolor='white', interpolation='spline'
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})
    
    return fig


@app.callback(
    Output('pie-chart', 'figure'),
    Input('xaxis-column4', 'value'),
    Input('xaxis-type4', 'value'))
def update_graph_two(xaxis_column, xaxis_type):
    fig = gross.iplot(
        asFigure=True, kind='pie', labels='Month', barmode='overlay',
        values=xaxis_column, hole=0.4, pull=0.05, textposition='outside',
        colorscale='rdylbu',linecolor='black', theme='white',
        textinfo='label+percent', sort=False
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})
    
    return fig