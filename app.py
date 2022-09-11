import pandas as pd
import pickle
from PIL import Image
import streamlit as st
import plotly.express as px

# tema dasar
px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'reds'

# menampilkan gambar di sidebar
img = Image.open('assets/5.png')
st.sidebar.image(img)

# buka file
with open('clear_data.pickle', 'rb') as f:
    data = pickle.load(f)

# input tgl berdasarkan data
min_date = data['trending_date'].min()
max_date = data['trending_date'].max()
start_date, end_date = st.sidebar.date_input(label='Rentang Waktu',
                                             min_value=min_date,
                                             max_value=max_date,
                                             value=[min_date, max_date])  # nilai default jika belum memilih

# input kategory
# categories = ["All Categories"] + list(data["category"].value_counts().keys())
# st.sidebar.selectbox(label="Kategori", options=categories)

# filter
outputs = data[(data['trending_date'] >= start_date) &
               (data['trending_date'] <= end_date)]
# if category != "All Categories":      #filter tambahan jika tidak memilih all category
# outputs = outputs[outputs['category'] == category  #outpus sebelumnya dan kategory tertentu

# visualisasi barchart
st.header(':video_camera: Channel')
bar_data = outputs['channel_name'].value_counts().nlargest(10).sort_values()
fig = px.bar(bar_data, color=bar_data, orientation='h',
             title=f'Channel Terpopuler')
st.plotly_chart(fig)

# input scatterplot
st.header(':bulb: Engagement')
col1, col2 = st.columns(2)
metric_choice = ['like', 'dislike', 'comment']
choice_1 = col1.selectbox('Horisontal', options=metric_choice)
choice_2 = col2.selectbox('Vertical', options=metric_choice)

# visualiasi scatterplot
fig = px.scatter(outputs,
                 x=choice_1,
                 y=choice_2,
                 size='view',
                 hover_name='channel_name',
                 hover_data=['title'],
                 title=f'Engagement of {choice_1.title()} and {choice_2.title()}'
                 )
st.plotly_chart(fig)
