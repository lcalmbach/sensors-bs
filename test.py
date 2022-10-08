import streamlit as st
import pandas as pd
import numpy as np
import math


# https://www.geeksforgeeks.org/write-custom-aggregation-function-in-pandas/

def decibel_mean(df):
    # lm = 10 * log[1/n * sum(10^ (0.1*Li)) ]
    #return 10 * math.log10(1/len(df) * 10 ^ (0.1 * df['pegel']))
    return 10 * math.log10( 1 / len(df) * ((10 ** (df['pegel'] * 0.1)).sum() ))


data = pd.DataFrame([
        {'station': 'A', 'pegel':60}, {'station': 'A', 'pegel': 50},
        {'station': 'B', 'pegel':60}, {'station': 'B', 'pegel': 100},
        {'station': 'B', 'pegel':10}, {'station': 'B', 'pegel': 1},
        ])


test = data.groupby(['station']).apply(decibel_mean)
st.write(test)