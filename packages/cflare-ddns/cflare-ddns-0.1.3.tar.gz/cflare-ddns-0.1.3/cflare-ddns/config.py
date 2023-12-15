import json
import exceptions as ex


def parse(filename):
    # Load configuration from a JSON file
    with open(filename, "r") as json_file:
        config = json.load(json_file)

    if "api_key" not in config:
        raise ex.ConfigInvalidError("Config missing api_key")
    if "email" not in config:
        raise ex.ConfigInvalidError("Config missing email")
    if "records" not in config:
        raise ex.ConfigInvalidError("Config missing records")
    if type(config["records"]) is not list:
        raise ex.ConfigInvalidError("Invalid records")
    for item in config["records"]:
        if "zone_id" not in item:
            raise ex.ConfigInvalidError("Config missing zone_id")
        if "domain" not in item:
            raise ex.ConfigInvalidError("Config missing domain")
        if "record_name" not in item:
            raise ex.ConfigInvalidError("Config missing record_name")

    return config
