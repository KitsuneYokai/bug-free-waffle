from flask import Blueprint, render_template
from db import mysql

serverpage = Blueprint('serverpage', __name__)

@serverpage.route("/<servern>")
def index(servern):
    
    # get serverinformation
    conn = mysql.connect()
    cur = conn.cursor()
    # select data from database based on URL (servername)
    cur.execute("SELECT servername, serverurl, server_text, discordserverid, registered_by, votes  FROM servers WHERE servername = (%s)", (servern))
    servername = cur.fetchall()
    cur.close()
    
    #TODO load reviews

    return render_template("servertemplate.html", servername=servername)