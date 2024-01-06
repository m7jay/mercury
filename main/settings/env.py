import environ
from pathlib import Path

env = environ.Env()


def get_csv_list(value: str):
    return value.split(",")


# read environment variables
env.read_env(Path(__file__).resolve().parent.parent.parent.joinpath(".env"))

# django
DEBUG = env.get_value("DEBUG")
SECRET_KEY = env.get_value("SECRET_KEY")
ALLOWED_HOSTS = get_csv_list(env.get_value("ALLOWED_HOSTS"))

# database
DB_HOST = env.get_value("DB_HOST")
DB_NAME = env.get_value("DB_NAME")
DB_USER = env.get_value("DB_USER")
DB_PASSWORD = env.get_value("DB_PASSWORD")
