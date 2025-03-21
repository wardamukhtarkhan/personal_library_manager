import streamlit as st
import sqlite3
import pandas as pd

# Set up the SQLite database connection
def create_connection():
    conn = sqlite3.connect('library_v2.db')
    return conn

# Create table if it doesn't exist
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        year INTEGER
    )
    ''')
    conn.commit()
    conn.close()

# Add a book to the database
def add_book(title, author, genre, year):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    INSERT INTO books (title, author, genre, year) 
    VALUES (?, ?, ?, ?)
    ''', (title, author, genre, year))
    conn.commit()
    conn.close()

# Remove a book from the database
def remove_book(book_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

# Get all books from the database
def get_books():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    rows = c.fetchall()
    conn.close()
    return rows

# Search books by title, author, or genre
def search_books(query):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
    ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
    rows = c.fetchall()
    conn.close()
    return rows

# Main app
def main():
    # Injecting custom CSS for background color and other styling
    st.markdown("""
    <style>
    body {
        background-color: #f0e68c;  /* Light Yellow background */
        font-family: 'Verdana', sans-serif;
    }
    .css-1v3fvcr {
        background-color: #008080;  /* Teal color for sidebar */
    }
    .css-1v3fvcr .sidebar .sidebar-content {
        color: white;
    }
    h1, h2, h3 {
        color: #d2691e;  /* Chocolate color for headers */
    }
    .stButton>button {
        background-color: #ff4500;  /* Orange red for buttons */
        color: white;
    }
    .stTextInput input {
        background-color: #f5f5dc;  /* Beige color for text input */
    }
    .stSelectbox, .stNumberInput {
        background-color: #f5f5dc;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Personal Library Manager ")

    create_table()

    # Sidebar for navigation
    menu = ["Home", "Add Book", "Search Books", "View Books", "Remove Book"]
    choice = st.sidebar.selectbox("Select an Option", menu)

    if choice == "Home":
        st.subheader("Welcome to Your Personal Library!")
        st.write("Manage your library using the options on the left sidebar.")

    elif choice == "Add Book":
        st.subheader("Add a New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        year = st.number_input("Publication Year", min_value=1900, max_value=2025, step=1)

        if st.button("Add Book"):
            if title and author:
                add_book(title, author, genre, year)
                st.success("Book successfully added!")
            else:
                st.error("Please fill in all fields!")

    elif choice == "Search Books":
        st.subheader("Search for Books")
        query = st.text_input("Search by title, author, or genre")
        if query:
            books = search_books(query)
            if books:
                df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year"])
                st.dataframe(df)
            else:
                st.warning("No books found that match your query.")

    elif choice == "View Books":
        st.subheader("View All Books in Your Library")
        books = get_books()
        if books:
            df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year"])
            st.dataframe(df)
        else:
            st.warning("Your library is currently empty.")

    elif choice == "Remove Book":
        st.subheader("Remove a Book")
        books = get_books()
        if books:
            book_ids = [book[0] for book in books]
            book_to_remove = st.selectbox("Select a book to remove", book_ids)
            if st.button("Remove Book"):
                remove_book(book_to_remove)
                st.success("Book successfully removed!")
        else:
            st.warning("No books to remove.")

if __name__ == "__main__":
    main()
