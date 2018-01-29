from germine import models
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect


def map_field_to_type(Model):
    inspector = inspect(Model)
    return {
        rel.class_attribute.key: rel.mapper.class_
        for rel in inspector.relationships
    }


def load_json(json, session):
    if type(json) == dict:
        collection = [json] 
    else:
        collection = json

    for model in collection:
        print("Loading entries for model: {}".format(model["model"]))
        load_instance(model, session)
        

def _handle_value(value, session, key, field_to_type):
    if type(value) is list:
        value = [_handle_value(entry, session, key, field_to_type) for entry in value]
    elif type(value) is dict:
        AttributeClass = field_to_type[key]
        value = session.query(AttributeClass).filter_by(**value).one()
    return value


def load_instance(model_json, session):
    ModelClass = getattr(models, model_json["model"])

    for row in model_json["rows"]:
        field_to_type = map_field_to_type(ModelClass)
        initial = {}
        for key, value in row.items():
            initial[key] = _handle_value(value, session, key, field_to_type)
        instance = ModelClass(**initial)
        session.add(instance)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(
                "\tNot adding '{}', because it would cause an integrity error:"
                "\n\t\t{}".format(instance, e)
            )
