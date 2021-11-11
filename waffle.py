from quart import Quart, redirect, url_for, render_template
from quart_discord import DiscordOAuth2Session, Unauthorized
from quart_rate_limiter import RateLimiter
from nextcord.ext import commands
from decouple import config

import os

app = Quart(__name__)
rate_limiter = RateLimiter(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = config('OAUTHLIB_INSECURE_TRANSPORT')
app.secret_key = os.urandom(24)

app.config["DISCORD_CLIENT_ID"] = config('DISCORD_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = config('DISCORD_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = config('DISCORD_REDIRECT_URI')
app.config["DISCORD_BOT_TOKEN"] = config('DISCORD_BOT_TOKEN')

discord = DiscordOAuth2Session(app)

bot = commands.Bot(command_prefix=config('BOT_PREFIX'))
cogs = "./cogs"

# Load cogs (bot commands Thank you PyWhy)
tasks = []
for filename in os.listdir("./cogs"): # load cogs dirs :D
	if filename.endswith(".py"):
		try:
			bot.load_extension(f'cogs.{filename[:-3]}')
			print(f'Loaded {filename}')
		except Exception as e:
			tasks.append(f'Failed to load {filename}')
			print(f'[ERROR] {e}')


@bot.event
async def on_ready():
    print(f'{bot.user} connected to Discord!')

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
# voting api point to look if the user voted in the past 12h
from API.voted import voted
app.register_blueprint(voted,url_prefix='/api')

# List all registered servers
from API.servers import servers
app.register_blueprint(servers,url_prefix='/api')

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
    bot.loop.create_task(app.run_task(port=config('PORT'), debug=config('DEBUG'), host="0.0.0.0"))
    bot.run(config('DISCORD_BOT_TOKEN'))


