import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # HDF default settings
    HDF_APPS = [
        # ("pkg_name", "pkg_class"),
        # ("hdf_appname", "Appname"),
    ]

    # Database default settings
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "hdf.db")
    )

    # Mail default settings
