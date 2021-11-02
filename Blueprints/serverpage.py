from flask import Blueprint, render_template, request


serverpage = Blueprint('serverpage', __name__)


from db import mysql


@serverpage.route("/<servern>")
def index(servern):
    
    # get serverinformation
    conn = mysql.connect()
    cur = conn.cursor()
    # select data from database based on URL (servername)
    cur.execute("SELECT * FROM servers WHERE servername = (%s)", (servern))
    servername = cur.fetchall()
    cur.close()


    # Reviews
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE servername = (%s) LIMIT 20", (servern))
    dcrevid = cur.fetchall()
    cur.close()
    
    return render_template("servertemplate.html", servername=servername, review=dcrevid)