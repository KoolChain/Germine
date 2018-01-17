class Default:
    DEBUG = True
    SECRET_KEY = "Q*0@+;W,`p-S_XzK{b*qn;-&xqTRN+;xZ#7T}<JgrUY^S'SlG:tOnKeK$THXZ~Q]Zj"
    # Hardcode instance as the instance folder at the moment
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/germine_dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

