from dotenv import load_dotenv
import os

def get_secret_token():
    """
    Get secret token from .env file
    :return:
    """
    load_dotenv()
    BOT_SECRET_KEY = os.getenv('DISCORD_BOT_TOKEN')
    return BOT_SECRET_KEY


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