import os
from dataclasses import dataclass
import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Database connection setup
con = psycopg2.connect(
    user="mhwu", 
    password="Wmh311@pos", 
    host="techin510wmh.postgres.database.azure.com", 
    port=5432, 
    database="postgres"
)
cur = con.cursor()

# Create table with favorites column
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        is_favorite BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)
con.commit()

@dataclass
class Prompt:
    title: str
    prompt: str
    is_favorite: bool = False

def prompt_form(prompt=Prompt("", "")):
    with st.form(key="prompt_form", clear_on_submit=True):
        title = st.text_input("Title", value=prompt.title)
        prompt_text = st.text_area("Prompt", height=200, value=prompt.prompt)
        submitted = st.form_submit_button("Submit")
        if submitted:
            return Prompt(title, prompt_text)

def display_prompts(prompts):
    for p in prompts:
        with st.expander(f"{p[1]}{' ★' if p[3] else ''}"):
            st.code(p[2])
            if st.button("Delete", key=f"delete_{p[0]}"):
                cur.execute("DELETE FROM prompts WHERE id = %s", (p[0],))
                con.commit()
                st.experimental_rerun()
            if st.button("Toggle Favorite", key=f"fav_{p[0]}"):
                cur.execute("UPDATE prompts SET is_favorite = NOT is_favorite WHERE id = %s", (p[0],))
                con.commit()
                st.experimental_rerun()
            if st.button("Edit", key=f"edit_{p[0]}"):
                # Placeholder for edit functionality
                pass

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

# Search bar
search_query = st.text_input("Search prompts")
search_button = st.button("Search")
if search_button and search_query:
    cur.execute("SELECT * FROM prompts WHERE title LIKE %s OR prompt LIKE %s", ('%' + search_query + '%', '%' + search_query + '%'))
else:
    cur.execute("SELECT * FROM prompts")

prompts = cur.fetchall()
display_prompts(prompts)

prompt = prompt_form()
if prompt:
    cur.execute("INSERT INTO prompts (title, prompt) VALUES (%s, %s)", (prompt.title, prompt.prompt))
    con.commit()
    st.success("Prompt added successfully!")
    st.experimental_rerun()