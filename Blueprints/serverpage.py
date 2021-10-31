from flask import Blueprint, render_template
from db import mysql
from waffle import discord

serverpage = Blueprint('serverpage', __name__)


@serverpage.route("/<servern>")
def index(servern):
    
    # get serverinformation
    conn = mysql.connect()
    cur = conn.cursor()
    # select data from database based on URL (servername)
    cur.execute("SELECT * FROM servers WHERE servername = (%s)", (servern))
    servername = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE servername = (%s)", (servern))
    dcrevid = cur.fetchall()
    cur.close()
    
    return render_template("servertemplate.html", servername=servername, reviews=dcrevid)