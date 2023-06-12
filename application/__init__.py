from flask import Flask
from mongoengine import connect


def register_blueprints(app: Flask):
    from application.views.user_views import user_blueprint as user_app
    from application.views.post_views import post_blueprint as post_app
    from application.views.tag_views import tag_blueprint as tag_app

    app.register_blueprint(user_app)
    app.register_blueprint(post_app)
    app.register_blueprint(tag_app)


def create_db(app: Flask):
    connect(
        db=app.config['MONGODB_SETTINGS']['db'],
        host=app.config['MONGODB_SETTINGS']['host'],
        port=app.config['MONGODB_SETTINGS']['port']
    )


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'tumblelog',
        'host': 'localhost',
        'port': 27017
    }
    register_blueprints(app)
    create_db(app)
    return app
