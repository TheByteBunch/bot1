import pytest
import os
from pathlib import Path
from configparser import ConfigParser

this_file_path = os.path.dirname(__file__)
repo_root_dir_path = str(Path(this_file_path).resolve().parents[0])


def test_config():
    config_file_name = "config.ini.example"
    config_file_path = os.sep.join([repo_root_dir_path, config_file_name])
    assert os.path.exists(config_file_path) is True


def test_config_content():
    try:
        config = ConfigParser()
        config_file_name = "config.ini.example"
        config_file_path = os.sep.join([repo_root_dir_path, config_file_name])
        config.read(config_file_path)

        # Check that the config file has the following items
        items_in_config = [
            "dev",
            "feature_flags",
        ]

        for item in items_in_config:
            assert item in config

        # Make sure that the feature flags are set to 0 except for init
        feature_flags = config["feature_flags"]
        feature_flags_dict = dict(feature_flags)
        for key, value in feature_flags_dict.items():
            if key == "init":
                continue
            assert value == "0"

        # Make sure that the dev section has the following items
        items_in_dev_section = {
            "guild_id": "Discord Guild ID",
            "user_id": "Discord User ID",
            "channel_id": "Discord Channel ID",
        }
        dev_section = config["dev"]
        dev_section_dict = dict(dev_section)
        for key, value in dev_section_dict.items():
            assert key in items_in_dev_section
            assert value == items_in_dev_section[key]

    except Exception as e:
        pytest.fail(f"Exception: {e}")
