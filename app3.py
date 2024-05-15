# Importing necessary libraries
import os
import sqlite3
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the model and get the response
def get_gemini_response(question, table_name, columns):
    prompt = generate_prompt(table_name, columns)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text

# Function to generate a dynamic prompt
def generate_prompt(table_name, columns):
    prompt = f"""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name {table_name}.
    \nExample - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM {table_name};
    \nExample - Tell me the details of the employees whose {columns[0]} is 'Sales'?,
    the SQL command will be something like this SELECT * FROM {table_name}
    where {columns[0]} = 'Sales';
    also the sql code should not have ``` in beginning or end and sql word in output
    """
    return prompt

# Function to execute SQL query on the database and fetch results
def execute_sql_query(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Define Streamlit app functions
def main():
    # Set page configuration
    st.set_page_config(
        page_title="SQL GPT",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"  # Expand the sidebar initially
    )

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        .css-18z1g7x {
            background-color: #f0f2f6;
        }
        .css-1sbxawv {
            background-color: #f0f2f6;
        }
        .st-cy {
            background-color: #ffffff;
        }
        .st-d4 {
            background-color: #ffffff;
        }
        .st-dg {
            background-color: #ffffff;
        }
        .st-dh {
            background-color: #ffffff;
        }
        .st-d6 {
            background-color: #ffffff;
        }
        .st-cl {
            background-color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar for upload
    st.sidebar.header("Upload CSV Files")
    uploaded_files = st.sidebar.file_uploader("Upload CSV files", accept_multiple_files=True, type=["csv"])
    table_names = []
    for uploaded_file in uploaded_files:
        table_name = st.sidebar.text_input(f"Enter Table Name for {uploaded_file.name}:")
        if table_name:
            table_names.append((table_name, uploaded_file))
    if not table_names:
        st.sidebar.info("Please upload CSV files and specify table names.")

    # Main content
    st.title("SQL GPT")
    st.markdown("---")  # Horizontal rule for separation

    # Dropdown menu to select table
    selected_table_name = st.selectbox("Select Table:", [name for name, _ in table_names] if table_names else [])

    # Display selected table
    if selected_table_name:
        st.subheader("Selected Database")
        conn = sqlite3.connect(":memory:")
        for table_name, uploaded_file in table_names:
            if table_name == selected_table_name:
                df = pd.read_csv(uploaded_file)
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                st.write(f"**{table_name}**")
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                input_data = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                input_df = pd.DataFrame(input_data, columns=columns)
                st.dataframe(input_df)

    # User Input
    if selected_table_name and 'conn' in locals():
        st.subheader("User Input")
        question = st.text_input("Input: ", key="input")
        submit = st.button("Ask the question")

        if submit:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({selected_table_name})")
            columns = [col[1] for col in cursor.fetchall()]  # Extracting column names
            response = get_gemini_response(question, selected_table_name, columns)
            st.subheader("Generated SQL Query")
            st.code(response, language="sql")

            # Execute SQL query and display result
            try:
                if response.strip().lower().startswith("insert") or response.strip().lower().startswith("delete") or response.strip().lower().startswith("update"):
                    cursor.execute(response)
                    num_affected_rows = cursor.rowcount
                    conn.commit()  # Commit changes to the database
                    if num_affected_rows > 0:
                        st.subheader("Result")
                        st.write("Operation Successful: Record updated/deleted/added successfully.")
                    else:
                        st.subheader("Result")
                        st.write("Operation Failed: No records were affected.")
                else:
                    query_result = execute_sql_query(response, conn)
                    if query_result:
                        st.subheader("Query Result")
                        if len(query_result) > 0:
                            df_result = pd.DataFrame(query_result)
                            st.dataframe(df_result)
                        else:
                            st.write("No results found.")
                    else:
                        st.write("No results found.")
            except Exception as e:
                st.error(f"An error occurred while executing the query: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    main()

