import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from copy import deepcopy

# st.text("I changed smth")

# mpg_df = pd.read_csv("./data/raw/mpg.csv")
# mpg_df

@st.cache_data # decorator
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path="./data/raw/mpg.csv") # for speed
mpg_df = deepcopy(mpg_df_raw) # for security

st.title('My 1st version')
st.header('MPG data exploration')

if st.sidebar.checkbox("Show dataframe:"):
    st.dataframe(data=mpg_df)

left_column, middle_column, right_column = st.columns([3, 1, 1])

show_means = middle_column.radio(
    'Show Class Means', ['Yes', 'No'])

years = ["All"]+sorted(pd.unique(mpg_df['year']))
year = left_column.selectbox("Choose a year", years)
if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose a plot type", plot_types)

# matplotlib
m_fig, ax = plt.subplots(figsize=(10,8))
ax.scatter(reduced_df["displ"], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7,
               color="red", label="Class Means")

# st.pyplot(fig=m_fig)

# plotly
p_fig = px.scatter(
    reduced_df,
    x="displ",
    y="hwy",
    opacity=0.7,
    range_y=[10,50],
    width=750,
    height=600,
    labels={
        "displ": "Displacement (lt)",
        "hwy": "MPG"
    },
    title= "Engine Size vs Highway Fuel Mileage"
)
p_fig.update_layout(title_font_size=22)

# st.plotly_chart(p_fig)

if plot_type == "Matplotlib":
    st.pyplot(fig=m_fig)
else:
    st.plotly_chart(p_fig)

ds_geo = px.data.carshare()
# ds_geo["lat"] = 

st.map(ds_geo, latitude="centroid_lat", longitude="centroid_lon")

st.dataframe(ds_geo.head())

url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)