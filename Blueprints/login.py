from flask import redirect, url_for, Blueprint


login = Blueprint('login', __name__)
from waffle import discord


@login.route("/login/")
def index():
    return discord.create_session()


@login.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    return redirect(url_for("dash.index"))