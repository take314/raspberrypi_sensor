import streamlit as st
import io
import sys
import json
import argparse
import pandas as pd
import datetime
import plotly


st.set_page_config(
     page_title='Raspberry-pi Sensor Monitor',
     layout="wide",
     initial_sidebar_state="expanded",
)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('mapbox_token', help='input mapbox token')
    # parser.add_argument('--input', help='mizzy input json')
    # args = parser.parse_args()
    current_date = datetime.datetime.now().split('0')[0]
    df = pd.read_csv(f'{current_date}.csv')
    st.header(f'CO2 (ppm) @{current_date}')
    st.line_chart(df)
