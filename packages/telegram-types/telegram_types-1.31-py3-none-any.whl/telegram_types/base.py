import inspect
import datetime
from base64 import b64encode
from enum import Enum

from pydantic import BaseModel, ConfigDict

from telegram_types.utils import datetime_to_timestamp


class Base(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    @classmethod
    def from_telegram_type_dict(cls, obj) -> dict:
        cls_dict = {}
        if 'owner_id' in cls.__fields__:
            cls_dict['owner_id'] = obj._client.me.id
        keys = obj.__dict__.keys() if hasattr(obj, '__dict__') else obj.__slots__
        for a in keys:
            v = getattr(obj, a, None)
            if a not in cls.__fields__:
                continue
            field_type = cls.__fields__[a].type_
            if type(v) == bytes:
                v = b64encode(v).decode()
            if type(v) == datetime.datetime:
                v = datetime_to_timestamp(v)
            if isinstance(v, Enum):
                v = v.value
            cls_dict[a] = ( field_type.from_telegram_type(v)
                            if inspect.isclass(field_type) and issubclass(field_type, Base)
                            else v )
        return cls_dict

    @classmethod
    def from_telegram_type(cls, obj):
        if obj is None:
            return None
        if isinstance(obj, list):
            return [cls.from_telegram_type(o) for o in obj]
        telegram_type_dict = cls.from_telegram_type_dict(obj)
        if telegram_type_dict is None:
            return None
        return cls(**telegram_type_dict)
