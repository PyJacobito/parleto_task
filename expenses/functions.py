from re import search
from datetime import datetime
from typing import List


def get_date_str(str_var):
    try:
        return datetime.strptime(search(r'\d{4}-\d{2}-\d{2}', str_var).group(), '%Y-%m-%d').date()

    except AttributeError:
        return None


def get_date_list(str_var) -> List[str] or None:
    match_str = []

    while get_date_str(str_var):
        match_str.append(get_date_str(str_var))
        str_var = str_var.replace(str(get_date_str(str_var)), "")

    return match_str if match_str is not [] else None


def get_all_tokens(str_var):
    return [str_item.strip() for str_item in str_var.lower().split(",")]
