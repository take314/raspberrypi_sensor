# -*- coding: utf-8 -*-

import csv
import glob
import subprocess
from datetime import datetime

import dash
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output


def get_date():
    return str(datetime.now()).split(' ')[0]


def get_path(d):
    return f'data/{d}.csv'


def get_csv_dates():
    files = glob.glob('data/*')
    return [f.split('/')[1].split('.')[0] for f in files]


def read_csv(path):
    with open(path) as f:
        reader = csv.reader(f, delimiter=' ')
        data = [row for row in reader]
        data_t = [list(x) for x in zip(*data)]
    return data_t


def sampling():
    sample = int(subprocess.check_output(['bash', 'sampling.sh']))
    datetime_now = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    return f'CO2: {sample} ppm', f'{datetime_now}'


def shutdown():
    subprocess.Popen(['bash', 'shutdown.sh'])


def get_co2_fig(path):
    data = read_csv(path)
    layout = go.Layout(plot_bgcolor='WhiteSmoke', paper_bgcolor='WhiteSmoke')
    fig = go.Figure(layout=layout)
    timestamp = [datetime.fromtimestamp(int(i)) for i in data[0][1:]]
    co2_ppm = [int(i) for i in data[1][1:]]
    fig.add_trace(go.Scatter(x=timestamp, y=co2_ppm, line=dict(width=2, color='Crimson')))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(yaxis_title='CO2 (ppm)',
                      margin=dict(l=200, r=200, t=10, b=10), showlegend=False,
                      uirevision='true', height=300)
    return fig


graph_types = ['CO2']
current_date = get_date()
app = dash.Dash(__name__)
app.title = 'Raspberry Pi Sensor Monitor'
app.layout = html.Div(children=[
    html.Br(),
    html.H3(children='Raspberry Pi Sensor Monitor', style={'fontFamily': 'Arial Black', 'fontSize': 48}),
    html.H3(id='container-sample-main', children='', style={'fontFamily': 'Arial Black', 'fontSize': 32}),
    html.H6(id='container-sample-sub', children=''),
    html.Hr(),
    html.Div(children=[
        html.Div(children=[
                html.Label('Type'),
                dcc.Dropdown(graph_types, value=graph_types[0], id='dropdown_graphtype', style={'textAlign': 'left'})
            ], style={'width': '20%', 'display': 'inline-block', 'marginRight': 5}),
        html.Div(children=[
                html.Label('Date'),
                dcc.Dropdown(get_csv_dates(), value=current_date, id='dropdown_date', style={'textAlign': 'left'})
            ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': 5})
    ], style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(id='co2-graph',
              figure=get_co2_fig(get_path(current_date)),
              config={'displayModeBar': False, 'responsive': False}),
    html.Hr(),
    html.Div(children=[
            html.Button('Shutdown', id='shutdown', n_clicks=0),
            html.H6(id='shutdown_message', children='', style={'fontSize': 16}),
            html.Br()]),
    html.Img(src='assets/plotly_logo.webp', alt='image', style={'width': '12%', 'marginBottom': 40}),
    dcc.Interval(id='interval', interval=10000, n_intervals=0)
], style={'textAlign': 'center', 'backgroundColor': 'WhiteSmoke', 'color': '#2F3F5C'})


@app.callback([Output('container-sample-main', 'children'),
               Output('container-sample-sub', 'children'),
               Output('co2-graph', 'figure')],
              [Input('interval', 'n_intervals'),
               Input('dropdown_date', 'value')])
def trigger_by_interval(n, selected_date):
    global current_date
    date = get_date()

    if current_date != date:
        current_date = date
        print(f'new csv created: {get_path(current_date)}')

    co2_ppm, updated_time = sampling()
    if selected_date is None or selected_date == current_date:
        print(f'selected_date: {selected_date} -> use {current_date}.csv')
        return co2_ppm, updated_time, get_co2_fig(get_path(current_date))
    else:
        print(f'selected_date: {selected_date}.csv exists -> use it')
        return co2_ppm, updated_time, get_co2_fig(get_path(selected_date))


@app.callback(Output('shutdown_message', 'children'), Input('shutdown', 'n_clicks'))
def shutdown_button_clicked(n_clicks):
    if n_clicks > 0:
        shutdown()
        return 'shutdown signal send...'
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
