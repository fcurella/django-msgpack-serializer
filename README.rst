## msgpack_serializer

Provides a [msgpack](http://msgpack.org) serializer/deserializer for Django models instances.

### Installation

Add the module `msgpack_serializer.serializer` to your `SERIALIZATION_MODULES` setting:

::

    SERIALIZATION_MODULES = {
        "msgpack" : "msgpack_serializer.serializer",
    }

### Usage

To serialize:

::

    from django.core import serializers

    msgpack_serializer = serializers.get_serializer("msgpack")()
    data = msgpack_serializer.serialize(my_objects)


To deserialize:

::

    from django.core import serializers

    deserialized_objects = serializers.deserialize('msgpack', data)
    objs = [deserialized.object for deserialized in deserialized_objects]
