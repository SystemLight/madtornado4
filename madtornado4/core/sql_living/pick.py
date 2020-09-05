from core.sql_living import member

from abc import ABC, abstractmethod
from typing import List

DirectiveField = List[member.Field]


class FilterBasic(ABC):

    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError()


class Where(FilterBasic):

    def __init__(self, condition: member.ConditionBasic):
        self.condition = condition
        self.pick = None

    def group_by(self, fields: DirectiveField) -> "GroupBy":
        self.pick = GroupBy(fields)
        return self.pick

    def order_by(self, fields: DirectiveField, sort: str) -> "OrderBy":
        self.pick = OrderBy(fields, sort)
        return self.pick

    def having(self, condition: member.ConditionBasic) -> "Having":
        self.pick = Having(condition)
        return self.pick

    def limit(self, count, start: int = 0) -> "Limit":
        self.pick = Limit(count, start)
        return self.pick

    def render(self) -> str:
        result = member.render_condition(self.condition)
        if self.pick is not None:
            result += self.pick.render()
        if result:
            result = " where " + result
        return result


class OrderBySort:
    DESC = "desc"
    ASC = "ASC"


class GroupBy(FilterBasic):

    def __init__(self, fields: DirectiveField):
        self.fields = fields
        self.pick = None

    def order_by(self, fields: DirectiveField, sort: str) -> "OrderBy":
        self.pick = OrderBy(fields, sort)
        return self.pick

    def having(self, condition: member.ConditionBasic) -> "Having":
        self.pick = Having(condition)
        return self.pick

    def limit(self, count, start: int = 0) -> "Limit":
        self.pick = Limit(count, start)
        return self.pick

    def render(self) -> str:
        result = map(lambda v: v.name, self.fields)
        result = ",".join(result)
        if self.pick is not None:
            result += self.pick.render()
        if result:
            result = " group by " + result
        return result


class OrderBy(FilterBasic):
    """

    排序指令，包含desc和asc两个可选参数值

    """

    def __init__(self, fields: DirectiveField, sort: str):
        self.fields = fields
        self.pick = None
        self.sort = sort

    def having(self, condition: member.ConditionBasic) -> "Having":
        self.pick = Having(condition)
        return self.pick

    def limit(self, count, start: int = 0) -> "Limit":
        self.pick = Limit(count, start)
        return self.pick

    def render(self) -> str:
        result = map(lambda v: v.name, self.fields)
        result = ",".join(result)
        if self.pick is not None:
            result += self.pick.render()
        if result:
            result = " order by " + result
        return result


class Having(FilterBasic):
    """

    聚合函数条件运算

    """

    def __init__(self, condition: member.ConditionBasic):
        self.condition = condition
        self.pick = None

    def limit(self, count, start: int = 0) -> "Limit":
        self.pick = Limit(count, start)
        return self.pick

    def render(self) -> str:
        result = member.render_condition(self.condition)
        if self.pick is not None:
            result += self.pick.render()
        if result:
            result = " having " + result
        return result


class Limit(FilterBasic):

    def __init__(self, count: int, start=0):
        self.count = count
        self.start = start

    def render(self) -> str:
        if self.start == 0:
            return " limit {}".format(self.count)
        return "limit {},{}".format(self.start, self.count)
