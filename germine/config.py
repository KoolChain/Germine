import os


def file_dir():
    return os.path.dirname(os.path.abspath(__file__))


class Default:
    DEBUG = True
    SECRET_KEY = (
        "Q*0@+;W,`p-S_XzK{b*qn;-&xqTRN+;xZ#7T}"
        "<JgrUY^S'SlG:tOnKeK$THXZ~Q]Zj"
    )
    # Hardcode instance as the instance folder at the moment
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.realpath(
            os.path.join(file_dir(), "../instance/germine_dev.db")
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
