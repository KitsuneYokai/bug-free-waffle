from sqlite3 import Row
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
@requires_authorization
def reg_server():
    msg=""
    if request.method == 'POST' and 'servername_input' in request.form and 'serverurl_input' and 'discordid_input' and 'servertext_input' in request.form:
            
        servername_input =  request.form['servername_input']
        serverurl_input =  request.form['serverurl_input']
        discordid_input =  request.form['discordid_input']
        servertext_input =  request.form['servertext_input']
        
        user = discord.fetch_user()

        # Make MySQL connection
        conn = mysql.connect()
        cur = conn.cursor()
        # look in the database if the user has registered a server
        cur.execute("SELECT registered_by FROM servers WHERE registered_by = (%s)", (user.id))
        reg_by = cur.fetchall()
        cur.close()
        conn.commit()

        if reg_by:
            msg="You already have a server registered"
        # If the user dosnt have a server, insert the data from the form into the database
        else:
            #TODO add hcaptcha to the form
            cur = conn.cursor()
            # write data to database
            cur.execute("INSERT INTO servers(servername, serverurl, discordserverid, server_text, registered_by) VALUES (%s,%s,%s,%s,%s)", (servername_input, serverurl_input, discordid_input, servertext_input, user.id))
            cur.close()
            conn.commit()
            msg="Your server has been successfully registered"


    return render_template('dash_register.html', msg=msg)


@dash.route('/edit_server', methods=['POST', 'GET'])
@requires_authorization
def edit_server():
    
    msg=""

    user = discord.fetch_user()

    # Make MySQL connection
    conn = mysql.connect()
    conn.autocommit = True
    cur = conn.cursor()
    
    # get the data from the database to edit
    cur.execute('SELECT servername, serverurl, discordserverid, server_text, registered_by FROM servers WHERE registered_by = (%s)', (user.id))
    serverdata = cur.fetchall()
    cur.close()

    if request.method == 'POST' and 'servername_input' in request.form and 'serverurl_input' and 'discordid_input' and 'servertext_input' in request.form:
            
        servername_input =  request.form['servername_input']
        serverurl_input =  request.form['serverurl_input']
        discordid_input =  request.form['discordid_input']
        servertext_input =  request.form['servertext_input']
        
        cur = conn.cursor()
        # get the data from the database to edit
        cur.execute("UPDATE servers SET servername=%s, serverurl=%s, discordserverid=%s, server_text=%s WHERE registered_by=%s " %(servername_input, serverurl_input, discordid_input, servertext_input, user.id))
        conn.commit()

        msg="Your server information has been updated"
        return render_template('dash_serveredit.html', serverdata=serverdata, msg=msg)

    return render_template('dash_serveredit.html', serverdata=serverdata, msg=msg)


@dash.route('/vote_server')
@requires_authorization
def vote():
    msg=""
        
    return render_template('dash_vote.html')


@dash.route('/review',methods=['POST', 'GET'])
@requires_authorization
def review():
    msg=""

    if request.method == 'POST' and 'server_select' in request.form and 'review_text' in request.form:
        
        review_server = request.form['server_select']
        review_txt = request.form['review_text']
        

    return render_template('dash_review.html', msg=msg, )