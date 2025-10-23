import os
from flask import Flask
from config import Config
from controller.user_controller import UserController

app = Flask(__name__, template_folder=os.path.join('views', 'templates'))
app.config.from_object(Config)

app.add_url_rule('/', 'index', UserController.index)

if (__name__) == '__main__':
    app.run(debug=True)