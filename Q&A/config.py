
SECRET_KEY = "hxuoanfohgasohoqnve"

# 配置数据库信息
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'zhiliaooa'
USERNAME = 'root'
PASSWORD = 'root'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)


# 邮箱配置

MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2337051839@qq.com"
MAIL_PASSWORD = "iwkgntahvyigdibb"
MAIL_DEFAULT_SENDER = "2337051839@qq.com"