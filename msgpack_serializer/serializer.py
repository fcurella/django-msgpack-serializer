"""
Serialize data to/from MsgPack
"""

import datetime
import decimal
from io import BytesIO

import msgpack
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.core.serializers.python import Serializer as PythonSerializer
from django.utils import datetime_safe


class Serializer(PythonSerializer):
    """
    Convert a queryset to msgpack.
    """

    internal_use_only = False
    stream_class = BytesIO

    def end_serialization(self):
        msgpack.pack(
            self.objects,
            self.stream,
            default=DjangoMsgPackEncoder().encode,
            **self.options
        )

    def getvalue(self):
        if callable(getattr(self.stream, "getvalue", None)):
            return self.stream.getvalue()


def Deserializer(stream_or_bytes):
    if isinstance(stream_or_bytes, bytes):
        stream = BytesIO(stream_or_bytes)
    else:
        stream = stream_or_bytes
    for obj in PythonDeserializer(
        msgpack.unpack(stream, object_hook=DjangoMsgPackDecoder().decode)
    ):
        yield obj


class DjangoMsgPack(object):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S.%f"


class DjangoMsgPackEncoder(DjangoMsgPack):
    """
    DjangoMsgPackEncoder class that knows how to encode date/time and decimal types.
    """

    def encode(self, o):
        if isinstance(o, datetime.datetime):
            return self.encode_datetime(o)
        elif isinstance(o, datetime.date):
            return self.encode_date(o)
        elif isinstance(o, datetime.time):
            return self.encode_time(o)
        elif isinstance(o, decimal.Decimal):
            return self.encode_decimal(o)
        else:
            return o

    def encode_datetime(self, obj):
        d = datetime_safe.new_datetime(obj)
        return {
            "__class__": "datetime",
            "as_str": d.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT)),
        }

    def encode_date(self, obj):
        d = datetime_safe.new_date(obj)
        return {"__class__": "date", "as_str": d.strftime(self.DATE_FORMAT)}

    def encode_time(self, obj):
        if isinstance(obj, datetime.datetime):
            return {"__class__": "time", "as_str": obj.strftime(self.TIME_FORMAT)}
        return obj

    def encode_decimal(self, obj):
        return {"__class__": "decimal", "as_str": str(obj)}


class DjangoMsgPackDecoder(DjangoMsgPack):
    """
    DjangoMsgPackEncoder class that knows how to encode date/time and decimal types.
    """

    def decode(self, obj):
        if "__class__" in obj:
            decode_func = getattr(self, "decode_%s" % obj["__class__"])
            return decode_func(obj)
        return obj

    def decode_datetime(self, obj):
        return datetime.datetime.strptime(
            obj["as_str"], "%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT)
        )

    def decode_date(self, obj):
        return datetime.datetime.strptime(obj["as_str"], self.DATE_FORMAT)

    def decode_time(self, obj):
        return datetime.datetime.strptime(obj["as_str"], self.TIME_FORMAT)

    def decode_decimal(self, obj):
        return decimal.Decimal(obj["as_str"])
