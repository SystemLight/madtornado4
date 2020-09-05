from abc import ABC, abstractmethod


def sql_filter(sql) -> str:
    dirty_stuff = ["\"", "\\", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@", "!"]
    sql = str(sql)
    for stuff in dirty_stuff:
        sql = sql.replace(stuff, "\\{}".format(stuff))
    return sql


class ConditionBasic(ABC):

    @abstractmethod
    def ior(self, condition: "ConditionBasic") -> "ConditionBasic":
        raise NotImplementedError()

    @abstractmethod
    def iand(self, condition: "ConditionBasic") -> "ConditionBasic":
        raise NotImplementedError()


def render_pure_field(field: "Field") -> str:
    """

    字段分隔渲染器

    :param field: Field
    :return: 渲染字符串

    """
    field_template = field.name
    f_size = 0
    for f in field.use_func:
        f_size += 1
        field_template = f + "(" + field_template
    field_template += ")" * f_size
    return field_template


def render_condition_field(field: "Field", set_mode: bool = False) -> str:
    """

    多重定义条件渲染器

    :param field: Field
    :param set_mode: 当前渲染添加是否为设置模式，即操作符恒定=号
    :return: 渲染字符串

    """
    if field.value is None:
        return ""
    field_template = render_pure_field(field)
    field_template += "{operator}'{value}'"
    operator = "=" if set_mode else field.operator
    return field_template.format(operator=operator, value=field.value)


def render_condition(condition: "ConditionBasic") -> str:
    if isinstance(condition, ConditionGroup):
        my_render = render_condition(condition.condition)
        if my_render:
            my_render = "(" + my_render + ")"
        if condition.brother is None:
            return my_render
        else:
            brother_render = render_condition(condition.brother)
            if my_render:
                brother_render += " " + condition.brother.link + " " + my_render
            return brother_render
    elif isinstance(condition, Condition):
        my_render = render_condition_field(condition.field)
        if condition.brother is None:
            return my_render
        else:
            brother_render = render_condition(condition.brother)
            if my_render:
                brother_render += " " + condition.brother.link + " " + my_render
            return brother_render
    else:
        raise TypeError("条件对象不正确")


class Field:

    def __init__(self, name: str):
        self.name = name
        self.__value = None
        self.__operator = None
        self.use_func = []

    @property
    def value(self):
        return self.__value

    @property
    def operator(self):
        return self.__operator

    def sum(self) -> "Field":
        self.use_func.append("sum")
        return self

    def count(self) -> "Field":
        self.use_func.append("count")
        return self

    def max(self) -> "Field":
        self.use_func.append("max")
        return self

    def min(self) -> "Field":
        self.use_func.append("min")
        return self

    def avg(self) -> "Field":
        self.use_func.append("avg")
        return self

    def lt(self, v):
        # field < value
        self.__operator = "<"
        self.__value = sql_filter(v)
        return self

    def le(self, v):
        # field <= value
        self.__operator = "<="
        self.__value = sql_filter(v)
        return self

    def eq(self, v):
        # field = value
        self.__operator = "="
        self.__value = sql_filter(v)
        return self

    def ne(self, v):
        # field <> value
        self.__operator = "<>"
        self.__value = sql_filter(v)
        return self

    def ge(self, v):
        # field >= value
        self.__operator = "<>"
        self.__value = sql_filter(v)
        return self

    def gt(self, v):
        # field > value
        self.__operator = ">"
        self.__value = sql_filter(v)
        return self

    def like(self, v):
        # field like value
        self.__operator = "like"
        self.__value = sql_filter(v)
        return self


class ConditionGroup(ConditionBasic):

    def __init__(self, condition: ConditionBasic, brother: ConditionBasic = None):
        self.condition = condition
        self.link = "or"
        self.brother = None

    def ior(self, condition: ConditionBasic) -> "ConditionBasic":
        self.link = "or"
        condition.brother = self
        return condition

    def iand(self, condition: ConditionBasic) -> "ConditionBasic":
        self.link = "and"
        condition.brother = self
        return condition


class Condition(ConditionBasic):

    def __init__(self, field: "Field", brother: ConditionBasic = None):
        self.field = field
        self.link = None
        self.brother = brother

    def ior(self, condition: ConditionBasic) -> "ConditionBasic":
        self.link = "or"
        condition.brother = self
        return condition

    def iand(self, condition: ConditionBasic) -> "ConditionBasic":
        self.link = "and"
        condition.brother = self
        return condition
