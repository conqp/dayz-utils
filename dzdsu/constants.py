"""Common constants."""

from os import environ, name
from pathlib import Path


__all__ = [
    'CONFIG_FILE',
    'DAYZ_APP_ID',
    'DAYZ_SERVER_APP_ID',
    'JSON_FILE',
    'KEYS_GLOB',
    'LINK',
    'MODS_BASE_DIR',
    'SERVER_BINARY',
    'STEAMCMD',
    'WORKSHOP_URL'
]


CONFIG_FILE = 'serverDZ.cfg'
DAYZ_APP_ID = 221100
DAYZ_SERVER_APP_ID = 223350
KEYS_GLOB = f'{DAYZ_APP_ID}/*/[Kk]eys/*.bikey'
LINK = '\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\\n'
MODS_BASE_DIR = Path('steamapps/workshop/content/')
WORKSHOP_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id={}'

if name == 'nt':
    JSON_FILE = Path(environ.get('PROGRAMFILES')) / 'dzsrv' / 'servers.json'
    SERVER_BINARY = 'DayZServer_x64.exe'
elif name == 'posix':
    JSON_FILE = Path('/etc/dzservers.json')
    SERVER_BINARY = 'DayZServer'
else:
    raise OSError('Unsupported operating system.')


STEAMCMD = 'steamcmd'
