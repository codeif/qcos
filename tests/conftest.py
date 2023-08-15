import os

import pytest


@pytest.fixture
def secret_id():
    return os.getenv("SECRET_ID")


@pytest.fixture
def secret_key():
    return os.getenv("SECRET_KEY")


@pytest.fixture
def region():
    return os.getenv("REGION")


@pytest.fixture
def bucket():
    return os.getenv("BUCKET")


@pytest.fixture
def client(secret_id, secret_key, region, bucket):
    from qcos import Client

    return Client(secret_id, secret_key, region, bucket)
