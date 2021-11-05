# imports
from flask import ctx
from quart import request, redirect, url_for, Blueprint, flash, render_template
from quart_discord import Unauthorized, requires_authorization
from nextcord.ext import commands
import discapty

from decouple import config

dash = Blueprint('dash', __name__)


# imports from py
from waffle import discord
from waffle import bot
from db import mysql

hsitekey = config('HCAPTCHA_SITE_KEY')


@dash.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login.index"))


"""routes/Dashboard"""
@dash.route('/dash',)
@requires_authorization
async def index():
    return await render_template('dashboard.html')


@commands.command()
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

    async def send_captcha(ctx):
        captcha = discapty.Captcha("image")
        captcha_image = discord.File(captcha.generate_captcha(), filename="captcha.png") # This is # # important to put this filename, otherwise Discord will send the image outside of the embed.
        # You can change it when generating the embed. 
        captcha_embed = captcha.generate_embed(ctx.user.id)
        await ctx.channel.send(embed=captcha_embed, file=captcha_image)
    
    await send_captcha(ctx)
# await bot.send_message(discord.Object(id='844648524955910175'), 'hello')
    if request.method == 'POST' and 'servername_input' and 'serverurl_input' and 'discordid_input' and 'servertext_input' in await request.form:
        servername_input =  (await request.form)['servername_input']
        serverurl_input =  (await request.form)['serverurl_input']
        discordid_input =  (await request.form)['discordid_input']
        servertext_input =  (await request.form)['servertext_input']
        
        if reg_by:
            await flash("You already have a server registered")
            return redirect(url_for("dash.index"))
        # If the user dosnt have a server, insert the data from the form into the database
        else:
            cur = conn.cursor()
            # write data to database
            cur.execute("INSERT INTO servers(servername, serverurl, discordserverid, server_text, registered_by, votes) VALUES (%s,%s,%s,%s,%s,0)", (servername_input, serverurl_input, discordid_input, servertext_input, user.id))
            cur.close()
            conn.commit()
            conn.close()
            await flash("Your server has been successfully registered")
            return redirect(url_for("dash.index"))

    return await render_template('dash_register.html', msg=msg, hsitekey=hsitekey)


# Edit your server
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
        if request.method == 'POST' and 'servername_input' and 'serverurl_input' and 'discordid_input' and 'servertext_input' in await request.form:
            
            servername_input =  (await request.form)['servername_input']
            serverurl_input =  (await request.form)['serverurl_input']
            discordid_input =  (await request.form)['discordid_input']
            servertext_input =  (await request.form)['servertext_input']

            cur = conn.cursor()
            # Edit the data
            cur.execute("UPDATE servers SET servername=%s, serverurl=%s, discordserverid=%s, server_text=%s WHERE registered_by=%s",(servername_input, serverurl_input, discordid_input, servertext_input, user.id))
            cur.close()
            conn.commit()
            await flash("Your server information has been updated")
            return redirect (url_for("dash.index"))

    else:
        await flash("you don't have a server registered. register a server in order to edit it. makes sense right?")
        return redirect (url_for("dash.index"))

    return await render_template('dash_serveredit.html', serverdata=serverdata, msg=msg, hsitekey=hsitekey)


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
        flash("You already voted in the past 12h")
        return redirect (url_for("dash.index"))

    else:
        cur = conn.cursor()
        # Get servernames to insert into the form
        cur.execute('SELECT servername FROM servers')
        serverdata = cur.fetchall()
        cur.close()

        if request.method == 'POST' and 'choose_server' in await request.form:

            chose_server =  (await request.form)['choose_server']

            cur = conn.cursor()
            # if the user is not deleted by line 130 insert data / vote
            cur.execute('UPDATE servers SET votes = votes + 1 WHERE servername = %s',(chose_server))
            cur.close()
            conn.commit()
            cur = conn.cursor()
            cur.execute("INSERT INTO user_votes(dcuserid, voted, voted_time) VALUES (%s,%s, CURRENT_TIMESTAMP)", (user.id, chose_server))
            cur.close()
            conn.commit()
            
            await flash("Your successfully voted for your favorite server")
            return redirect(url_for("dash.index"))

    return await render_template('dash_vote.html', serverdata=serverdata, msg=msg, hsitekey=hsitekey)


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
            
            await flash("Your review has been submitted and has now a chance to be shown on the serverpage")
            return redirect(url_for("dash.index"))

    return await render_template('dash_review.html', msg=msg, hsitekey=hsitekey, serverdata=serverdata)


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
            
            await flash("Bye Bye server. It was a nice time")
            return redirect (url_for("dash.index"))

    return await redirect (url_for("dash.index", msg=msg))