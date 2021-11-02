from waffle import app

from decouple import config

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address, default_limits=["60 per minute", "1 per second"],)
limiter.init_app(app)