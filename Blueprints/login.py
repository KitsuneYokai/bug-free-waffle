from flask import redirect, url_for, Blueprint


login = Blueprint('login', __name__)
from waffle import discord

# Login route
@login.route("/login/")
def index():
    return discord.create_session()


@login.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for("dash.index"))

# Logout route
@login.route("/logout")
def logout():
    discord.revoke()
    return redirect (url_for("index.home"))