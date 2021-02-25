import pandas as pd
import cufflinks
import plotly.express as px
import dash_trich_components as dtc
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
from app import app
from datetime import datetime, timezone


df = pd.read_csv('data/new.csv')
data = pd.read_csv('data/dataset.csv')
gross = pd.read_csv('data/gross.csv')
now = datetime.now(timezone.utc)
current_month = now.strftime('%B')
datenow = now.strftime("%d:%m:%Y")
timenow = now.strftime("%H:%M:%S")

#while:
#    timenow - now.strftime("%H:%S:%p")
available_indicators = df['Month'].unique()
available_columns = df.columns
gross_columns = gross.columns

layout = html.Div([
    dbc.Row([
        dbc.Col(
            daq.LEDDisplay(
                id='time-display',
                value=datenow,
                color='#FF5E5E',
                label='Last Updated',
                style={
                    'font-variant': 'small-caps', 'font-weight': 'bold'
                }
            ), width={'size': 6, 'offset': 3}
        )
    ], align='centre', className='row'),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[{
                            'label': i, 'value': i
                        } for i in available_columns],
                        value='Total Revenue'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={
                    'width': '48%', 'display': 'inline-block',
                    'color': 'black'
                }),
                html.Div([
                    dcc.Dropdown(
                        id='yaxis-column',
                        options=[{
                            'label': i, 'value': i
                        } for i in available_indicators],
                        value=str(current_month)
                    ),
                    dcc.RadioItems(
                        id='yaxis-type',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={
                    'width': '48%', 'display': 'inline-block',
                    'color': 'black'
                }),

                dcc.Graph(
                    id='indicator-graphic',
                    responsive=True,
                    config={
                        'displaylogo': False,
                        'showTips': True
                    }
                )
            ], style = {
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6, xs=12, sm=12, md=6
        ),
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column2',
                        options=[{
                            'label': i, 'value': i
                        } for i in available_columns],
                        value='Albayrak Share'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type2',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={
                    'width': '48%', 'display': 'inline-block',
                    'color': 'black'
                }),
                dcc.Graph(
                    id='sunburst_graphic',
                    responsive=True,
                    config={
                        'showTips': True,
                        'displaylogo': False
                    }
                )
            ], style = {
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6, xs=12, sm=12, md=6
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
                ], style={
                    'width': '48%', 'display': 'inline-block',
                    'color': 'black'
                }),
            dcc.Graph(
                id='gross-graphic',
                responsive=True,
                config={
                    'showTips': True,
                    'displaylogo': False
                }
            )
            ], style = {
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6, xs=12, sm=12, md=6
        ),
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column4',
                        options=[{
                            'label': i, 'value': i
                        } for i in available_indicators],
                        value=str(current_month)
                    ),
                    dcc.RadioItems(
                        id='xaxis-type4',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={
                    'width': '48%', 'display': 'inline-block',
                    'color': 'black'
                }),
            dcc.Graph(
                id='pie-chart',
                responsive=True,
                config={
                    'showTips': True,
                    'displaylogo': False
                }
            )
            ], style = {
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6, xs=12, sm=12, md=6
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
    clr = ['#54408c']
    fig = dff.iplot(
        asFigure=True, kind='scatter', x='Date', mode='lines+markers',
        y=xaxis_column, yTitle='Amount in USD', colors=clr,
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
    colors = ['#54408c', '#85d9e2', '#d1ba5e', '#df4bb8', '#4c72a3']
    fig = px.sunburst(
        df, path=['Year', 'Month', 'Day'], values=xaxis_column,
        color=xaxis_column, color_continuous_scale=colors,
        template='seaborn'
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})
    
    return fig


@app.callback(
    Output('gross-graphic', 'figure'),
    Input('xaxis-column3', 'value'),
    Input('xaxis-type3', 'value'))
def update_graph_one(xaxis_column, xaxis_type):
    fig = gross.iplot(
        asFigure=True, kind='bar', y=xaxis_column, barmode='overlay',
        x='Month', xTitle='Amount in USD', yTitle='2018',
        colorscale='prgn', theme='white', gridcolor='white', orientation='h'
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})
    
    return fig


@app.callback(
    Output('pie-chart', 'figure'),
    Input('xaxis-column4', 'value'),
    Input('xaxis-type4', 'value'))
def update_graph_two(xaxis_column, xaxis_type):
    dts = data[data['Month'] == xaxis_column]
    ss = dts['Month'].unique()
    colors = ['#7EAFED', '#6192BA', '#2D2F89', '#465DAB', '#1E1F2E']
    fig = dts.iplot(
        asFigure=True, kind='pie', labels='Element', values='Amount in USD',
        hole=0.5, pull=0.02, textposition='inside', colors=colors,
        linecolor='black', theme='white', textinfo='percent', sort=False
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})
    
    return fig

