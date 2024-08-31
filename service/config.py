import os

from dotenv import load_dotenv


env_file_path = '.env'

load_dotenv(dotenv_path=env_file_path)

###################################################
DB_USER = os.getenv("POSTGRES_USER")  #
DB_PASS = os.getenv("POSTGRES_PASSWORD")  #
DB_NAME = os.getenv("POSTGRES_DB")  #
DB_PORT = os.getenv("POSTGRES_PORT")  #
DB_HOST = os.getenv("POSTGRES_HOST")  #
###################################################

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


###################################################
DB_USER_TEST = os.getenv("POSTGRES_TEST_USER")  #
DB_PASS_TEST = os.getenv("POSTGRES_TEST_PASSWORD")  #
DB_NAME_TEST = os.getenv("POSTGRES_TEST_DB")  #
DB_PORT_TEST = os.getenv("POSTGRES_TEST_PORT")  #
DB_HOST_TEST = os.getenv("POSTGRES_TEST_HOST")  #
###################################################

SQLALCHEMY_DATABASE_TEST_URL = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'




