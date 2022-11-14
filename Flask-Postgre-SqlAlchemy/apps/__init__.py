from config import Config
from apps.utils.utils import *
from apps.models import db

migration = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_CONNECTION_URI
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(DEBUG=True, JWT_SECRET_KEY="JVM Screat Key")

    db.init_app(app)
    migration.init_app(app, db)
    # db.create_all()
    return app
