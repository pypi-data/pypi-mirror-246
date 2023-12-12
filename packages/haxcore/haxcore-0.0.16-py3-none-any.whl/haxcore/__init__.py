"""Import the core methods and classes for HaX tool"""
# flake8: noqa

from os.path import dirname, realpath

from toml import loads as toml_load

from .classes.attacks.attack_manager import AttackManager
from .classes.attacks.enums import AttackType, RequestType
from .classes.crack.brute_force import BruteForce
from .classes.crack.crack_pass_manager import CrackPassManager
from .classes.crack.enums import CrackType, HashAlgorithm
from .classes.crack.password_rule import PasswordRule
from .classes.crack.rainbow import Rainbow
from .classes.crack.wordlist_rules import WordlistRules
from .classes.exception.database import SQLException
# import manager classes
from .utilities.config import CORE, CORE_DIR, DB, get_db_path, get_package_version
from .utilities.db.base import execuate, init_db
from .utilities.db.tbl_attack import get_all_attacks, get_attack_by_url, insert_attack, update_attack
from .utilities.db.tbl_setting import get_all_setting, get_setting_by_name, update_setting
from .utilities.log import LOGGER_FILE, LogLevel, init_log, log_msg

__version__ = get_package_version()
