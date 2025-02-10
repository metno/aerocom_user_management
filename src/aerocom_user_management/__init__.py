from importlib import metadata

__version__ = metadata.version(__package__)

# import aerocom_user_management.cli.aumn_manage_user
from . import const
from . import cli

