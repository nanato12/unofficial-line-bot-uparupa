from __future__ import annotations

from datetime import datetime

from inflection import pluralize
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, scoped_session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer

from linebot.parser import ConfigParser

c = ConfigParser.get_config_by_name("default")
engine = create_engine(
    "mysql://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
        user=c["db_user"],
        password=c["db_password"],
        host=c["db_host"],
        port=c["db_port"],
        database=c["db_database"],
        charset=c["db_charset"],
    )
)

Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=engine,
    )
)


class BaseModel:
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return pluralize(cls.__name__.lower())  # type: ignore

    def save(self) -> None:
        with Session() as session:
            session.add(self)
            session.commit()


Base: DeclarativeMeta = declarative_base(cls=BaseModel)
