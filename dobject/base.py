# coding: utf-8


class FieldBase(object):
    def __init__(self, required=False, default=None):
        self.required = required
        self.default = default

    def validate(self, value):
        if not isinstance(value, self._type):
            raise ValidateFieldError("'%s' is not matched field '%s'" % (value.__class__.__name__, self._type.__name__))

        return value


class ModelMeta(type):
    def __new__(meta, name, bases, dict_):
        fields = {k: v for k, v in dict_.items() if isinstance(v, Field)}

        for k in fields:
            del dict_[k]

        cls = super().__new__(meta, name, bases, dict_)
        cls._fields = fields

        return cls


class ModelBase(object, metaclass=ModelMeta):
    def __init__(self, **attrs):
        self._data = {}

        for k, v in attrs.items():
            setattr(self, k, v)

    def __getattr__(self, name):
        value = self._data.get(name)

        if not value:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

        return value

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        if name not in self._fields:
            raise TypeError("'%s' is not defined in '%s' object fields" % (name, self.__class__.__name__))

        validated = self._fields[name].validate(value)

        self._data[name] = validated

    def serialize(self):
        return self._data

    def __repr__(self):
        return '<%s `%s`>' % (self.__class__.__name__, str(self.serialize()))

    @classmethod
    def load(cls, data):
        return cls(**data)
