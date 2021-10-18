from flask import Flask, render_template
from flask_discord import DiscordOAuth2Session
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


"""404"""
#TODO Create 404 page
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")