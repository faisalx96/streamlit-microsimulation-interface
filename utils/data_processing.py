import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    return pd.read_csv("data/population_composition.csv")


def filter_data(df, comb):
    return df[df['Combination'] == comb]


def get_combination(asmr, asfr):
    return f"asmr_{-asmr}_asfr_{-asfr}"


def format_number(num):
    if num >= 1e6:
        return f'{num / 1e6:.1f}M'
    elif num >= 1e3:
        return f'{num / 1e3:.0f}K'
    else:
        return f'{num:.0f}'
