from quart import jsonify, Blueprint
from quart_rate_limiter import limit_blueprint, timedelta


voted = Blueprint('voted', __name__)
limit_blueprint(voted, 60, timedelta(minutes=1))


from db import  mysql

@voted.route("/if_voted<dcid>")
async def if_voted(dcid):
    conn = mysql.connect()
    
    cur = conn.cursor()
    # Delete voter database entry if the vote is older than 12 h
    cur.execute("DELETE FROM `user_votes` WHERE `voted_time` < ADDDATE(NOW(), INTERVAL -12 HOUR)")
    cur.close()
    conn.commit()
    
    cur = conn.cursor()
    # Look if the user voted in the past 12h (defined by discorduserid)
    cur.execute("SELECT * from user_votes WHERE dcuserid = %s", (dcid))
    res = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(res)
