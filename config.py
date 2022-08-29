PG_USER = "postgres"
PG_PSSWRD = "nazar2415"
PG_HOST = "127.0.0.1"
PG_PORT = "5432"
PG_DATABASE = "food"

DATABASE_URL = 'postgresql://mndnusjyggiwvj:fe99a1c7b460e709520e0b6d1796590849362ac37af68923a2815e9c36cbaa7c@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/d2tsirtb3pcjm3'

SECRET_KEY = '135f61d2fwe6523ada5651f'

# SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{PG_USER}:{PG_PSSWRD}@localhost/{PG_DATABASE}"
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_USERNAME = 'xxxnazarkoxxx@gmail.com'
MAIL_PASSWORD = 'hvichzlggoazsniw'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False

FOLDER_TO_UPLOAD = 'static/images/profiles/'
FOLDER_TO_UPLOAD_RECIPES = 'static/images/recipes/'

API_KEY = 'RqP4PaFOvIjtix0Sdg0ddGKlBTe6Ryl41zcTAtSe'  # https://fdc.nal.usda.gov/
