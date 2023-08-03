# Discord bot functions

## Table of Contents

1. Role bot
2. Table bot
3. Event bot
4. Git bot


## Role bot

### Description

This bot is used to manage roles on the server. It can add and remove roles from users based on reactions.

### Features

- Admin can call the bot to create new message of roles that users can react to (with `/create_role_message`)
- Admin can edit the roles in the message (with `/edit_role_message`)
- Admin can remove the message (with `/delete_role_message`)
- Users can react to the message to get the role
- Users can remove the role by removing their reaction

### TODO

- [x] Create new role message
- [ ] Add role based on reaction
- [ ] Remove role based on reaction
- [ ] Remove new role message
- [ ] Edit role message
- [ ] Make code more clean with comments and docstrings
- [ ] Move code to separate files
- 