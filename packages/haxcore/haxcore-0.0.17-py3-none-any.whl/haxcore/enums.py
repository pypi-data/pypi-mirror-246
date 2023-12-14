"""All enums in the package"""
from enum import Enum


class ConfigType(Enum):
  """Different confiuration files"""
  CORE = "core.yml"
  DB = "db.yml"
  LOG = "log.yml"


class Table(Enum):
  """All tables in the database"""
  SETTING = 1
  ATTACK = 2


class AttackType(Enum):
  """All attack types"""
  XSS = 1
  SQLI = 2


class RequestType(Enum):
  """All request types"""
  POST = 1
  GET = 2

  @classmethod
  def get_names(cls):
    """Get all enum names"""
    # pylint: disable=W0212,E1101
    return RequestType._member_names_


class CrackType(Enum):
  """All attack types"""
  RAINBOW = 1
  BRUTE_FORCE = 2

  @classmethod
  def get_names(cls):
    """Get all enum names"""
    # pylint: disable=W0212,E1101
    return CrackType._member_names_


class ManglingOptions(Enum):
  """All attack types"""
  DOUBLE = 1
  CAPITALIZE = 2

  @classmethod
  def get_names(cls):
    """Get all enum names"""
    # pylint: disable=W0212,E1101
    return ManglingOptions._member_names_


class HashAlgorithm(Enum):
  """Supported hash algorithms"""
  MD5 = 1
  SHA256 = 2
  BCRYPT = 3

  @classmethod
  def get_names(cls):
    """Get all enum names"""
    # pylint: disable=W0212,E1101
    return HashAlgorithm._member_names_
