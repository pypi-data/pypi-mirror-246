from ..__const import Const


class MessageTypeConst(Const):
    TEXT_INTEGER = 'int'
    TEXT_STRING = 'str'
    TEXT_SPECIAL_CHARACTER = ''
    TYPE_TEXT = 'text'


class StringFormat(Const):
    REMOVE_ALL_CHARACTERS_EXCEPT_TEXT = r"[\n\t\s]+"
    FORMAT_AB_123_PATTERN = r'(\D+)(\d+)'
    FORMAT_AB_123_REPL = r'\1-\2'
