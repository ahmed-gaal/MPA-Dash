import pandas as pd
import cufflinks
import plotly.express as px
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from datetime import datetime

df = pd.read_csv('data/new.csv')
data = pd.read_csv('data/dataset.csv')
ves = pd.read_csv('data/ves.csv')
gross = pd.read_csv('data/gross.csv')
now = datetime.now()
current_month = now.strftime('%B')
current_day = now.strftime('%A')
current_year = now.strftime('%Y')
datenow = now.strftime("%d:%m:%Y")
colors=['#8798BF', '#2A3E5D']
ves['Month'] = pd.DatetimeIndex(ves['Date']).month_name()
ves["Day"] = pd.DatetimeIndex(ves['Date']).day

fig1 = ves.iplot(
    asFigure=True, kind='barh', x='Month', y='Vessels', xTitle='2018',
    yTitle='Number of Vessels', colorscale='piyg', theme='polar',
    title='Vessels docked at the Port of Mogadishu'
)
fig2 = ves.iplot(
    asFigure=True, kind='pie', labels='CTU', hole=0.5, pull=0.02,
    values='Quantity', colors=colors,
    title='Cargo Transport Units that passed through the Port in 2018'
)
fig3=go.Figure()

fig3.add_trace(go.Indicator(
    mode = "number+delta",
    value = gross['Tax Revenue'].sum(),
    title = {
        "text": "Tax<br><span style='font-size\
                :0.8em;color:gray'>Revenue</span><br><span style='font-size\
                :0.8em;color:gray'>Collected</span>"
    },
    delta = {
        'reference': gross['Tax Revenue'].sum(),\
            'relative': True
    },
    domain = {'x': [0, 0.5], 'y': [0.5, 0]}))

fig3.add_trace(go.Indicator(
    mode = "number+delta",
    value = gross['Net Revenue'].sum(),
    title = {
        "text": "Net<br><span style='font-size:0.8em;\
                color:gray'>Revenue</span><br><span style='font-size\
                :0.8em;color:gray'>Collected</span>"
    },
    delta = {
        'reference': gross['Service Revenue'].sum(),\
            'relative': True
    },
    domain = {'x': [0.5, 1], 'y': [0, 1]}))

fig3.add_trace(go.Indicator(
    mode = "number+delta",
    value = gross['Albayrak Share'].sum(),
    title = {
        "text": "Albayrak<br><span style='font-size:0.8em\
                ;color:gray'>Gross</span><br><span style='font-size:0.8em\
                ;color:gray'>Revenue</span>"
    },
    delta = {
        'reference': gross['Albayrak Share'].sum(),
            'relative': True
    },
    domain = {'x': [0.5, 0], 'y': [1, 0.5]}))


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
                dbc.CardHeader("Vessels Docked at the Port of Mogadishu."),
                dbc.CardBody([
                    dcc.Graph(
                        id='no_vessels',
                        figure=fig1,
                        responsive=True,
                        config={
                            'showTips': True,
                            'displaylogo': False
                        }
                    )
                ])
            ], style={
                'font-variant': 'small-caps', 'font-weight': 'bold'
                }), width=6, xs=12, sm=12, md=6
        ),
        dbc.Col(
            html.Div([
                dbc.CardHeader("Cargo Transport Units in Port of Mogadishu."),
                dbc.CardBody([
                    dcc.Graph(
                        id='no_ctu',
                        figure=fig2,
                        responsive=True,
                        config={
                            'showTips': True,
                            'displaylogo': False
                        }
                    )
                ])
            ], style={
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6, xs=12, sm=12, md=6
        )
    ], className='row'),
    dbc.Row(
        dbc.Col(
            html.Div([
                dcc.Graph(
                    id='indicator',
                    figure=fig3,
                    responsive=True,
                    config={
                        'showTips': True,
                        'displaylogo': False
                    }
                )
            ], style={
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=12, xs=12, sm=12, md=12
        ), className='row'
    )
])