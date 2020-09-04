from abc import ABC, abstractmethod
from typing import Union, Optional, TypeVar, List


class RenderBasic(ABC):

    def render(self) -> str:
        raise NotImplementedError()


class ConditionBasic(RenderBasic):

    @abstractmethod
    def c_or(self, condition) -> "Condition":
        raise NotImplementedError()

    @abstractmethod
    def c_and(self, condition) -> "Condition":
        raise NotImplementedError()


class SQL(RenderBasic):

    def __init__(self):
        pass

    @staticmethod
    def from_sql(sql: str):
        return SQL()

    @staticmethod
    def from_model(model):
        return SQL()

    def select(self, fields=None, table=None):
        return Select(self)

    def sql(self) -> str:
        pass

    def render(self) -> str:
        pass


class Select(RenderBasic):

    def __init__(self, sql_parent: SQL):
        self.sql_parent = sql_parent

    def where(self) -> "Where":
        pass

    def group_by(self) -> "GroupBy":
        pass

    def order_by(self) -> "OrderBy":
        pass

    def having(self) -> "Having":
        pass

    def limit(self) -> "Limit":
        pass

    def render(self) -> str:
        pass


class Where(RenderBasic):

    def __init__(self, sql_parent: SQL):
        self.sql_parent = sql_parent

    def group_by(self) -> "GroupBy":
        pass

    def order_by(self) -> "OrderBy":
        pass

    def having(self) -> "Having":
        pass

    def limit(self) -> "Limit":
        pass

    def render(self) -> str:
        pass


class GroupBy(RenderBasic):

    def __init__(self, sql_parent: SQL):
        pass

    def order_by(self) -> "OrderBy":
        pass

    def having(self) -> "Having":
        pass

    def limit(self) -> "Limit":
        pass

    def render(self) -> str:
        pass


class OrderBy(RenderBasic):
    """

    排序指令，包含desc和asc两个可选参数值

    """

    def __init__(self, sql_parent: SQL):
        pass

    def having(self) -> "Having":
        pass

    def limit(self) -> "Limit":
        pass

    def render(self) -> str:
        pass


class Having(RenderBasic):
    """

    聚合函数条件运算

    """

    def __init__(self, sql_parent: SQL):
        pass

    def limit(self) -> "Limit":
        pass

    def render(self) -> str:
        pass


class Limit(RenderBasic):
    def __init__(self, sql_parent: SQL):
        pass

    def render(self) -> str:
        pass


class FieldNull:
    pass


class Field(RenderBasic):

    def __init__(self, name: str, value=FieldNull):
        self.value = value

    def sum(self) -> "Field":
        return self

    def count(self) -> "Field":
        return self

    def max(self) -> "Field":
        return self

    def min(self) -> "Field":
        return self

    def avg(self) -> "Field":
        return self

    def v(self, val=None) -> "Field":
        self.value = val
        return self

    def render(self) -> str:
        pass


class ConditionGroup(ConditionBasic):

    def __init__(self, condition: "Condition"):
        pass

    def c_or(self, condition) -> "Condition":
        pass

    def c_and(self, condition) -> "Condition":
        pass

    def render(self) -> str:
        pass


class Condition(ConditionBasic):

    def __init__(self, field: "Field"):
        self.field = field

    def c_or(self, condition) -> "Condition":
        pass

    def c_and(self, condition) -> "Condition":
        pass

    def render(self) -> str:
        pass
