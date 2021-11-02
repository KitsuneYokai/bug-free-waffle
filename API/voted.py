from flask import jsonify, Blueprint


voted = Blueprint('voted', __name__)


from db import  mysql
from limiter import Limiter

#TODO make limiter work
@voted.route("/if_voted<dcid>")
def if_voted(dcid):
    conn = mysql.connect()

    cur = conn.cursor()
    # Look if the user voted in the past 12h (defined by discorduserid)
    cur.execute("SELECT * from user_votes WHERE dcuserid = %s", (dcid))
    resault = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(resault)
