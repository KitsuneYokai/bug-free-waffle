from flask import Blueprint, render_template

serverpage = Blueprint('serverpage', __name__)

@serverpage.route("/server/")
def index():
    return render_template("servertemplate.html")