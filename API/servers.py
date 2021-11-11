from quart import jsonify, Blueprint
from quart_rate_limiter import limit_blueprint, timedelta


servers = Blueprint('servers', __name__)
limit_blueprint(servers, 20, timedelta(minutes=1))

from db import mysql

@servers.route("/serverlist")
async def Serverlist():
    
    conn = mysql.connect()
    cur = conn.cursor()
    # Delete voter database entry if the vote is older than 12 h
    cur.execute("SELECT * FROM servers ORDER BY votes DESC")
    serverdata = cur.fetchall()
    cur.close()
    conn.commit()
    
    return jsonify(serverdata)