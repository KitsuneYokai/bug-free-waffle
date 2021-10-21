from waffle import app
from flask_hcaptcha import hCaptcha
from decouple import config

hcaptcha = hCaptcha()
app.config["HCAPTCHA_ENABLED"] = config('HCAPTCHA_ENABLED')
app.config["HCAPTCHA_SITE_KEY"] = config('HCAPTCHA_SITE_KEY')
app.config["HCAPTCHA_SECRET_KEY"] = config('HCAPTCHA_SECRET_KEY')
hcaptcha.init_app(app)