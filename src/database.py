import sqlite3 

Database_path = "db/Mistakes.db"

def init_db():
    """Initilize the database with the required schema."""
    with sqlite3.connect(Database_path) as connection:
        with open("db/schema.sql", "r") as query:
            connection.executescript(query.read()) 

def log_mistakes(user_id, mistake, correction):
    """Log a user's mistake into the database."""
    with sqlite3.connect(Database_path) as connection:
        cursor = connection.cursor() 
        cursor.execute(
            "INSERT INTO Mistakes (User_ID, Mistake, Correction) VALUES (?, ?, ?)",
            (user_id, mistake, correction) 
        )
        connection.commit() 

def get_mistakes(user_id):
    """Retrive all mistakes made by a specific user."""
    with sqlite3.connect(Database_path) as connection:
        cursor = connection.cursor() 
        cursor.execute(
            "SELECT Mistake, Correction, timestamp"
            "FROM Mistakes Where User_ID = ?", (user_id, )
        )
        return cursor.fetchall() 
