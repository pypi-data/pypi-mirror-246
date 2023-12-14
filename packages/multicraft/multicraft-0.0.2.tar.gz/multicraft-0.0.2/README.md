# multicraft

[![PyPI](https://img.shields.io/pypi/v/multicraft)](https://pypi.org/project/multicraft/)
[![Python](https://img.shields.io/pypi/pyversions/multicraft)](https://www.python.org/downloads/)
![Downloads](https://img.shields.io/pypi/dm/multicraft)
![Status](https://img.shields.io/pypi/status/multicraft)
[![Issues](https://img.shields.io/github/issues/legopitstop/multicraft-py)](https://github.com/legopitstop/multicraft-py/issues)

Interact with your Minecraft server from hosts that use [Multicraft](https://www.multicraft.org/) using Python.

## Installation
Install the module with pip:
```bat
pip3 install multicraft
```
Update existing installation: `pip3 install multicraft --upgrade`

## Features
- Includes a handful of common multicraft hosts.
- Manage users, players, commands, schedules, and databases.
- Start, stop, or restart your server.
- Run console commands (give, kill, whitelist, op, etc)
- Read your servers current cpu and memmory usage.
- Send a chat message.

See the [docs](https://github.com/legopitstop/multicraft-py/wiki) for more information.

## Dependencies
|Name|Description|
|--|--|
|[requests](https://pypi.org/project/requests/) | Requests is a simple, yet elegant, HTTP library. |

## Example
```py
from multicraft import MulticraftAPI

api = MulticraftAPI(
    url = 'https://localhost/api.php',
    user = 'username',
    key = 'apiKey'
)

owner = api.get_user_id(api.user)

owned_servers = api.list_servers_by_owner(owner)
print(owned_servers)

for id in owned_servers.keys():
    server = api.get_server(id)
    print(server)
```