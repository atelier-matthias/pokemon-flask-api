from typing import (
    List,
    Any,
    Union,
    Dict,
    Optional,
)


MATCH_FROM_START = 1
MATCH_CONTAINS = 2
MATCH_FROM_END = 3


class MongoUtils:
    __slots__ = ()

    @staticmethod
    def match_in(value_list: List[Any]) -> Union[Any, Dict[str, List]]:
        if len(value_list) == 1:
            return value_list[0]
        else:
            return {'$in': value_list}

    @staticmethod
    def join_keys(*fields):
        return '.'.join(fields)

    @staticmethod
    def match_string_contains(matching: str, options: Optional[str] = 'i'):
        return MongoUtils.match_string(matching, options, match=MATCH_CONTAINS)

    @staticmethod
    def match_string(matching: str, options: Optional[str] = 'i', match: int = MATCH_FROM_START) -> Dict[str, str]:
        matching = str(matching).replace('$', '\\$').replace('.', '\\.').replace('^', '\\^')
        if match == MATCH_CONTAINS:
            str_query = f"{matching}"
        elif match == MATCH_FROM_START:
            str_query = f"^{matching}"
        elif match == MATCH_FROM_END:
            str_query = f"{matching}$"
        else:
            str_query = matching
        query = {'$regex': str_query}
        if options:
            query['$options'] = options
        return query
