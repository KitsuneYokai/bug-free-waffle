from flask import render_template, request, redirect, url_for, Blueprint
from flask_discord import Unauthorized, requires_authorization
from decouple import config


dash = Blueprint('dash', __name__)

from waffle import discord
from db import mysql
from hcaptcha import hcaptcha

hsitekey = config('HCAPTCHA_SITE_KEY')


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
async def reg_server():
    msg=""
    if request.method == 'POST' and 'servername_input' in request.form and 'serverurl_input' and 'discordid_input' and 'servertext_input' in request.form:
            
        servername_input =  request.form['servername_input']
        serverurl_input =  request.form['serverurl_input']
        discordid_input =  request.form['discordid_input']
        servertext_input =  request.form['servertext_input']
        
        if hcaptcha.verify():
            user = discord.fetch_user()

            # Make MySQL connection
            conn = mysql.connect()
            cur = conn.cursor()
            # look in the database if the user has registered a server
            cur.execute("SELECT registered_by FROM servers WHERE registered_by = (%s)", (user.id))
            reg_by = cur.fetchall()
            cur.close()

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
        
        else:
            msg="Please solve the captcha!"


    return render_template('dash_register.html', msg=msg, hsitekey=hsitekey)


@dash.route('/edit_server', methods=['POST', 'GET'])
@requires_authorization
def edit_server():
    msg=""

    user = discord.fetch_user()

    # Make MySQL connection
    conn = mysql.connect()
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
        
        if hcaptcha.verify():
        
            cur = conn.cursor()
            # Edit the data
            cur.execute("UPDATE servers SET servername=%s, serverurl=%s, discordserverid=%s, server_text=%s WHERE registered_by=%s " %(servername_input, serverurl_input, discordid_input, servertext_input, user.id))
            conn.commit()

            msg="Your server information has been updated"
        
        else:
            msg="Please solve the captcha!"

    return render_template('dash_serveredit.html', serverdata=serverdata, msg=msg, hsitekey=hsitekey)


@dash.route('/vote_server', methods=['POST', 'GET'])
@requires_authorization
def vote():
    msg=""
    
    conn = mysql.connect()
    cur = conn.cursor()
    
    # Get servernames and to insert into the form
    cur.execute('SELECT servername FROM servers')
    serverdata = cur.fetchall()
    cur.close()

    if request.method == 'POST' and 'chose_server' in request.form:
        
        chose_server =  request.form['chose_server']

        user = discord.fetch_user()

        if hcaptcha.verify():

            # Delete voter database entry if the vote is older than 12 h
            cur = conn.cursor()
            cur.execute("DELETE FROM `user_votes` WHERE `voted_time` < ADDDATE(NOW(), INTERVAL -12 HOUR)")
            cur.close()
            conn.commit()

            cur = conn.cursor()
            # look if the user is in the vote database
            cur.execute("SELECT voted, voted_time FROM user_votes WHERE dcuserid = (%s)", (user.id))
            voted = cur.fetchall()
            cur.close()

            if voted:
                msg="You already voted in the past 12h"

            else:
                cur = conn.cursor()
                # if the user is not deleted by votes.py insert data / vote
                cur.execute('UPDATE servers SET votes = votes + 1 WHERE servername = %s',(chose_server))
                cur.close()
                conn.commit()

                cur = conn.cursor()
                cur.execute("INSERT INTO user_votes(dcuserid, voted, voted_time) VALUES (%s,%s, CURRENT_TIMESTAMP)", (user.id, chose_server))
                cur.close()
                conn.commit()

                msg="Your successfully voted for your favorite server"
        
        else:
            msg="Please solve the captcha!"

    return render_template('dash_vote.html', serverdata=serverdata, msg=msg, hsitekey=hsitekey)


@dash.route('/review',methods=['POST', 'GET'])
@requires_authorization
def review():
    msg=""

    if request.method == 'POST' and 'server_select' in request.form and 'review_text' in request.form:
        
        review_server = request.form['server_select']
        review_txt = request.form['review_text']
        

    return render_template('dash_review.html', msg=msg, hsitekey=hsitekey)