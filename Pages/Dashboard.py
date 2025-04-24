import streamlit as st
import pandas as pd
import requests
import json
import time
from datetime import datetime
import csv
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
st.markdown(
    """
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Shadows+Into+Light&display=swap" rel="stylesheet">
    </head>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
body, h1, h2, h3, h4, h5, h6, p, label, button, div, input, select, option {
    font-family: 'Shadows Into Light', cursive !important;
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
<style>
.stApp {
background-color: #A3B18A; 
}
.stButton button {
background-color: #DAD7CD;}

.stSelectbox > div > div > div {
background-color: #DAD7CD;
}

.stDateInput input {
background-color: #DAD7CD;
}
</style>
""", unsafe_allow_html=True,
)


st.markdown(
    f"<h1 style='color: #{'344E41'}'>Dashboard</h1>",
    unsafe_allow_html=True
)


dininghalls = ["Lulu", "StoneD", "Bates", "Tower"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

visited = {
    "Lulu": [4, 0, 1, 0, 1, 0, 1],
    "Bates": [8, 0, 1, 6, 0, 3, 6],
    "Tower": [5, 7, 6, 8, 3, 2, 1],
    "StoneD": [1, 2, 0, 0, 2, 8, 1],
}

df = pd.DataFrame(visited, index=days)

# Reshape the DataFrame using melt()
df_melted = df.reset_index().melt(
    id_vars='index',
    value_vars=dininghalls,
    var_name='Dining Hall',
    value_name='Visits'
)
df_melted = df_melted.rename(columns={'index': 'Day'})

color_mapping = {
    'Lulu': '#588157',
    'Bates': '#3A5A40',
    'Tower': '#344E41',
    'StoneD': '#DAD7CD'
}
df_melted['color'] = df_melted['Dining Hall'].map(color_mapping)

# Create the Altair bar chart with tooltips and background color
chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X('Day'),
    y=alt.Y('Visits'),
    color=alt.Color('Dining Hall', scale={'domain': list(color_mapping.keys()), 'range': list(color_mapping.values())}),
    tooltip=['Day', 'Dining Hall', 'Visits']  # Add tooltips
).properties(
    title="Dining Hall Visits Throughout the Week"
).configure(
    background='#A3B18A',  # Try this simpler form first
    view=alt.ViewConfig(
        #background='#A3B18A'  # If the above doesn't work, try this
    )
)

# Display the Altair chart in Streamlit
st.altair_chart(chart, use_container_width=True)
# Sample weekly data (replace with your actual data)
data = {
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'Carbs': [50, 60, 75, 55, 80, 40, 45],
    'Protein': [30, 35, 40, 32, 45, 25, 30],
    'Fats': [20, 25, 15, 22, 20, 30, 25]
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
n_days = len(df)
theta = np.linspace(0, 2 * np.pi, n_days, endpoint=False)
width = (2 * np.pi) / n_days

colors = ['#3A5A40', '#588157', '#344E41']
labels = ['Carbs', 'Protein', 'Fats']

background_color = '#A3B18A'
bottom = np.zeros(n_days)

for i, macronutrient in enumerate(['Carbs', 'Protein', 'Fats']):
    values = df[macronutrient].values
    ax.bar(theta, values, width=width, bottom=bottom, color=colors[i], label=labels[i], alpha=0.7)
    bottom += values

lines, labels = plt.thetagrids(np.degrees(theta), df['Day'])

plt.style.use('dark_background')  # Apply the dark style

# --- Override the background color here (SIMPLIFIED) ---
background_color = '#A3B18A'  # Replace with your desired color (e.g., light gray)

# 1. Set Figure Background
fig.patch.set_facecolor(background_color)
fig.patch.set_alpha(1)  # Ensure it's opaque

# 2. Set Axes Background
ax.set_facecolor(background_color)
ax.set_alpha(1) 
ax.set_title("Weekly Macronutrient Breakdown", va='bottom', y=1.05)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))


ax.set_rticks([])
ax.grid(False)

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

plt.tight_layout()
st.pyplot(fig)