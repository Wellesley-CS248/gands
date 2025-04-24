import streamlit as st
import pandas as pd
import requests
import json
from datetime import date, timedelta
import random
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
} </style>
""", unsafe_allow_html=True,
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
# Your get_week_menu function
#def get_week_menu(date, locationID, mealID):
    #base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    #params = {"date": date, "locationID": locationID, "mealID": mealID}
    #result = requests.get(base_url, params=params).text
    #data = json.loads(result)
    #return pd.DataFrame(data)
def get_week_menu(date, locationID, mealID):
    base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {"date": date, "locationID": locationID, "mealID": mealID}
    result = requests.get(base_url, params=params).text
    data = json.loads(result)
    return pd.DataFrame(data)

st.title("Food Tinder (Any Meal, Any Location - Within a Week)")

# --- Configuration - Choose ONE location and ONE meal to start with ---
default_location_id = '96'  # REPLACE WITH AN ACTUAL LOCATION ID
default_meal_id = '148'      # REPLACE WITH AN ACTUAL MEAL ID

# --- Determine the date for the next week ---
today = date.today()
start_of_next_week = today + timedelta(days=(7 - today.weekday()) % 7 + 7)
next_week_date_str = start_of_next_week.strftime("%Y-%m-%dT00:00:00")

# --- Fetch the menu for the next week for the chosen location and meal ---
weekly_menu_df = get_week_menu(next_week_date_str, default_location_id, default_meal_id)

if 'weekly_menu' not in st.session_state:
    st.session_state['weekly_menu'] = weekly_menu_df.to_dict('records')
if 'current_meal_index' not in st.session_state:
    st.session_state['current_meal_index'] = 0
if 'user_preferences' not in st.session_state:
    st.session_state['user_preferences'] = {}

def record_preference(preference):
    if st.session_state['weekly_menu']:
        meal = st.session_state['weekly_menu'][st.session_state['current_meal_index']]
        meal_name = meal.get('name', 'Unnamed Meal') # Adjust key if needed
        st.session_state['user_preferences'][meal_name] = preference
        if st.session_state['current_meal_index'] < len(st.session_state['weekly_menu']) - 1:
            st.session_state['current_meal_index'] += 1
        else:
            st.info(f"You've seen all the meals for this week at this location and meal!")
    else:
        st.info("No menu data available.")

if st.session_state['weekly_menu']:
    if st.session_state['current_meal_index'] < len(st.session_state['weekly_menu']):
        current_meal = st.session_state['weekly_menu'][st.session_state['current_meal_index']]
        st.subheader(current_meal.get('name', 'Unnamed Meal')) # Adjust key if needed
        if 'description' in current_meal: # Adjust key if needed
            st.write(current_meal['description'])

        col1, col2, col3 = st.columns(3)
        with col1:
            dislike_button = st.button("👎 Dislike")
        with col2:
            no_preference_button = st.button("😐 No Preference")
        with col3:
            like_button = st.button("❤️ Like")

        if dislike_button:
            record_preference("Dislike")
            st.rerun()
        elif no_preference_button:
            record_preference("No Preference")
            st.rerun()
        elif like_button:
            record_preference("Like")
            st.rerun()
    else:
        st.write("--- Your Preferences ---")
        st.write(st.session_state['user_preferences'])
else:
    st.info("Fetching menu...")
    