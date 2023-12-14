from . import settings
from .exceptions import TypeMismatchError, ParameterError


class ResultSet:

    def __init__(
            self,
            result=None,
            type_=settings.DEFAULT_RESULT_SET_TYPE,
            fields=None
    ):
        """
        ResultSet 结果集

        Args:
            result: 结果集
            type_: 结果集类型
            fields: 字段名, 当type_为dict时, 不可缺省
        """
        if result is None:
            result = []

        self._result = []
        self._index = 0
        self._type = type_

        if self._type == list:
            for row in result:
                if len(row) > 1:
                    self._result.append(list(row))
                elif len(row) == 1:
                    self._result.append(row[0])
                else:
                    self._result.append([None])
        elif self._type == dict:
            if fields is None:
                raise ParameterError("'type_' 为dict时 'fields' 需要传入参数")
            else:
                if isinstance(fields, list):
                    self._fields = fields
                elif isinstance(fields[0], list):
                    self._fields = fields[0]
                elif isinstance(fields[0], dict):
                    _ = []
                    for field in fields:
                        _.append(field.get('COLUMN_NAME'))
                    self._fields = _
                else:
                    raise ParameterError("'fields' 参数类型错误, 应为list[str]/list[dict]类型")
                for row in result:
                    self._result.append(_extract_as_dict(self._fields, row))
        else:
            raise TypeMismatchError("'type_' 只能是 list/dict 类型")

    def __iter__(self):
        return self

    def __next__(self):
        if not isinstance(self._result, list):
            return self._result
        if self._index < len(self._result):
            next_ = self._result[self._index]
            self._index += 1
            return next_
        else:
            raise StopIteration

    def __str__(self):
        return self._result.__str__()

    def __len__(self):
        return len(self._result)

    def all(self):
        """
        获取结果集, 并将结果集转换为一个方便迭代的结构(List)

        Returns:
            结果集
        """
        return self._result

    def get_key(self, key: str = None):
        """
        获取特定字段的值, 只能对单记录结果集使用

        Args:
            key: 字段

        Returns:
            记录
        """
        if self._type == dict and len(self._result) == 1:
            if len(self._result[0].values()) == 1:
                return list(self._result[0].values())[0]
            return self._result[0].get(key)

    def get(self, index: int = 0):
        """
        获取特定索引位置的记录

        Args:
            index: 索引

        Returns:
            结果集
        """
        if self._type == list:
            return self._result[index]
        if self._type == dict:
            if len(self._result) == 1:
                return self._result[0]
            return self._result[index]

    def limit(self, num: int = 1):
        """
        截取结果集的前n个结果

        Args:
            num: 数量

        Returns:
            结果集
        """
        if num > 0:
            return self._result[: num]
        else:
            raise ParameterError("'num' 参数的值必须大于 0 ！")

    def next(self):
        """
        获取结果集中的下一个结果

        Returns:
            记录
        """
        return self.__next__()


def _extract_as_dict(fields: list, value: list):
    """
    提取字段名和字段值组合后转换为dict结构

    Args:
        fields: 字段名
        value: 字段值

    Returns:
        dict结构的单行数据
    """
    fields_len = len(fields)
    value_len = len(value)

    if fields_len == value_len:
        return dict(zip(fields, value))

    row_data = {}
    for index_ in range(fields_len):
        if index_ >= value_len:
            row_data[fields[index_]] = None
        else:
            row_data[fields[index_]] = value[index_]
    return row_data
