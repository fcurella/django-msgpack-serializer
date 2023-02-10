import pytest
from django.contrib.auth.models import User
from django.core import serializers


@pytest.mark.django_db(transaction=True)
def test_serialize(msgpack_serializer, some_date):
    user = User.objects.create(date_joined=some_date)
    result = msgpack_serializer.serialize([user])
    assert (
        result
        == b"\x91\x83\xa5model\xa9auth.user\xa2pk\x01\xa6fields\x8c\xa8password\xa0\xaalast_login\xc0\xacis_superuser\xc2\xa8username\xa0\xaafirst_name\xa0\xa9last_name\xa0\xa5email\xa0\xa8is_staff\xc2\xa9is_active\xc3\xabdate_joined\x82\xa9__class__\xa8datetime\xa6as_str\xba2023-01-01 08:00:00.000000\xa6groups\x90\xb0user_permissions\x90"  # noqa
    )

    users = [obj.object for obj in serializers.deserialize("msgpack", result)]
    assert users == [user]
