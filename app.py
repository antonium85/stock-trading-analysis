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
    ss = StockSymbol(api_key)
    list_spx = ss.get_symbol_list(index="SPX",symbols_only=True)
    list_cac40 = ss.get_symbol_list(index="PX1",symbols_only=True)

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
                    ['SPX500', 'CAC40'])

    if 'SPX500' in options:
        symbols = st.sidebar.multiselect('Select a company',list_spx)

        df = pd.read_csv(current_dir+'spx500_short_term_strat.csv',index_col='ticker')

        with st.container():
            # Create a section for the dataframe header
            st.header('Recommendation for SPX500 companies')
            
            if not symbols :
                st.write(df)
            else:
                st.write(df.loc[df.index.isin(symbols)])

    if 'CAC40' in options:
        symbols = st.sidebar.multiselect('Select a company',list_cac40)

        df = pd.read_csv(current_dir+'cac40_short_term_strat.csv',index_col='ticker')

        with st.container():
            # Create a section for the dataframe header
            st.header('Recommendation for CAC40 companies')
            if not symbols :
                st.write(df)
            else:
                st.write(df.loc[df.index.isin(symbols)])

if __name__ == '__main__':
    main()