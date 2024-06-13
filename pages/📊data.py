import pandas as pd
import numpy as np
import streamlit as st

st.title('Data on Recycling Items')
st.subheader("This is data on waste management in Singapore")
data = pd.read_csv('pages/sgwastedata.csv')
data = pd.DataFrame(data)
data = data.dropna()
st.write(data)
