from flask import Blueprint, render_template, make_response, request, jsonify
import random
import time

index = Blueprint('index', __name__)
from db import mysql

"""INDEX"""
@index.route('/')
def home():

    # MySQL - Servername
    # Make MySQL connection
    conn = mysql.connect()
    cur = conn.cursor()

    # get the servername,server_text & serverid from the database
    cur.execute('SELECT servername, server_text, idservers FROM servers ORDER BY votes DESC')
    servername = list(cur.fetchall())
    cur.close()

    # TODO 
    return render_template('index.html', servername=servername)