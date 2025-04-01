class Config:
    SECRET_KEY = "your_jwt_secret"
    WTF_CSRF_ENABLED = False
    SJWT_SECRET_KEY = "your_jwt_secret"
    JWT_ACCESS_TOKEN_EXPIRES = 3600 
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:97082@localhost/IIITK"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
