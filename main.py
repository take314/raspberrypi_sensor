# -*- coding: utf-8 -*-

import csv
import datetime
import os
import subprocess

import dash
import plotly.graph_objects as go
from dash import dcc, html, no_update
from dash.dependencies import Input, Output

current_date = str(datetime.datetime.now()).split(' ')[0]
path = f'{current_date}.csv'
last_mtime = os.stat(path).st_mtime


def sampling():
    return subprocess.check_output(['bash', 'sampling.sh'])


def read_csv():
    with open(path) as f:
        reader = csv.reader(f, delimiter=' ')
        data = [row for row in reader]
        data_t = [list(x) for x in zip(*data)]
    return data_t


def get_co2_fig():
    data = read_csv()
    fig = go.Figure()
    timestamp = [datetime.datetime.fromtimestamp(int(i)) for i in data[0][1:]]
    co2_ppm = [int(i) for i in data[1][1:]]
    fig.add_trace(go.Scatter(x=timestamp, y=co2_ppm, line=dict(width=2)))
    fig.update_layout(title=dict(text='CO2 Monitor', xref='paper', xanchor='center', x=0.5),
                      xaxis_title='Date',
                      yaxis_title='CO2 (ppm)',
                      margin=dict(l=200, r=200))
    return fig


def get_sampling_values():
    sample = int(sampling())
    return f'{sample} ppm', f'{datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S")}'


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Hr(),
    html.H2(children='Raspberry Pi Sensor Monitor'),
    html.Hr(),
    html.H3(id='container-sample-main', children=''),
    html.H6(id='container-sample-sub', children=''),
    html.Hr(),
    dcc.Graph(id='co2-graph', figure=get_co2_fig()),
    dcc.Interval(id='interval', interval=10000, n_intervals=0)
], style={'textAlign': 'center'})


@app.callback([Output('container-sample-main', 'children'),
               Output('container-sample-sub', 'children'),
               Output('co2-graph', 'figure')],
              [Input('interval', 'n_intervals')])
def trigger_by_modify(n):
    co2_ppm, date = get_sampling_values()
    global last_mtime
    if os.stat(path).st_mtime > last_mtime:
        last_mtime = os.stat(path).st_mtime
        print(f'modified at {last_mtime}')
        return co2_ppm, date, get_co2_fig()
    return co2_ppm, date, no_update


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
