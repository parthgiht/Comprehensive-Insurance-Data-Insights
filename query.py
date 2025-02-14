import mysql.connector 
import streamlit as st

#Connection 
conn = mysql.connector.connect(
    host = "127.0.0.1",
    port = '3306',
    user = 'root',
    password = "Root",
    db = "insurancedashboard",
)
c = conn.cursor()

# Fetch 
def view_all_data():
    c.execute("SELECT * FROM insurancedashboard.`insurance data` ORDER BY id ASC")
    data = c.fetchall()
    return data