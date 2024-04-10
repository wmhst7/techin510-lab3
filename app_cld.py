import os
from dataclasses import dataclass

import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Connect to our database
con = psycopg2.connect(user="mhwu", password="Wmh311@pos", host="techin510wmh.postgres.database.azure.com", port=5432, database="postgres")
cur = con.cursor()

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

@dataclass
class Prompt:
    title: str
    prompt: str
    is_favorite: bool = False

def prompt_form(prompt=Prompt("","",False)):
    with st.form(key="prompt_form", clear_on_submit=True):
        title = st.text_input("Title", value=prompt.title)
        prompt_text = st.text_area("Prompt", height=200, value=prompt.prompt)
        is_favorite = st.checkbox("Favorite", value=prompt.is_favorite)
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not title.strip() or not prompt_text.strip():
                st.error("Title and Prompt are required.")
            else:
                return Prompt(title, prompt_text, is_favorite)

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

search_query = st.text_input("Search prompts")
sort_by = st.selectbox("Sort by", ["Created At (Newest First)", "Created At (Oldest First)", "Title (A-Z)", "Title (Z-A)"])
filter_favorite = st.checkbox("Show only favorites")

prompt = prompt_form()
if prompt:
    cur.execute("INSERT INTO prompts (title, prompt, is_favorite) VALUES (%s, %s, %s)", (prompt.title, prompt.prompt, prompt.is_favorite))
    con.commit()
    st.success("Prompt added successfully!")

# Build the SQL query based on the search and filter options
sql_query = "SELECT * FROM prompts"
if search_query:
    sql_query += f" WHERE title ILIKE '%{search_query}%' OR prompt ILIKE '%{search_query}%'"
if filter_favorite:
    if "WHERE" in sql_query:
        sql_query += " AND is_favorite = TRUE"
    else:
        sql_query += " WHERE is_favorite = TRUE"

if sort_by == "Created At (Newest First)":
    sql_query += " ORDER BY created_at DESC"
elif sort_by == "Created At (Oldest First)":
    sql_query += " ORDER BY created_at ASC"
elif sort_by == "Title (A-Z)":
    sql_query += " ORDER BY title ASC"
elif sort_by == "Title (Z-A)":
    sql_query += " ORDER BY title DESC"

cur.execute(sql_query)
prompts = cur.fetchall()

for p in prompts:
    with st.expander(p[1]):
        st.code(p[2])
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Delete", key=f"delete_{p[0]}"):
                cur.execute("DELETE FROM prompts WHERE id = %s", (p[0],))
                con.commit()
                st.rerun()
        with col2:
            if st.button("Edit", key=f"edit_{p[0]}"):
                prompt