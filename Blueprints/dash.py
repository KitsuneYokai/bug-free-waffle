# imports
from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_discord import Unauthorized, requires_authorization
from decouple import config


dash = Blueprint('dash', __name__)


# imports from py
from waffle import discord
from db import mysql
from hcaptcha import hcaptcha


hsitekey = config('HCAPTCHA_SITE_KEY')


@dash.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login.index"))


"""routes/Dashboard"""
@dash.route('/dash',)
@requires_authorization
def index():
    return render_template('dashboard.html')


# Register your server to the site   
@dash.route('/register_server', methods=["GET","POST"])
def reg_server():
    # Variables
    user = discord.fetch_user()
    msg=""
    conn = mysql.connect()

    cur = conn.cursor()
    # look in the database if the user has registered a server
    cur.execute("SELECT registered_by FROM servers WHERE registered_by = (%s)", (user.id))
    reg_by = cur.fetchall()
    cur.close()

    if request.method == 'POST' and 'servername_input' in request.form and 'serverurl_input' and 'discordid_input' and 'servertext_input' in request.form:

        servername_input =  request.form['servername_input']
        serverurl_input =  request.form['serverurl_input']
        discordid_input =  request.form['discordid_input']
        servertext_input =  request.form['servertext_input']

        if hcaptcha.verify():

            if reg_by:
                flash("You already have a server registered")
                return redirect (url_for("dash.index"))

            # If the user dosnt have a server, insert the data from the form into the database
            else:
                cur = conn.cursor()
                # write data to database
                cur.execute("INSERT INTO servers(servername, serverurl, discordserverid, server_text, registered_by, votes) VALUES (%s,%s,%s,%s,%s,0)", (servername_input, serverurl_input, discordid_input, servertext_input, user.id))
                cur.close()
                conn.commit()

                flash("Your server has been successfully registered")
                return redirect (url_for("dash.index"))

        else:
            msg="Please solve the captcha!"

    return render_template('dash_register.html', msg=msg, hsitekey=hsitekey)


# Edit your server
@dash.route('/edit_server', methods=['POST', 'GET'])
@requires_authorization
def edit_server():
    # Variables
    user = discord.fetch_user()
    msg=""
    conn = mysql.connect()

    cur = conn.cursor()
    # get the data from the database to edit
    cur.execute('SELECT * FROM servers WHERE registered_by = (%s)', (user.id))
    serverdata = cur.fetchall()
    cur.close()

    if serverdata:
        if request.method == 'POST' and 'servername_input' in request.form and 'serverurl_input' and 'discordid_input' and 'servertext_input' in request.form:

            servername_input =  request.form['servername_input']
            serverurl_input =  request.form['serverurl_input']
            discordid_input =  request.form['discordid_input']
            servertext_input =  request.form['servertext_input']

            if hcaptcha.verify():

                cur = conn.cursor()
                # Edit the data
                cur.execute("UPDATE servers SET servername=%s, serverurl=%s, discordserverid=%s, server_text=%s WHERE registered_by=%s",(servername_input, serverurl_input, discordid_input, servertext_input, user.id))
                cur.close()
                conn.commit()

                flash("Your server information has been updated")
                return redirect (url_for("dash.index"))

            else:
                msg="Please solve the captcha!"

    else:
        flash("you don't have a server registered. register a server in order to edit it. makes sense right?")
        return redirect (url_for("dash.index"))

    return render_template('dash_serveredit.html', serverdata=serverdata, msg=msg, hsitekey=hsitekey)


# Vote for your favorite server
@dash.route('/vote_server', methods=['POST', 'GET'])
@requires_authorization
def vote():
    # Variables
    user = discord.fetch_user()
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

        if request.method == 'POST' and 'choose_server' in request.form:

            chose_server =  request.form['choose_server']

            if hcaptcha.verify():

                cur = conn.cursor()
                # if the user is not deleted by line 130 insert data / vote
                cur.execute('UPDATE servers SET votes = votes + 1 WHERE servername = %s',(chose_server))
                cur.close()
                conn.commit()

                cur = conn.cursor()
                cur.execute("INSERT INTO user_votes(dcuserid, voted, voted_time) VALUES (%s,%s, CURRENT_TIMESTAMP)", (user.id, chose_server))
                cur.close()
                conn.commit()

                flash("Your successfully voted for your favorite server")
                return redirect (url_for("dash.index"))

            else:
                msg="Please solve the captcha!"

    return render_template('dash_vote.html', serverdata=serverdata, msg=msg, hsitekey=hsitekey)


# write a review for a server
@dash.route('/review',methods=['POST', 'GET'])
@requires_authorization
def review():
    # Variables
    user = discord.fetch_user()
    msg=""
    conn = mysql.connect()

    cur = conn.cursor()
    # Get servernames to insert into the form
    cur.execute('SELECT servername, serverid FROM servers')
    serverdata = cur.fetchall()
    cur.close()

    if request.method == 'POST' and 'choose_server' in request.form and 'server_text' in request.form and 'serverid' in request.form:

        serverid = request.form['serverid']
        review_server = request.form['choose_server']
        review_txt = request.form['server_text']

        if hcaptcha.verify():

            cur = conn.cursor()
            # look if the user already wrote a review for that server
            cur.execute("SELECT * FROM reviews WHERE dcuserid = %s and serverid = %s", (user.id, serverid))
            revserver = cur.fetchall()
            cur.close()

            if revserver:
                flash("you already reviewed that server, and reviews are final. (RIP)")
                return redirect (url_for("dash.index"))

            else:
                # Insert data into the database
                cur = conn.cursor()
                cur.execute("INSERT INTO reviews(servername, revtext, dcuserid, revat, serverid) VALUES (%s,%s,%s,CURRENT_TIMESTAMP,%s)", (review_server, review_txt, user.id, serverid))
                cur.close()
                conn.commit()

                flash("Your review has been submitted and has now a chance to be shown on the serverpage")
                return redirect (url_for("dash.index"))

        else:
            msg="Please solve the captcha"

    return render_template('dash_review.html', msg=msg, hsitekey=hsitekey, serverdata=serverdata)


# Route to deleat the server from the Database
@dash.route('/delete_server/<servers>',methods=['POST'])
@requires_authorization
def delete_server(servers):
    # Variables
    user = discord.fetch_user()
    msg=""
    conn = mysql.connect()

    if hcaptcha.verify():

        if request.method == 'POST' and 'serverid' in request.form:

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

                flash("Bye Bye server. It was a nice time")
                return redirect (url_for("dash.index"))

        else:
            msg="What da fuq are you doing?"

    else:
        msg="Please solve the captcha!"

    return redirect (url_for("dash.index", msg=msg))