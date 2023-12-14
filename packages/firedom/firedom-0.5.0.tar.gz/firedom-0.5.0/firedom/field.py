from datetime import datetime
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from google.cloud.firestore_v1 import FieldFilter
from typing import Any


class Field:
    def __init__(self, name: str, field_type: type, default_value: any = None) -> None:
        self.name = name
        self.field_type = field_type
        self.default_value = default_value

    def __eq__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '==', value)

    def __ne__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '!=', value)

    def __lt__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '<', value)

    def __le__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '<=', value)

    def __gt__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '>', value)

    def __ge__(self, value: Any) -> FieldFilter:
        return FieldFilter(self.name, '>=', value)

    def __hash__(self) -> None:
        pass

    def is_in(self, values: list[any]) -> FieldFilter:
        return FieldFilter(self.name, 'in', values)

    def is_not_in(self, values: list[any]) -> FieldFilter:
        return FieldFilter(self.name, 'not-in', values)

    def to_db_value(self, value: any) -> any:
        return value

    def to_python_value(self, value: any) -> any:
        return value


class DatetimeField(Field):
    def to_python_value(self, value: DatetimeWithNanoseconds) -> any:
        return datetime.fromtimestamp(value.timestamp())


class FieldFactory:
    FIELDS_MAPPING = {
        datetime: DatetimeField,
    }

    @classmethod
    def create_field(cls, **kwargs) -> Field:
        field_class = cls.FIELDS_MAPPING.get(kwargs.get('field_type'), Field)

        return field_class(**kwargs)
