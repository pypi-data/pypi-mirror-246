""""load all application configuration files (YAML format)"""
from os import makedirs
from os.path import dirname, exists, join

from yaml import safe_load

from haxcore.classes.enums import ConfigType
from haxcore.classes.exception.application import ConfigException

CORE_DIR = dirname(dirname(__file__))


def load_config(config_type) -> dict:
  """Load specific configuration file"""
  file_path = join(CORE_DIR, "assets", ".config", config_type.value)
  if exists(file_path):
    with open(file_path, encoding="UTF-8") as config:
      data: dict = safe_load(config)
      return data
  raise FileNotFoundError(f"Application {config_type.value} config file not found in path: {file_path}")


CORE = load_config(ConfigType.CORE)
DB = load_config(ConfigType.DB)  # pylint: disable=invalid-name
LOG = load_config(ConfigType.LOG)


def get_db_path():
  """get the application database path"""
  if "name" in DB:
    db_path = join(CORE_DIR, "assets", DB["name"])
    if not exists(dirname(db_path)):
      makedirs(dirname(db_path))
    return db_path
  raise ConfigException("db")


def get_package_version():
  """get the package version"""
  if "version" in CORE:
    return CORE["version"]
  raise ConfigException("version")
