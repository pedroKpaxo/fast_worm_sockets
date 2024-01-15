from pytest import fixture

from starlette.testclient import TestClient

# TODO Find a better way to handle the fixtures


@fixture(scope="session")
def test_client(test_user):
    from app.main import app
    with TestClient(app) as test_client:
        yield test_client
