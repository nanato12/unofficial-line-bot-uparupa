from typing import Any

from database.engine import Session


def bulk_create(objects: list[Any]) -> None:
    with Session() as session:
        session.bulk_save_objects(objects)
        session.commit()
