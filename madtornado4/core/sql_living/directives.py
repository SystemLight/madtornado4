from core.sql_living import pick, member

from abc import ABC, abstractmethod
from typing import Optional


class InvalidDirectivesError(Exception):
    pass


class DirectivesBasic(ABC):

    def __init__(self, table: str, fields: Optional[pick.DirectiveField] = None):
        self.fields = fields
        self.table = table
        self.pick = None
        self.template = None
        self.extra = {}

    def where(self, condition: member.ConditionBasic) -> "pick.Where":
        self.pick = pick.Where(condition)
        return self.pick

    def group_by(self, condition: member.ConditionBasic) -> "pick.GroupBy":
        raise InvalidDirectivesError()

    def order_by(self, condition, sort: str) -> "pick.OrderBy":
        raise InvalidDirectivesError()

    def having(self, condition: member.ConditionBasic) -> "pick.Having":
        raise InvalidDirectivesError()

    def limit(self, count: int, start: int = 0) -> "pick.Limit":
        raise InvalidDirectivesError()

    @abstractmethod
    def render_fields(self, field: "member.Field") -> str:
        raise NotImplementedError()

    def render(self) -> str:
        fields_str = ""
        if isinstance(self.fields, list):
            fields_list = []
            for f in self.fields:
                fields_list.append(self.render_fields(f))
            fields_str = ",".join(fields_list)

        if not fields_str:
            fields_str = "*"
        result = self.template.format(fields=fields_str, table=self.table, **self.extra)
        if self.pick is not None:
            result += self.pick.render()
        return result


def build_sql(model: object, sql: str) -> "SQL":
    return SQL()


class SQL:

    def __init__(self):
        self.directives = None  # type: Optional[DirectivesBasic]

    def select(self, table: str, fields: pick.DirectiveField = None) -> "Select":
        self.directives = Select(table, fields)
        return self.directives

    def insert(self, table: str, fields: pick.DirectiveField = None) -> "Insert":
        self.directives = Insert(table, fields)
        return self.directives

    def update(self, table: str, fields: pick.DirectiveField = None) -> "Update":
        self.directives = Update(table, fields)
        return self.directives

    def delete(self, table: str) -> "Delete":
        self.directives = Delete(table)
        return self.directives

    def sql(self) -> str:
        if self.directives is None:
            raise TypeError("空的指令")
        return self.directives.render()


class Select(DirectivesBasic):

    def __init__(self, table: str, fields: Optional[pick.DirectiveField] = None):
        super().__init__(table, fields)
        self.template = "select {fields} from {table}"

    def group_by(self, condition: member.ConditionBasic) -> "pick.GroupBy":
        self.pick = pick.GroupBy(condition)
        return self.pick

    def order_by(self, condition, sort: str) -> "pick.OrderBy":
        self.pick = pick.OrderBy(condition, sort)
        return self.pick

    def having(self, condition: member.ConditionBasic) -> "pick.Having":
        self.pick = pick.Having(condition)
        return self.pick

    def limit(self, count: int, start: int = 0) -> "pick.Limit":
        self.pick = pick.Limit(count, start)
        return self.pick

    def render_fields(self, field: "member.Field") -> str:
        return member.render_pure_field(field)


class Insert(DirectivesBasic):

    def __init__(self, table: str, fields: Optional[pick.DirectiveField] = None):
        super().__init__(table, fields)
        self.template = "insert into {table} {fields} values ({values})"

    def render_fields(self, field: "member.Field") -> str:
        return member.render_pure_field(field)

    def render(self) -> str:
        fields_str = ""
        values = []
        if isinstance(self.fields, list):
            fields_list = []
            for f in self.fields:
                if not f.value:
                    continue
                fields_list.append(f.name)
                values.append("'" + str(f.value) + "'")
            fields_str = ",".join(fields_list)

        fields_str = "(" + fields_str + ")" if fields_str else ""

        result = self.template.format(fields=fields_str, table=self.table, values=",".join(values))
        if self.pick is not None:
            result += self.pick.render()
        return result


class Update(DirectivesBasic):

    def __init__(self, table: str, fields: Optional[pick.DirectiveField] = None):
        super().__init__(table, fields)
        self.template = "update {table} set {fields}"

    def render_fields(self, field: "member.Field") -> str:
        return member.render_condition_field(field, True)


class Delete(DirectivesBasic):

    def __init__(self, table: str):
        self.table = table
        self.template = "delete from {table}"

    def render_fields(self, field: "member.Field") -> str:
        return member.render_pure_field(field)

    def render(self) -> str:
        result = self.template.format(table=self.table)
        if self.pick is not None:
            result += self.pick.render()
        return result
