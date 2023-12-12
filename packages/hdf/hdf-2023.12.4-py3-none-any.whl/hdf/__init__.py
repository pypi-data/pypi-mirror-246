import importlib

from flask import Flask
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from hdf.config import Config


try:
    import pkg_resources

    __distr__ = pkg_resources.get_distribution("hdf")
    __version__ = __distr__.version
except ImportError:
    __version__ = "n/a"


db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    ma.init_app(app)

    # Create `app.hdf_apps`
    if not hasattr(app, "hdf_apps"):
        app.hdf_apps = {}

    # Automatically load the applications listed in the config file
    for pkg_name, pkg_class in app.config.get("HDF_APPS", []):
        if pkg_name not in app.hdf_apps:
            pkg_instance = importlib.import_module(pkg_name)
            pkg_object = getattr(pkg_instance, pkg_class)
            pkg_object(app)

    @app.get("/")
    def index():
        return f"""
        <!doctype html>
        <html lang="en">
            <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <!-- Bootstrap CSS -->
                <link href="//cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

                <title>HDF</title>
            </head>
            <body>
                <p class="text-center">HDF {__version__}</p>

                <!-- Option 1: Bootstrap Bundle with Popper -->
                <script src="//cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
            </body>
        </html>
        """

    return app
