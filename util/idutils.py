import uuid


def generate_id(name):
    return uuid.uuid5(uuid.NAMESPACE_DNS, name).hex
