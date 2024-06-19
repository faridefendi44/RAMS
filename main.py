import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

from utils import get_csv_url
from plot import plot_interactive_weibull
from data_processing import process_failure_rate, process_availability

# URL default Google Sheets
url_default = "https://docs.google.com/spreadsheets/d/1toTRK3kANu7lL7BuNcNT37H4I3ztnYNi/edit?usp=sharing&ouid=111987242205368293051&rtpof=true&sd=true"

# Input URL Google Sheets di sidebar
st.sidebar.header('URL Google Sheets')
url = st.sidebar.text_input('Masukkan URL Google Sheets:', url_default)

# Konversi URL menjadi format CSV eksport
csv_url = get_csv_url(url)

try:
    # Baca data dari Google Sheets
    data = pd.read_csv(csv_url, thousands=',', decimal='.')

    # Sidebar untuk memilih metrik
    st.sidebar.header('Pilih Metrik')
    metric = st.sidebar.radio('Metrik:', ('Failure Rate', 'Availability'))

    if metric == 'Failure Rate':
        process_failure_rate(data)
    elif metric == 'Availability':
        process_availability(data)

except Exception as e:
    st.error(f"Error reading data: {e}")