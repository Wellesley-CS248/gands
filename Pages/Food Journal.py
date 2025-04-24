import streamlit as st
import sqlite3
from datetime import datetime
from myPalate import get_day_menu
from myPalate import get_meal_and_location
from myPalate import ids
#from UserSpecificDBs import init_user_db
#from databases.UserSpecificDBs import init_fj_db

#init_user_db()
#init_fj_db()

conn = sqlite3.connect("food_journal_new")
cursor = conn.cursor()
# Table for food journal
cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_journal_new (
        entryID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        mealID TEXT,
        dining_hall TEXT,
        date TEXT,
        liked BOOLEAN,
        FOREIGN KEY (userID) REFERENCES users(userID),
        FOREIGN KEY (mealID) REFERENCES meals(mealID)
    )
''')

conn.commit()
conn.close()




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
.st-an.st-ao.st-ap.st-aq.st-ak.st-ar.st-am.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9.st-ba.st-bb.st-cs  {
background-color: #DAD7CD;}
.st-emotion-cache-b0y9n5.e486ovb8  { 
  background-color: #DAD7CD !important;
}
</style>
""", unsafe_allow_html=True,
) 

conn = sqlite3.connect("food_journal_new")
cursor = conn.cursor()
# Table for food journal
cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_journal_new (
        entryID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        mealID TEXT,
        dining_hall TEXT,
        date TEXT,
        liked BOOLEAN,
        FOREIGN KEY (userID) REFERENCES users(userID),
        FOREIGN KEY (mealID) REFERENCES meals(mealID)
    )
''')

conn.commit()
conn.close()


st.title("Food Journal")
st.header("Add Entry")

def store_entry(
        mealID: str,
        dining_hall: str,
        date: str,
        liked: bool,
):
    conn = sqlite3.connect("food_journal_new")
    cursor = conn.cursor()

    # Ensure user exists and fetch user_id
    #cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
    #cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    #user_id = cursor.fetchone()[0]
    user_id = st.secrets["google"]["client_id"]

    # Insert summary record and get its ID
    cursor.execute('''
        INSERT INTO food_journal_new (userID, mealID, dining_hall, date, liked)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, mealID, locationID, date, liked))
    entryID = cursor.lastrowid

    conn.commit()
    conn.close()


with st.form("Journal Entry"):
    dining_hall = st.selectbox("Where?", ["Lulu", "Tower", "Stone D", "Bates"])
    meal = st.selectbox("When?", ["Breakfast", "Lunch", "Dinner"])
    locationID, mealID = get_meal_and_location(ids, dining_hall, meal )
    #today = datetime.today()
    date = "2025-04-16T00:00:00" #str(today.strftime("%Y-%m-%d")) + "T00:00:00"
    meals = get_day_menu(date, locationID, mealID)
    if meals.empty:
        st.write("No data available.")
    else:
        meals_for_day = []
        for i in range(len(meals)):
            meals_for_day.append(meals.iloc[i]['name'])
        selections = st.multiselect("What?", meals_for_day)
        submitted = st.form_submit_button("Add Entry")


liked_ids = []

if "selections_ids" not in st.session_state:
    st.session_state["selections_ids"] = []


#Table header
header_cols = st.columns([2, 1.5])
header_cols[0].markdown("#### Dish")
header_cols[1].markdown("#### Like")

# st.markdown("---")

# Loop through each row of the dataframe
for item in selections:
    if item not in st.session_state:
        st.session_state[item] = False
    col1, col2= st.columns([2, 1])
    col1.write(item)
    with col2:            
        st.session_state[item] = st.checkbox("Like?", key=f"check_{item}", value = st.session_state[item])
    if st.session_state[item]:
        for idx, row in meals.iterrows():
            if item == row["name"]:
                st.session_state["selections_ids"].append(row["id"])
            else:
                if item == row["name"] and row["id"] in st.session_state["selection_ids"]:
                    st.session_state["selection_ids"].remove(row["id"])

            

dish_ids_selected = st.session_state["selections_ids"]

if len(dish_ids_selected) != 0:
    for selection in dish_ids_selected:
        bool = selection in dish_ids_selected
        store_entry(selection, locationID, date, bool)
    st.write(f"Entry added for {meal} at {dining_hall} today!")

else:

    st.write("No meals selected.")



