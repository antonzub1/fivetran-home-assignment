import csv
from functools import partial
from pathlib import Path

from alembic import command
from alembic.config import Config
import dotenv
from pytest import fixture
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists


env = dotenv.dotenv_values()

@fixture
def alembic_config_path():
    return str((Path(__file__).parent / ".." / "migrations/alembic.ini").absolute())

@fixture
def alembic_config(alembic_config_path):
    alembic_cfg = Config()
    return Config(alembic_config_path)

@fixture(scope="function")
def alembic_client(alembic_config, alembic_config_path):
    # We must cleanup a database after each test
    # That's why we yield command runner and run downgrade after each test execution
    yield command
    command.downgrade(alembic_config, 'base')

@fixture(scope="session")
def db_url():
    return (
        f"postgresql+psycopg://{env['POSTGRES_USER']}:{env['POSTGRES_PASSWORD']}"
        f"@{env['POSTGRES_HOST']}:{env['POSTGRES_PORT']}/{env['POSTGRES_DB']}"
    )

@fixture(scope="session")
def engine(db_url):
    engine = create_engine(db_url, pool_size=20, echo=False)
    return engine

@fixture(scope="session")
def connection(db_url, engine):
    if not database_exists(db_url):
        create_database(db_url)

    yield engine.connect()

# @fixture(scope="session")
# def setup_database(connection):
#     Base.metadata.bind = connection
#     Base.metadata.create_all(Base.metadata.bind)

#     yield

#     Base.metadata.drop_all(Base.metadata.bind)


@fixture(scope="function", autouse=True)
def db_session(connection):
    transaction = connection.begin()

    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


@fixture(scope="session")
def inspector(engine):
    return inspect(engine)

@fixture
def data():
    with open("tests/data.csv", "r") as data:
        records = csv.DictReader(data)
        yield records
