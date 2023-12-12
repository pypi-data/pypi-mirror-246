"""All enums in the app"""
from enum import Enum


class ConfigType(Enum):
  """Different confiuration files"""
  CORE = "core.yml"
  DB = "db.yml"
  LOG = "log.yml"
