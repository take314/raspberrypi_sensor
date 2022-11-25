# -*- coding: utf-8 -*-

import dash
from dash import dcc, html, callback_context, no_update
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import datetime
import csv
import os
current_date = str(datetime.datetime.now()).split(' ')[0]
#path = f'{current_date}.csv'
path = f'test.csv'

last_mtime = os.stat(path).st_mtime


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
    fig.add_trace(go.Scatter(x=timestamp, y=co2_ppm, line=dict(width=3)))
    fig.update_layout(title='CO2 Monitor', xaxis_title='Date', yaxis_title='CO2 (PPM)')

    return fig


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Raspberry Pi Sensor Monitor'),
    dcc.Graph(
        id='co2-graph',
        figure=get_co2_fig()
    ),
    dcc.Interval(id='interval', interval=60000, n_intervals=0)
])


@app.callback(Output('co2-graph', 'figure'), [Input('interval', 'n_intervals')])
def trigger_by_modify(n):
    global last_mtime
    if os.stat(path).st_mtime > last_mtime:
        print("modified")
        last_mtime = os.stat(path).st_mtime
        return get_co2_fig()
    return no_update


if __name__ == '__main__':
    # `debug=True`でhot-reloadingモードを有効にし、コード上の変更を画面に反映する。
    app.run_server(debug=True, host="0.0.0.0")
