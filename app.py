# -*- coding: utf-8 -*-

import csv
import glob
import subprocess
from datetime import datetime
from itertools import zip_longest

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
    files.sort(reverse=True)
    return [f.split('/')[1].split('.')[0] for f in files]


def read_csv(path):
    with open(path) as f:
        reader = csv.reader(f, delimiter=' ')
        data = [row for row in reader]
        data_t = [list(x) for x in zip_longest(*data)]
    return data_t


def shutdown():
    subprocess.Popen(['bash', 'shutdown.sh'])


def get_co2_fig(csv_data):
    layout = go.Layout(plot_bgcolor='WhiteSmoke', paper_bgcolor='WhiteSmoke')
    fig = go.Figure(layout=layout)
    timestamp = [datetime.fromtimestamp(int(i)) for i in csv_data[0][1:]]
    co2_ppm = [int(i) if i is not None else None for i in csv_data[1][1:]]
    t_celsius = [float(i) if i is not None else None for i in csv_data[2][1:]]
    p_hpa = [float(i) if i is not None else None for i in csv_data[3][1:]]
    h_percent = [float(i) if i is not None else None for i in csv_data[4][1:]]
    fig.add_trace(go.Scatter(name='co2', x=timestamp, y=co2_ppm, line=dict(width=2, color='crimson')))
    fig.add_trace(go.Scatter(name='temp', x=timestamp, y=t_celsius, line=dict(width=2, color='royalblue'), yaxis="y2"))
    fig.add_trace(go.Scatter(name='pres', x=timestamp, y=p_hpa, line=dict(width=2, color='tomato'), yaxis="y3"))
    fig.add_trace(go.Scatter(name='humid', x=timestamp, y=h_percent, line=dict(width=2, color='teal'), yaxis="y4"))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(margin=dict(l=100, r=150, t=10, b=10), showlegend=True,
                      uirevision='true', height=300,
                      xaxis=dict(domain=[0.2, 0.8]),
                      yaxis=dict(title='CO2 (ppm)', side='left', showgrid=False,
                                  titlefont=dict(color='crimson'), tickfont=dict(color='crimson'), position=0.15),
                      yaxis2=dict(title='Temperature (℃)', side='left', showgrid=False, overlaying='y',
                                  titlefont=dict(color='royalblue'), tickfont=dict(color='royalblue'), position=0.05),
                      yaxis3=dict(title='Pressure (hPa)', side='right', showgrid=False, overlaying='y',
                                  titlefont=dict(color='tomato'), tickfont=dict(color='tomato'), position=0.85),
                      yaxis4=dict(title='Humidity (%)', side='right', showgrid=False, overlaying='y',
                                  titlefont=dict(color='teal'), tickfont=dict(color='teal'), position=0.95))
    return fig


csv_dates = get_csv_dates()
current_date = get_date()
current_csv_data = read_csv(get_path(current_date))
selected_csv_data = current_csv_data
co2_fig = get_co2_fig(current_csv_data)

app = dash.Dash(__name__)
app.title = 'Raspberry Pi Sensor Monitor'
app.layout = html.Div(children=[
    html.Br(),
    html.H3(children='Raspberry Pi Sensor Monitor', style={'fontFamily': 'Arial Black', 'fontSize': 48}),
    html.Hr(),
    html.Div(children=[
        html.Div(children=[
            html.H3(children='CO2 [ppm]', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'crimson'}),
            html.H3(id='current-co2', children=' ', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'crimson'}),
        ], style={'width': '25%', 'display': 'inline-block', 'marginLeft': 5}),
        html.Div(children=[
            html.H3(children='Temp [°C]', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'royalblue'}),
            html.H3(id='current-temp', children=' ', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'royalblue'}),
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': 5}),
        html.Div(children=[
            html.H3(children='Pres [hPa]', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'tomato'}),
            html.H3(id='current-pres', children=' ', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'tomato'}),
        ], style={'width': '25%', 'display': 'inline-block', 'marginLeft': 5}),
        html.Div(children=[
            html.H3(children='Humid [%]', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'teal'}),
            html.H3(id='current-humid', children=' ', style={'fontFamily': 'Arial Black', 'fontSize': 32, 'color': 'teal'}),
        ], style={'width': '27%', 'display': 'inline-block', 'marginLeft': 5})
    ], style={'width': '65%', 'display': 'inline-block'}),
    html.Div(children=[
        html.H6(children='last update:'),
        html.H6(id='last-update', children=' '),
    ]),
    html.Hr(),
    dcc.Graph(id='co2-graph',
              figure=co2_fig,
              config={'displayModeBar': False, 'responsive': False}),
    html.Div(children=[
        html.Div(children=[
            html.Label('Date'),
            dcc.Dropdown(csv_dates, value=current_date, id='dropdown_date', style={'textAlign': 'left'})
        ], style={'width': '25%', 'display': 'inline-block', 'marginLeft': 5})
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Hr(),
    html.Div(children=[
            html.Button('Shutdown', id='shutdown', n_clicks=0),
            html.H6(id='shutdown_message', children='', style={'fontSize': 16}),
            html.Br()]),
    html.Img(src='assets/plotly_logo.webp', alt='image', style={'width': '12%', 'marginBottom': 40}),
    dcc.Interval(id='interval', interval=60000, n_intervals=0)
], style={'textAlign': 'center', 'backgroundColor': 'WhiteSmoke', 'color': '#2F3F5C'})


@app.callback([Output('current-co2', 'children'),
               Output('current-temp', 'children'),
               Output('current-pres', 'children'),
               Output('current-humid', 'children'),
               Output('last-update', 'children'),
               Output('co2-graph', 'figure'),
               Output('dropdown_date', 'options'),
               Output('dropdown_date', 'value')],
              [Input('interval', 'n_intervals'),
               Input('dropdown_date', 'value')])
def trigger_by_interval(n, selected_date):
    global current_date, csv_dates, current_csv_data, selected_csv_data, co2_fig
    date = get_date()
    csv_dates = get_csv_dates()
    current_csv_data = read_csv(get_path(current_date))

    last_update = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    co2 = current_csv_data[1][-1]
    temp = current_csv_data[2][-1]
    pres = current_csv_data[3][-1]
    humid = current_csv_data[4][-1]

    if current_date != date:
        current_date = date
        print(f'new csv created: {get_path(current_date)}')
        co2_fig = get_co2_fig(current_csv_data)
        return co2, temp, pres, humid, last_update, co2_fig, csv_dates, current_date
    if selected_date is None or selected_date == current_date:
        print(f'selected_date: {selected_date} -> use {current_date}.csv')
        co2_fig = get_co2_fig(current_csv_data)
        return co2, temp, pres, humid, last_update, co2_fig, csv_dates, current_date
    else:
        print(f'selected_date: {selected_date}.csv exists -> use it')
        selected_csv_data = read_csv(get_path(selected_date))
        co2_fig = get_co2_fig(selected_csv_data)
        return co2, temp, pres, humid, last_update, co2_fig, csv_dates, selected_date


@app.callback(Output('shutdown_message', 'children'), Input('shutdown', 'n_clicks'))
def shutdown_button_clicked(n_clicks):
    if n_clicks > 0:
        shutdown()
        return 'shutdown signal send...'
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
