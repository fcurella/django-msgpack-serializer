from django.test import TestCase
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import timezone


class SimpleTest(TestCase):
    fixtures = ["test_data.json"]

    def test_serialization(self):
        user = User.objects.all()[0]
        user.last_joined = timezone.now()
        user.save()

        msgpack_serializer = serializers.get_serializer("msgpack")()
        data = msgpack_serializer.serialize([user])
        objs = [i for i in serializers.deserialize('msgpack', data)]
        self.assertEqual(objs[0].object, user)
