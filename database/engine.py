from __future__ import annotations

from datetime import datetime

from inflection import pluralize
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, scoped_session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.pool import StaticPool
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer

from linebot.helpers.config import get_config_by_name

c = get_config_by_name("default")
engine = create_engine(
    "mysql://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
        user=c["db_user"],
        password=c["db_password"],
        host=c["db_host"],
        port=c["db_port"],
        database=c["db_database"],
        charset=c["db_charset"],
    ),
    poolclass=StaticPool,
)

Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        expire_on_commit=False,
        bind=engine,
    )
)


class BaseModel:
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(
        DateTime,
        default=datetime.now,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return pluralize(cls.__name__.lower())  # type: ignore[no-any-return, attr-defined]

    def create(self) -> None:
        with Session() as session:
            session.add(self)
            session.commit()

    def save(self) -> None:
        with Session() as session:
            session.commit()

    def delete(self) -> None:
        with Session() as session:
            session.delete(self)
            session.commit()


Base: DeclarativeMeta = declarative_base(cls=BaseModel)
