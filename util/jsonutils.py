import json


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if not isinstance(obj, dict):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)


def collection_to_json(obj):
    return json.dumps(obj, cls=SetEncoder)


def from_json(obj):
    return json.loads(obj)
