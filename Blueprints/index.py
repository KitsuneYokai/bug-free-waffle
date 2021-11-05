from quart import Blueprint, render_template

index = Blueprint('index', __name__)
from db import mysql


"""INDEX"""
@index.route('/',methods=["POST","GET"])
async def home():

    # Make MySQL connection
    conn = mysql.connect()
    cur = conn.cursor()

    # get the servername,server_text from the database
    cur.execute('SELECT servername, server_text, serverurl, votes FROM servers ORDER BY votes DESC')
    servername = list(cur.fetchall())
    cur.close()

    return await render_template('index.html', servername=servername)