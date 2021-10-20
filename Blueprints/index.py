from flask import Blueprint, render_template


index = Blueprint('index', __name__)
from db import mysql

"""INDEX"""
@index.route('/')
def home():

    # MySQL - Servername
    # Make MySQL connection
    conn = mysql.connect()
    cur = conn.cursor()

    # get the servername,server_text from the database
    cur.execute('SELECT servername, server_text, votes FROM servers ORDER BY votes DESC')
    servername = list(cur.fetchall())
    cur.close()
    conn.commit()

    # TODO add the right redirect 
    return render_template('index.html', servername=servername)