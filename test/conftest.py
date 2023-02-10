from datetime import datetime, timezone

import pytest
from django.conf import settings
from django.core import serializers


def pytest_configure():
    settings.configure(
        SERIALIZATION_MODULES={
            "msgpack": "msgpack_serializer.serializer",
        },
        USE_TZ=True,
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
    )


@pytest.fixture
def some_date():
    yield datetime(2023, 1, 1, 8, 0, 0, tzinfo=timezone.utc)


@pytest.fixture()
def msgpack_serializer():
    yield serializers.get_serializer("msgpack")()
