from flask import Flask, render_template, redirect, url_for
from flask_discord import DiscordOAuth2Session, Unauthorized
# Todo Look @ line 69
# from functools import partial
# from threading import Thread
# from nextcord.ext import commands

from decouple import config

import os


app = Flask(__name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = config('OAUTHLIB_INSECURE_TRANSPORT')
app.secret_key = os.urandom(24)

app.config["DISCORD_CLIENT_ID"] = config('DISCORD_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = config('DISCORD_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = config('DISCORD_REDIRECT_URI')
app.config["DISCORD_BOT_TOKEN"] = config('DISCORD_BOT_TOKEN')

discord = DiscordOAuth2Session(app)


# TODO look at line 69 (>_<)
#
# bot = commands.Bot(command_prefix=config('BOT_PREFIX'))
# 
# @bot.event
# async def on_ready():
#     print(f'{bot.user} has connected to Discord!')


"""importing Blueprints"""
# Dashboard Blueprint
from Blueprints.dash import dash
app.register_blueprint(dash)

# Login Blueprint
from Blueprints.login import login
app.register_blueprint(login)

# Server pages
from Blueprints.serverpage import serverpage
app.register_blueprint(serverpage)

# index
from Blueprints.index import index
app.register_blueprint(index)

"""Importing API"""
#voting api point to look if the user voted in the past 12h
from API.voted import voted
app.register_blueprint(voted,url_prefix='/api')

"""404"""
#TODO Create 404 page
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")

"""Auth handler"""
@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login.index"))

if __name__ == "__main__":
    app.run(port=config('PORT'), debug=config('DEBUG'), host="0.0.0.0")


# Will be used then converted to quart to start a bot instance with it
# 
# bot.run(config('DISCORD_BOT_TOKEN'))
# bot.loop.create_task(app.run(port=config('PORT'), debug=config('DEBUG'), host="0.0.0.0"))

