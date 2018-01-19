from germine import models

from sqlalchemy.inspection import inspect
from sqlalchemy.exc import IntegrityError


def map_field_to_type(Model):
    inspector = inspect(Model)
    result = {}
    return {
        rel.class_attribute.key: rel.mapper.class_
        for rel in inspector.relationships
    }


def load_json(json, session):
    ModelClass = getattr(models, json["model"])

    for row in json["rows"]:
        instance = ModelClass()
        field_to_type = map_field_to_type(ModelClass)
        initial = {}
        for key, value in row.items():
            if type(value) is dict:
                AttributeClass = field_to_type[key]
                value = session.query(AttributeClass).filter_by(**value).one()
            initial[key] = value
        instance = ModelClass(**initial)
        session.add(instance)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(
                "Not adding '{}', because it would cause an integrity error:\n\t{}".
                format(instance, e)
            )
