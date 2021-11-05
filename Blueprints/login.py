from quart import redirect, url_for, Blueprint

login = Blueprint('login', __name__)
from waffle import discord

# Login route
@login.route("/login/")
async def index():
    return await discord.create_session()


@login.route("/callback/")
async def callback():
    await discord.callback()
    return redirect(url_for("dash.index"))

# Logout route
@login.route("/logout")
async def logout():
    await discord.revoke()
    return redirect (url_for("index.home"))