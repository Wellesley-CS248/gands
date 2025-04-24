import requests
import json
import time
from datetime import datetime
import pandas as pd
import csv
import streamlit as st
import numpy
import sqlite3
from  auth import google_login
from userProfile import render_user_profile
from pushDBtoPrivate import download_db_from_github
#from databases.UserSpecificDBs import init_user_db
#from databases.UserSpecificDBs import init_fj_db

#download_db_from_github()
google_login()
#init_user_db()
#init_fj_db

conn = sqlite3.connect("users_new")
cursor = conn.cursor()

# Table for individual users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_new (
        userID PRIMARY KEY,
        firstName TEXT,
        lastName TEXT,
        diningHall TEXT,
        allergies TEXT,
        restrictions TEXT    
    )
''')
conn.commit()
conn.close()


conn = sqlite3.connect("users_new")
cursor = conn.cursor()

# Table for individual users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_new (
        userID PRIMARY KEY,
        firstName TEXT,
        lastName TEXT,
        diningHall TEXT,
        allergies TEXT,
        restrictions TEXT    
    )
''')
conn.commit()
conn.close()
#############################################################
#App Theme
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

DEBUG = False #keep false when testing login
#DEBUG = True # keep true when don't want to go throuhg testing

def fake_login():
    """Sets a fake access token and user info for debugging."""
    st.session_state["access_token"] = "fake-token"
    st.session_state["fake_user_name"] = "Test Student"
    st.session_state["fake_user_picture"] = "https://i.pravatar.cc/60?img=25"  # random placeholder


def get_week_menu(date, locationID, mealID):
    base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {"date": date, "locationID": locationID, "mealID": mealID}
    result = requests.get(base_url, params=params).text
    data = json.loads(result)
    return pd.DataFrame(data)

def get_day_menu(date, locationID, mealID):
    base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {"date": date, "locationID": locationID, "mealID": mealID}
    result = requests.get(base_url, params=params).text
    data = json.loads(result)
    df = pd.DataFrame(data)
    df = df[df["date"] == date]
    df = df.drop_duplicates(subset="id")
    if df.empty:
        st.info(f"No menu available for today {datetime.today}")
        return False
    return df

######################################################################################
#Rendering sidebar and pages (Tinder, Food Journal, Dashboard)


st.title("My Palate")
page_selected = st.sidebar.success("Menu")

#Manipulating date to match date in dataframe
date = str(st.date_input("Date: ")) + "T00:00:00"



#User selects dining hall and meal
dining_hall = st.selectbox("Dining Hall: ", ["Lulu", "Tower", "Stone D", "Bates"])
meal = st.selectbox("Meal: ", ["Breakfast", "Lunch", "Dinner"])



locationID = 0
mealID = 0
with open("wellesley-dining.csv", "r") as file:
    meals = pd.read_csv(file)

ids = pd.read_csv("wellesley-dining.csv")

def get_meal_and_location(df, loc, meal):
    """

    """
    if loc == "Lulu":
        loc = "Bao"
    matching_df = df[(df["location"] == loc) & (df["meal"] == meal)]
    locationID = matching_df["locationId"].iloc[0]
    mealID = matching_df["mealID"].iloc[0]
    return locationID, mealID


locationID, mealID = get_meal_and_location(ids, dining_hall, meal)

if "show_menu" not in st.session_state:
    st.session_state["show_menu"] = False

show_menu = st.button("Show Menu")

if show_menu:
    st.session_state["show_menu"] = False
    st.write(get_day_menu(date, locationID, mealID))


##########################################################################
#Set new preferences button

def update_meal_preferences(meal):
    cursor = sqlite3.connect("users")
    cursor.connect()

    cursor.execute('''
        INSERT INTO preferences[users], ?, meal
    ''')

preferences = st.button("Set new preferences")
if preferences and ('diet_rest' not in st.session_state):
    diet_rest = st.selectbox("Select dietary restrictions", ["Vegan", "Vegetarian", "Gluten Sensitive"]);
    allergies = st.selectbox("Select allergies", ["Eggs", "Fish", "Milk", "Peanuts", "Soy", "Sesame", "Shellfish", "Tree Nuts", "Wheat"])

    st.session_state['diet_rest'] = diet_rest
    st.session_state['allergies'] = allergies

#CLIENT_ID = st.secrets['google']['client_id']