#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import *

import warnings
warnings.filterwarnings('ignore')

def main():
    current_dir = get_current_dir()

    # get spx list
    list_spx = pd.read_csv(current_dir+'markets/SPX500.csv')

    # get spf120 list
    list_spf120 = pd.read_csv(current_dir+'markets/SPF120.csv')

    # Add a title and intro text
    st.title('💸 What should you do last 7 days ?')
    st.info('This web app will give you advice',icon='ℹ️')

    st.sidebar.title('Parameters')

    # Using "with" notation
    with st.sidebar:
        add_radio = st.radio(
            "Choose a strategy",
            ("Short-term (12-26 days)", "Mid-term (50-100 days)", "Long-term (100-200 days)")
        )

        options = st.multiselect(
                    'Select market',
                    ['SPX500', 'SPF120'])

    if 'SPX500' in options:
        if add_radio == 'Short-term (12-26 days)' :
            df = pd.read_csv(current_dir+'spx500_short_term_strat.csv',index_col='ticker')
        elif add_radio == 'Mid-term (50-100 days)' :
            df = pd.read_csv(current_dir+'spx500_mid_term_strat.csv',index_col='ticker')
        elif add_radio == 'Long-term (100-200 days)' :
            df = pd.read_csv(current_dir+'spx500_long_term_strat.csv',index_col='ticker')

        with st.container():
            # Create a section for the dataframe header
            st.header('🇺🇸 Recommendation for SPX500 companies')

            symbols = st.multiselect('Select SP500 companies',list_spx[['symbol']])
            
            if not symbols :
                st.write(df.sort_values(by='date',ascending=False))
            else:
                st.write(df.loc[df.index.isin(symbols)])

    if 'SPF120' in options:
        if add_radio == 'Short-term (12-26 days)' :
            df = pd.read_csv(current_dir+'spf120_short_term_strat.csv',index_col='ticker')
        elif add_radio == 'Mid-term (50-100 days)' :
            df = pd.read_csv(current_dir+'spf120_mid_term_strat.csv',index_col='ticker')
        elif add_radio == 'Long-term (100-200 days)' :
            df = pd.read_csv(current_dir+'spf120_long_term_strat.csv',index_col='ticker')

        with st.container():
            # Create a section for the dataframe header
            st.header('🇫🇷 Recommendation for SPF120 companies')

            symbols = st.multiselect('Select SPF120 companies',list_spf120[['symbol']])

            if not symbols :
                st.write(df.sort_values(by='date',ascending=False))
            else:
                st.write(df.loc[df.index.isin(symbols)])

if __name__ == '__main__':
    main()