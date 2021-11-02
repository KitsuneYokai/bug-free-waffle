from waffle import app
from decouple import config

from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = config('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = config('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = config('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = config('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_PORT'] = 3307

mysql.init_app(app)
