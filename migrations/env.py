import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers based on the .ini file.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    """
    This function attempts to get the engine from Flask-SQLAlchemy (for both older and newer versions).
    """
    try:
        # This works with Flask-SQLAlchemy < 3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # This works with Flask-SQLAlchemy >= 3
        return current_app.extensions['migrate'].db.engine

def get_engine_url():
    """
    This function retrieves the engine's URL as a string for use in the Alembic config.
    """
    try:
        # Get the URL and hide the password for security purposes
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        # Return URL string directly in case of an error
        return str(get_engine().url).replace('%', '%%')

# Use the engine URL for the sqlalchemy.url in config
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# Optionally, add custom metadata for auto-generating migrations
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# Other configuration options (optional, can be used for specific cases)
# my_important_option = config.get_main_option("my_important_option")

# Example of logging at various levels (this can be customized)
logger.debug("Alembic migration environment initialized.")
logger.info(f"Using SQLAlchemy URL: {get_engine_url()}")
logger.warning("If you see this message, it could indicate a potential issue.")

# The rest of the migration environment setup can follow here.

