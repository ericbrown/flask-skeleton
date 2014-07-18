#!/usr/bin/env python

"""
Usage: ./manage.py [submanager] <command>
Manage script for development. Type ./manage.py for more info

Commands:
- runserver <args>  : Runs the Flask development server. Accepts additional args like host and port
- shell             : Loads an interactive python shell with app, db, and models imported
- routes            : Shows all registered routes
- db <command>      : Runs database commands. See data/manager.py for more details
"""
def import_env():
    import os
    if os.path.exists('.env'):
        print 'Importing environment from .env...'
        for line in open('.env'):
            var = line.strip().split('=', 1)
            if len(var) == 2:
                os.environ[var[0]] = var[1]

import_env()

from flask_script import Manager
from flask_script.commands import ShowUrls
from flask_migrate import MigrateCommand

from src.app import create_app
from src.settings import app_config
from src.data.base import Base
from src.data.database import db
from src.data import models

app = create_app(app_config)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command("routes", ShowUrls())

@manager.shell
def make_context_shell():
    # Loads all the models which inherit from Base
    models_map = {name: cls for name, cls in models.__dict__.items() if isinstance(cls, type(Base))}
    return dict(app=app, db=db, **models_map)

@manager.command
def test_email():
    from flask_mail import Mail, Message
    mail = Mail(app)
    msg = Message(subject='test subject', recipients=[app.config['TEST_RECIPIENT']])
    msg.body = 'text body'
    msg.html = '<b>HTML</b> body'
    with app.app_context():
        mail.send(msg)

if __name__ == '__main__':
    manager.run()
