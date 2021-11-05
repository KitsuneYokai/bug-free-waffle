from quart import Blueprint, render_template

serverpage = Blueprint('serverpage', __name__)


from db import mysql


@serverpage.route("/<servern>")
async def index(servern):
    
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
    
    return await render_template("servertemplate.html", servername=servername, review=dcrevid)