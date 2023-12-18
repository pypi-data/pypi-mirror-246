import random
import re
import string
import base64
import hashlib
import ast

from cores.const.common import CommonTypeUsageConst, StringFormat


class StringUtil:

    @staticmethod
    def generate_random_number(length: int = 5) -> int:
        """
        Example: 12312312312
        """
        text = ""
        for _ in range(length):
            text += f"{random.choice(string.digits)}"
        return int(text)

    @staticmethod
    def generate_random_string(number_words: int = 5, is_contain_space: bool = False, is_upper_case: bool = False) -> str:
        text = ""
        alphabet = string.ascii_lowercase if not is_upper_case else string.ascii_uppercase

        if is_contain_space:
            for _ in range(number_words):
                new_length = random.randrange(1, number_words)
                text += ''.join(random.choice(alphabet)
                                for _ in range(new_length)) + ' '
        else:
            text = ''.join(random.choice(alphabet)
                           for _ in range(number_words))
        return text

    @staticmethod
    def generate_random_number_string(number_words: int = 5, is_contain_space: bool = False, is_upper_case: bool = False) -> str:
        text = ""
        alphabet = string.ascii_lowercase if not is_upper_case else string.ascii_uppercase
        number = string.digits

        if is_contain_space:
            for _ in range(number_words):
                new_length = random.randrange(1, number_words)
                text += ''.join(random.choice(alphabet) + random.choice(number)
                                for _ in range(new_length)) + ' '
        else:
            text = ''.join(random.choice(alphabet) + random.choice(number)
                           for _ in range(number_words))[:number_words]
        return text

    @staticmethod
    def generate_random_special_characters(number_words: int = 5, is_contain_space: bool = False) -> str:
        text = ""
        alphabet = string.punctuation
        number = string.digits

        if is_contain_space:
            for _ in range(number_words):
                new_length = random.randrange(1, number_words)
                text += ''.join(random.choice(alphabet) + random.choice(number)
                                for _ in range(new_length)) + ' '
        else:
            text = ''.join(random.choice(alphabet) + random.choice(number)
                           for _ in range(number_words))[:number_words]
        return text

    @staticmethod
    def generate_random_text_by_type(text_tp: str, number_words: int = 5, is_combine: bool = False, is_contain_space: bool = False, is_upper_case: bool = False):
        if is_combine:
            return StringUtil.generate_random_number_string(number_words=number_words, is_contain_space=is_contain_space, is_upper_case=is_upper_case)
        if text_tp == 'str':
            return StringUtil.generate_random_string(number_words=number_words, is_contain_space=is_contain_space, is_upper_case=is_upper_case)
        elif text_tp == 'int':
            return StringUtil.generate_random_number(length=number_words)
        else:
            return StringUtil.generate_random_special_characters(number_words=number_words, is_contain_space=is_contain_space)

    @staticmethod
    def decode_str(data):
        """
        Convert encoded string to base64 string
        :return: string in byte format
        """
        decoded = base64.b64decode(data)
        return decoded.decode().encode()

    @staticmethod
    def base64_encode_text(data):
        """
        Convert string to base64 string
        :return: string in base64 format
        """
        return base64.b64encode(data.encode(encoding='utf-8'))

    @staticmethod
    def base64_decode_text(encoded_data):
        """
        Convert string to base64 string
        :return: string
        """
        return base64.b64decode(encoded_data).decode(encoding='utf-8')

    @staticmethod
    def format_string_with_re(re_format, value, repl: str = CommonTypeUsageConst.EMPTY):
        return re.sub(re_format, repl, value)

    @staticmethod
    def remove_all_except_text(value):
        return StringUtil.format_string_with_re(StringFormat.REMOVE_ALL_CHARACTERS_EXCEPT_TEXT, value)

    @staticmethod
    def convert_string_to_md5(text) -> str:
        """
            convert string to hash md5 hexstring
            :var text: input as string
            :return: md5 hashed string
        """
        result = hashlib.md5(text.encode())
        return result.hexdigest()

    @staticmethod
    def remove_space(value):
        """
        remove start space and end space
        :return: string
        """
        return re.sub(' +', ' ', value.lstrip(" ").rstrip(" "))

    @staticmethod
    def is_sorted(my_list: list, condition: str = 'asc') -> bool:
        if condition.lower() == 'asc':
            return all(my_list[i] <= my_list[i + 1] for i in range(len(my_list) - 1))
        elif condition.lower() == 'desc':
            return all(my_list[i] >= my_list[i+1] for i in range(len(my_list)-1))
        else:
            raise f'Do not support condition: {condition}. Valid value must be asc or desc!'

    @staticmethod
    def split_the_list(input_list: list = None, list_length: int = 50) -> dict:
        smaller_lists = {}

        for i in range(len(input_list) // list_length):
            smaller_lists[i] = input_list[i *
                                          list_length: (i + 1) * list_length]

        # Handling any remaining items
        if len(input_list) % list_length != 0:
            smaller_lists[len(input_list) // list_length] = input_list[(
                len(input_list) // list_length) * list_length:]

        return smaller_lists

    @staticmethod
    def convert_string_like_list_to_list(input_str: str) -> list:
        try:
            return ast.literal_eval(input_str)
        except Exception as e:
            raise f"Input str not in the string like list format {input_str}"
