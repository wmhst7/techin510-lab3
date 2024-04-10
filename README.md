# Promptbase

Promptbase is a simple and intuitive web application built with Streamlit and PostgreSQL that allows users to store, manage, and retrieve prompts efficiently. It provides a user-friendly interface for creating, editing, searching, and rendering prompts. This is TECHIN 510 Lab 3.

## Features

- Create new prompts with a title, content, and favorite status
- Edit and update existing prompts
- Delete prompts
- Search prompts by title or content
- Sort prompts by creation date or title
- Filter prompts to show only favorites
- Render selected prompts as templates
- Copy rendered prompts to the clipboard with a single click

## Prerequisites

Before running the Promptbase application, ensure that you have the following prerequisites installed:

- Python 3.x
- PostgreSQL database
- Required Python packages listed in the `requirements.txt` file

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/promptbase.git
   ```

2. Navigate to the project directory:

   ```
   cd promptbase
   ```

3. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:

   - Create a new PostgreSQL database for Promptbase.
   - Update the database connection details in the `.env` file.

5. Run the Streamlit application:

   ```
   streamlit run app.py
   ```

6. Access the Promptbase application in your web browser at `http://localhost:8501`.

## Usage

1. Create a new prompt by filling in the title, content, and optionally marking it as a favorite. Click the "Submit" button to save the prompt.

2. Use the search bar to search for prompts by title or content. The search results will be displayed automatically.

3. Sort the prompts by creation date or title using the "Sort by" dropdown.

4. Filter the prompts to show only favorites by checking the "Show favorites only" checkbox.

5. Edit a prompt by clicking the "Edit" button next to the prompt. Update the prompt details and click "Submit" to save the changes.

6. Delete a prompt by clicking the "Delete" button next to the prompt.

7. Render a selected prompt as a template by choosing a prompt from the "Choose a prompt to render" dropdown. The rendered prompt will be displayed below.

8. Copy the rendered prompt to the clipboard by clicking the "Copy Prompt" button.


## Lessions Learned

1. Streamlit proved to be a powerful and user-friendly framework for building interactive web applications quickly.
2. Integrating PostgreSQL with Streamlit allowed for efficient storage and retrieval of prompts. Understanding how to establish a connection, execute SQL queries, and handle data manipulation was crucial for the project's success.

## Questions
1. How to write more fancy web pages?