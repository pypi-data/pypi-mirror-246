"""different methods to support wordlist operations"""

from ..crack.wordlist_rules import WordlistRules


def load_wordlist(file_path: str, rules: WordlistRules):
  """Load the wordlist from a file"""
  if rules:
    pass
  with open(file_path, "r", encoding="UTF-8") as wordlist_file:
    return [word.strip("\n") for word in wordlist_file.readlines()]
