# coding: utf-8

from enum import Enum

from ..exceptions import ValidateFieldError
from .base import FieldBase


class String(FieldBase):
    _type = str


class Integer(FieldBase):
    _type = int

    def __init__(self, max=None, min=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max = max
        self.min = min

    def validate(self, value):
        value = super().validate(value)

        if self.max is not None and value > self.max:
            raise ValidateFieldBaseError("'%s' is over '%s' field maximum '%s'" % (value, self.__class__.__name__, self.max))

        if self.min is not None and value < self.min:
            raise ValidateFieldBaseError("'%s' is over '%s' field mininum '%s'" % (value, self.__class__.__name__, self.max))

        return value


class List(FieldBase):
    _type = list

    def __init__(self, cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(cls, tuple) and all(isinstance(c, type) for c in cls):
            self._nested_types = cls
        elif isinstance(cls, type):
            self._nested_types = (cls)
        else:
            raise TypeError('%s field require class or tuple contain classes' % self.__class__.__name__)


class Set(List):
    _type = set


class Dict(FieldBase):
    def __init__(self, cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(cls, tuple) and all(isinstance(c, type) for c in cls):
            self._nested_types = cls
        elif isinstance(cls, type):
            self._nested_types = (cls)
        else:
            raise TypeError('%s field require class or tuple contain classes' % self.__class__.__name__)


class DateTime(FieldBase):
    pass


class Date(DateTime):
    pass


class Enum(FieldBase):
    def __init__(self, cls, *args, **kwargs):
        super(Enum, self).__init__(*args, **kwargs)

        if not isinstance(cls, Enum):
            raise TypeError('Enum field require Enum class')

        self._type = cls


class ValueObject(FieldBase):
    def __init__(self, cls, *args, **kwargs):
        super(ValueObject, self).__init__(*args, **kwargs)

        if not isinstance(cls, ValueObject):
            raise TypeError('ValueObject field require ValueObject class')

        self._type = cls


class Entity(FieldBase):
    def __init__(self, cls, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)

        if not isinstance(cls, Entity):
            raise TypeError('Entity field require Entity class')

        self._type = cls
