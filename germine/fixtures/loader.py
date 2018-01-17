from germine import models

def load_json(json, session):
    ModelClass = getattr(models, json["model"])
    for row in json["rows"]:
        session.add(ModelClass(**row))

    session.commit()

