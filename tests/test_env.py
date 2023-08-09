"""
Test that env.example exists and it has the correct fields
"""
import os
from pathlib import Path

import pytest

this_file_path = os.path.dirname(__file__)
repo_root_dir_path = str(Path(this_file_path).resolve().parents[0])


def test_env():
    env_file_name = ".env.example"
    env_file_path = os.sep.join([repo_root_dir_path, env_file_name])
    assert os.path.exists(env_file_path) is True


def test_env_content():
    expected_env_content = {
        "DISCORD_BOT_TOKEN": "Discord Bot Token Here",
    }
    env_file_name = ".env.example"
    env_file_path = os.sep.join([repo_root_dir_path, env_file_name])
    try:
        with open(env_file_path, "r") as f:
            env_content = f.read()
            for key, value in expected_env_content.items():
                assert key in env_content
                assert value in env_content
    except pytest.fail as e:
        pytest.fail(f"Exception: {e}")
