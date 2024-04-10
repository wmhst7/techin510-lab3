import os
import streamlit as st
import psycopg2
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# Connect to our database
con = psycopg2.connect(user="mhwu", password="Wmh311@pos", host="techin510wmh.postgres.database.azure.com", port=5432, database="postgres")
cur = con.cursor()


@dataclass
class Prompt:
    id: int = None
    title: str = ""
    prompt: str = ""
    is_favorite: bool = False

def prompt_form(prompt=Prompt()):
    with st.form(key="prompt_form"):
        title = st.text_input("Title", value=prompt.title)
        prompt_text = st.text_area("Prompt", height=200, value=prompt.prompt)
        is_favorite = st.checkbox("Favorite", value=prompt.is_favorite)
        submitted = st.form_submit_button("Submit")
        if submitted:
            return Prompt(prompt.id, title, prompt_text, is_favorite)

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
                edit_prompt(Prompt(p[0], p[1], p[2], p[3]))

def edit_prompt(prompt):
    new_prompt = prompt_form(prompt)
    if new_prompt:
        cur.execute("UPDATE prompts SET title = %s, prompt = %s, is_favorite = %s WHERE id = %s", 
                    (new_prompt.title, new_prompt.prompt, new_prompt.is_favorite, new_prompt.id))
        con.commit()
        st.success("Prompt updated successfully!")
        st.experimental_rerun()

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

# Search and sort bar
search_query = st.text_input("Search prompts")
sort_order = st.selectbox("Sort by", ["created_at", "title"], index=0)
search_button = st.button("Search")

query = "SELECT * FROM prompts"
if search_query:
    query += " WHERE title LIKE %s OR prompt LIKE %s"
    query += f" ORDER BY {sort_order} DESC"
    cur.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
else:
    query += f" ORDER BY {sort_order} DESC"
    cur.execute(query)

prompts = cur.fetchall()
display_prompts(prompts)

prompt = prompt_form()
if prompt:
    if prompt.id:  # This means we are updating an existing prompt
        cur.execute("UPDATE prompts SET title = %s, prompt = %s, is_favorite = %s WHERE id = %s", 
                    (prompt.title, prompt.prompt, prompt.is_favorite, prompt.id))
    else:  # This means we are creating a new prompt
        cur.execute("INSERT INTO prompts (title, prompt, is_favorite) VALUES (%s, %s, %s)", 
                    (prompt.title, prompt.prompt, prompt.is_favorite))
    con.commit()
    st.success("Prompt added/updated successfully!")
    st.experimental_rerun()

# Additional feature: Render prompts as templates
st.subheader("Rendered Prompt Templates")
template_id = st.selectbox("Choose a prompt to render", [p[0] for p in prompts])
if template_id:
    selected_prompt = next((p for p in prompts if p[0] == template_id), None)
    if selected_prompt:
        st.text_area("Rendered Prompt", value=selected_prompt[2], height=300)