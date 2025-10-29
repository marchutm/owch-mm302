from flask import Flask
import os
import pyodbc

app = Flask(__name__)

def get_db_connection():
    conn_str = os.environ.get('SQLAZURECONNSTR_DB_CONNECTION_STRING')
    return conn_str, pyodbc.connect(conn_str)

@app.route('/')
def index():
    tasks_html = "<h2>Lista zadan z bazy danych:</h2><ul>"
    try:
        conn_str, conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Title FROM Tasks")
        rows = cursor.fetchall()
        for row in rows:
            tasks_html += f"<li>{row.Title}</li>"
        conn.close()
    except Exception as e:
        conn_str = os.environ.get('CUSTOMCONNSTR_DB_CONNECTION_STRING')
        tasks_html += f"<li>Blad polaczenia z baza: {str(e)}</li>"
        tasks_html += f"<li>Uzyty connection string: {conn_str}</li>"

    tasks_html += "</ul>"
    return tasks_html