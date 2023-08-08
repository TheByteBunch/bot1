[![GitHub Super-Linter](https://github.com/Al1babax/bot1/actions/workflows/linter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)
# bot1

# Table of Contents
- Overview
- Setup instructions
- Discord bot functions


## Overview
This is a Discord bot for and by The Byte Bunch. It will be deployed in that Discord server.

## Setup Instructions
- Prerequisites
  - A Discord Bot, and a token for this bot
  - A server to which you can invite this bot
  - Your bot should be in that server, and should have the following positions: read and write messages, manage roles.
- clone this repo
- create and activate virtual environment and install pip dependencies
- Setup up credentials and configuration
  - Copy `.env.example` to `.env`
  - Edit `.env` to include your real Discord bot token
  - Copy `config.ini.example` to `config.ini`
  - Edit `config.ini` to contain your Guild_id, Channel_id, and User_id
  - Edit `config.ini` to set feature flags to `1` for the features you would like to use
- Run the bot
  - `python src/main.py`
- Running the tests:
  - `python -m pytest tests/`
  - Note: this must be run from the root directory of the repository.
## Discord bot functions



1. Role bot
2. Table bot
3. Event bot
4. Git bot


## Role bot

### Description

This bot is used to manage roles on the server. It can add and remove roles from users based on reactions.

### Features

- Admin can call the bot to create new message of roles that users can react to (with `/create_role_message`)
- Admin can add new role to the message (with `/add_role`)
- Admin can remove role from the message (with `/remove_role`)
- Users can react to the message to get the role
- Users can remove the role by removing their reaction

### TODO

- [x] Create new role message
- [x] Add role based on reaction
- [x] Remove role based on reaction
- [x] Edit role message
- [x] Make code more clean with comments and docstrings
- [x] Move code to separate files


## Table bot

### Description

This bot is used to manage tables on the server. It can create new tables and add users to them with information.

### Features

- Admin can call the bot to create new table (with `/create_member_table`)
- Admin can add users info to the table (with `/add_body`)
- Admin can add headers to the table (with `/remove_header`)

### TODO

- [x] Create new table
- [x] Add user info to table
- [x] Add headers to table
- [ ] Remove user from table
- [ ] Remove headers from table
- [ ] Multiple tables
