from xml.dom.domreg import registered
from flask import render_template, request, redirect, url_for, Blueprint
from flask_discord import Unauthorized, requires_authorization

dash = Blueprint('dash', __name__)

from waffle import discord
from db import mysql


@dash.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login.index"))


"""routes/Dashboard"""
@dash.route('/dash')
@requires_authorization
def index():
    return render_template('dashboard.html')


# Register a server to the site   
@dash.route('/register_server', methods=["GET","POST"])
# @requires_authorization
def reg_server():    
    msg=""
    if request.method == 'POST' and 'servername_input' in request.form and 'serverurl_input' and 'discordid_input' and 'servertext_input' in request.form:
            
        servername_input =  request.form['servername_input']
        serverurl_input =  request.form['serverurl_input']
        discordid_input =  request.form['discordid_input']
        servertext_input =  request.form['servertext_input']

        # MySQL - Servername
        # Make MySQL connection
        conn = mysql.connect()
        cur = conn.cursor()

        # get the see if the user is tn the database& has a server
        cur.execute('SELECT registered_by FROM servers')
        reg_by = list(cur.fetchall())
        cur.close()

        user = discord.fetch_user()
        userid = user.id

        if reg_by:
            msg="You already have an server registered"

        cur = conn.cursor()
        # write data to database
        # TODO re read how its done
        cur.execute('INSERT INTO servers (servername, serverurl, discordserverid, server_text, registered_by) VALUES (%s,%s,%s,%s,%s)' (servername_input,serverurl_input,discordid_input,servertext_input,userid))
        cur.close()
        msg="Your server has been successfully registered"


    return render_template('dash_register.html', msg=msg)


@dash.route('/edit_server')
@requires_authorization
def edit_server():
    return render_template('dash_serveredit.html')


@dash.route('/vote_server')
@requires_authorization
def vote():
    return render_template('dash_vote.html')


@dash.route('/review')
@requires_authorization
async def review():
    return await render_template('dash_review.html')