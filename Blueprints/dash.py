# imports
from quart import request, redirect, url_for, Blueprint, flash, render_template
from quart_discord import Unauthorized, requires_authorization
from nextcord.ext import commands
from quart_rate_limiter import limit_blueprint, timedelta


from decouple import config

dash = Blueprint('dash', __name__)
limit_blueprint(dash, 60, timedelta(minutes=1))


# imports from py
from waffle import discord
from db import mysql


@dash.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login.index"))


"""routes/Dashboard"""
@dash.route('/dash',)
@requires_authorization
async def index():
    return await render_template('dashboard.html')


@commands.command()
@requires_authorization
@dash.route('/register_server', methods=["GET","POST"])
async def reg_server():
    # Variables
    user = await discord.fetch_user()
    msg=""

    #MySQL
    conn = mysql.connect()
    cur = conn.cursor()
    # look in the database if the user has registered a server
    cur.execute("SELECT registered_by FROM servers WHERE registered_by = (%s)", (user.id))
    reg_by = cur.fetchall()
    cur.close()

    if request.method == 'POST' and 'servername_input' and 'serverurl_input' and 'discordid_input' and 'servertext_input' and 'server_icon' in await request.form:
        servername_input =  (await request.form)['servername_input']
        serverurl_input =  (await request.form)['serverurl_input']
        discordid_input =  (await request.form)['discordid_input']
        servertext_input =  (await request.form)['servertext_input']
        server_icon =  (await request.form)['server_icon']
        
        cur = conn.cursor()
        # look in the database if the user has registered a server
        cur.execute("SELECT * FROM servers where servername = %s", (servername_input))
        servername_sql = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        # look in the database if the user has registered a server
        cur.execute("SELECT * FROM servers where discordserverid = %s", (discordid_input))
        discordserverid_sql = cur.fetchall()
        cur.close()
        
        if reg_by:
            await flash("You already have a server registered")
            return redirect(url_for("dash.index"))
        
        elif servername_sql:
            msg="That servername is already taken"
        
        elif discordserverid_sql:
            msg="That discord server is already linked to another server"

        # If the user dosnt have a server, and the servername/discordserver_id isn't already registered, insert the data from the form into the database
        else:
            cur = conn.cursor()
            # write data to database
            cur.execute("INSERT INTO servers(servername, serverurl, discordserverid, server_text, registered_by, votes, servericon) VALUES (%s,%s,%s,%s,%s,0,%s)", (servername_input, serverurl_input, discordid_input, servertext_input, user.id, server_icon))
            cur.close()
            conn.commit()
            conn.close()

            await flash("Your server has been successfully registered")
            return redirect(url_for("dash.index"))

    return await render_template('dash_register.html', msg=msg)


# Edit your server
# Todo: Disallow the edit of the servername aswell as the dc serverid, because that could cause trouble with the vote bot
@dash.route('/edit_server', methods=['POST', 'GET'])
@requires_authorization
async def edit_server():
    # Variables
    user = await discord.fetch_user()
    msg=""
    conn = mysql.connect()

    cur = conn.cursor()
    # get the data from the database to edit
    cur.execute('SELECT * FROM servers WHERE registered_by = (%s)', (user.id))
    serverdata = cur.fetchall()
    cur.close()

    if serverdata:
        if request.method == 'POST' and 'servername_input' and 'serverurl_input' and 'discordid_input' and 'servertext_input' and 'server_icon' in await request.form:       
            servername_input =  (await request.form)['servername_input']
            serverurl_input =  (await request.form)['serverurl_input']
            discordid_input =  (await request.form)['discordid_input']
            servertext_input =  (await request.form)['servertext_input']
            server_icon = (await request.form)['server_icon']

            cur = conn.cursor()
            # Edit the data
            cur.execute('UPDATE servers SET servername=%s, serverurl=%s, discordserverid=%s, server_text=%s, servericon=%s WHERE registered_by=%s',(servername_input, serverurl_input, discordid_input, servertext_input, server_icon, user.id))
            cur.close()
            conn.commit()
            conn.close() 

            await flash("Your server information has been updated")
            return redirect(url_for("dash.index"))
    
    else:
        await flash("you don't have a server registered. register a server in order to edit it. makes sense right?")
        return redirect (url_for("dash.index"))
    
    return await render_template('dash_serveredit.html', serverdata=serverdata, msg=msg)

# Vote for your favorite server
@dash.route('/vote_server', methods=['POST', 'GET'])
@requires_authorization
async def vote():
    # Variables
    user = await discord.fetch_user()
    msg=""
    conn = mysql.connect()

    cur = conn.cursor()
    # Delete voter database entry if the vote is older than 12 h
    cur.execute("DELETE FROM `user_votes` WHERE `voted_time` < ADDDATE(NOW(), INTERVAL -12 HOUR)")
    cur.close()
    conn.commit()

    cur = conn.cursor()
    # look if the user is in the vote database
    cur.execute("SELECT voted, voted_time FROM user_votes WHERE dcuserid = (%s)", (user.id))
    voted = cur.fetchall()
    cur.close()

    if voted:
        await flash("You already voted in the past 12h")
        return redirect (url_for("dash.index"))

    else:
        cur = conn.cursor()
        # Get servernames to insert into the form
        cur.execute('SELECT servername, serverid FROM servers')
        serverdata = cur.fetchall()
        cur.close()

        if request.method == 'POST' and 'serverid' in await request.form:

            serverid = (await request.form)['serverid']
            
            cur = conn.cursor()
            # if the user is not deleted by line 130 insert data / vote
            cur.execute('UPDATE servers SET votes = votes + 1 WHERE serverid = %s',(serverid))
            cur.close()
            conn.commit()
            
            cur = conn.cursor()
            cur.execute("INSERT INTO user_votes(dcuserid, voted, voted_time) VALUES (%s,%s, CURRENT_TIMESTAMP)", (user.id, serverid))
            cur.close()
            conn.commit()
            conn.close()
            
            await flash("You successfully voted for your favorite server")
            return redirect(url_for("dash.index"))

    return await render_template('dash_vote.html', serverdata=serverdata, msg=msg)


# write a review for a server
@dash.route('/review',methods=['POST', 'GET'])
@requires_authorization
async def review():
    # Variables
    user = await discord.fetch_user()
    msg=""
    conn = mysql.connect()

    cur = conn.cursor()
    # Get servernames to insert into the form
    cur.execute('SELECT servername, serverid FROM servers')
    serverdata = cur.fetchall()
    cur.close()

    if request.method == 'POST' and 'choose_server' and 'server_text' and 'serverid' in await request.form:

        serverid = (await request.form)['serverid']
        review_server = (await request.form)['choose_server']
        review_txt = (await request.form)['server_text']

        cur = conn.cursor()
        # look if the user already wrote a review for that server
        cur.execute("SELECT * FROM reviews WHERE dcuserid = %s and serverid = %s", (user.id, serverid))
        revserver = cur.fetchall()
        cur.close()
        
        if revserver:
            await flash("you already reviewed that server, and reviews are final. (RIP)")
            return redirect (url_for("dash.index"))

        else:
            # Insert data into the database
            cur = conn.cursor()
            cur.execute("INSERT INTO reviews(servername, revtext, dcuserid, revat, serverid) VALUES (%s,%s,%s,CURRENT_TIMESTAMP,%s)", (review_server, review_txt, user.id, serverid))
            cur.close()
            conn.commit()
            conn.close()
            
            await flash("Your review has been submitted and has now a chance to be shown on the serverpage")
            return redirect(url_for("dash.index"))

    return await render_template('dash_review.html', msg=msg, serverdata=serverdata)


# Route to deleat the server from the Database
@dash.route('/delete_server/<servers>',methods=['POST'])
@requires_authorization
async def delete_server(servers):
    # Variables
    user = await discord.fetch_user()
    msg=""
    conn = mysql.connect()

    if request.method == 'POST' and 'serverid' in await request.form:

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servers WHERE registered_by = (%s)", (user.id))
        servers = cur.fetchall()
        cur.close() 
        
        if servers:
            cur = conn.cursor()
            cur.execute("DELETE FROM servers WHERE registered_by = (%s)", (user.id))
            cur.close()
            conn.commit()  
            conn.close() 
            
            await flash("Bye Bye server. It was a nice time")
            return redirect (url_for("dash.index"))

    return await redirect (url_for("dash.index"))