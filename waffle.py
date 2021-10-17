from flask import Flask, render_template, request, jsonify, make_response
from flask_discord import DiscordOAuth2Session
from decouple import config

import random
import time
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config["DISCORD_CLIENT_ID"] = config('DISCORD_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = config('DISCORD_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = config('DISCORD_REDIRECT_URI')
app.config["DISCORD_BOT_TOKEN"] = config('DISCORD_BOT_TOKEN')

discord = DiscordOAuth2Session(app)

#TODO let it get the data from the database
heading = "Test.server"

content = """
Testing the Test before the tester 
is getting tested by the testing testers 
that test testers testing testers
"""

db = list()
posts = 500 
quantity = 20 

for x in range(posts):

    heading_parts = heading.split(" ")
    random.shuffle(heading_parts)
    content_parts = content.split(" ")
    random.shuffle(content_parts)

    db.append([x, " ".join(heading_parts), " ".join(content_parts)])


"""importing Blueprints"""
# Dashboard Blueprint
from Blueprints.dash import dash
app.register_blueprint(dash)


from Blueprints.login import login
app.register_blueprint(login)


"""404"""
#TODO Create 404 page & error handler
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")


"""INDEX"""
@app.route('/')
def home():

    return render_template("index.html")


"""load the servers into the list"""
@app.route("/load")
async def load():
    time.sleep(0.2)
    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(db[0: quantity]), 200)
        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)
        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify(db[counter: counter + quantity]), 200)
    return await res


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")