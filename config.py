PG_USER = "postgres"
PG_PSSWRD = "nazar2415"
PG_HOST = "127.0.0.1"
PG_PORT = "5432"
PG_DATABASE = "food"

SECRET_KEY = '135f61d2fwe6523ada5651f'

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{PG_USER}:{PG_PSSWRD}@localhost/{PG_DATABASE}"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_USERNAME = 'xxxnazarkoxxx@gmail.com'
MAIL_PASSWORD = 'hvichzlggoazsniw'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False

FOLDER_TO_UPLOAD = 'static/images/profiles/'

API_KEY = 'RqP4PaFOvIjtix0Sdg0ddGKlBTe6Ryl41zcTAtSe'  # https://fdc.nal.usda.gov/
