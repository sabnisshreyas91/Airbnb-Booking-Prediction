import os
import sqlalchemy as sql
import config

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker


def create_db(engine=None, engine_string=None):
    """Creates a database with the data models inherited from `Base` (Tweet and TweetScore).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = sql.create_engine(engine_string)


def create_schema():
    Base = declarative_base()
    if config.RDS_FLAG == 'T':
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = config.RDS_HOST
        port = config.RDS_PORT
        databasename = config.MYSQL_DB
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, databasename)
        engine = sql.create_engine(engine_string)
    else:
        engine = sql.create_engine(config.SQLITE_DATABASE_URI)
        create_db(engine_string=config.SQLITE_DATABASE_URI)

    class UserInput(Base):
        """Create a data model for the database to be set up for capturing songs """
        __tablename__ = 'User_Input'
        id = Column(Integer, primary_key=True)
        age = Column(Integer, unique=False, nullable=False)
        Gender = Column(String(100), unique=False, nullable=False)
        Preffered_Destination = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<UserInput %r>' % self.title
        
    Base.metadata.create_all(engine)
