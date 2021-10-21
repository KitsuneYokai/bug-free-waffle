from flask import Blueprint, render_template
from db import mysql

serverpage = Blueprint('serverpage', __name__)

@serverpage.route("/<servern>")
def index(servern):
    
    # Make mysql connection & look if the provided servername exists in the database
    conn = mysql.connect()
    cur = conn.cursor()
    # write data to database
    cur.execute("SELECT servername, serverurl, server_text, discordserverid, registered_by, votes  FROM servers WHERE servername = (%s)", (servern))
    servername = cur.fetchall()
    cur.close()
    
    #TODO load reviews

    return render_template("servertemplate.html", servername=servername)