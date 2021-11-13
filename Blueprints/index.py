from quart import Blueprint, render_template

index = Blueprint('index', __name__)
from db import mysql
from waffle import ipc_client

"""INDEX"""
@index.route('/',methods=["POST","GET"])
async def home():
    commands = await ipc_client.request("get_cmd")
    desc = await ipc_client.request("get_cmd_desc")
    
    member = await ipc_client.request("get_member_count")
    uptime = await ipc_client.request("get_uptime")
    guilds = await ipc_client.request("get_guild_count")
    # Make MySQL connection
    conn = mysql.connect()
    cur = conn.cursor()

    # get the servername,server_text from the database
    cur.execute('SELECT * FROM servers ORDER BY votes DESC')
    servername = list(cur.fetchall())
    cur.close()

    return await render_template('index.html', servername=servername, commands=commands, member=member, uptime=uptime, guilds=guilds, desc=desc)