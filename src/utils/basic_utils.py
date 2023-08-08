from dotenv import load_dotenv
import os
from configparser import ConfigParser
from pathlib import Path

this_file_path = os.path.dirname(__file__)
repo_root_dir_path = str(Path(this_file_path).resolve().parents[1])


def parse_feature_flags():
    """
    Parse feature flags from the config.ini file
    :return:
    """

    # Create config parser
    config = ConfigParser()

    # Read the config file
    config_file_name = "config.ini"
    config_file_path = os.sep.join([repo_root_dir_path, config_file_name])
    config.read(config_file_path)

    # Get the feature flags
    feature_flags = config["feature_flags"]
    feature_flags_dict = dict(feature_flags)
    # Return the feature flags
    return feature_flags_dict


def get_user_id():
    config = ConfigParser()
    config_file_name = "config.ini"
    config_file_path = os.sep.join([repo_root_dir_path, config_file_name])
    config.read(config_file_path)
    return int(config["dev"]["user_id"])


def get_guild_id():
    config = ConfigParser()
    config_file_name = "config.ini"
    config_file_path = os.sep.join([repo_root_dir_path, config_file_name])
    config.read(config_file_path)
    return int(config["dev"]["guild_id"])


def get_secret_token():
    """
    Get secret token from .env file
    :return:
    """
    load_dotenv()
    return os.getenv("DISCORD_BOT_TOKEN")


def debug_object_fields(obj):
    """
    Print all fields in the object
    :param obj:
    :return:
    """
    for field in dir(obj):
        if field.startswith("_"):
            continue
        print(field, getattr(obj, field))


if __name__ == "__main__":
    print(parse_feature_flags())
