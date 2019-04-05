import pytest


@pytest.fixture(scope="session")
def custom_crate_a(crate_layer):
    yield from crate_layer("crate_a", "3.2.x")


@pytest.fixture(scope="session")
def custom_crate_b(crate_layer):
    yield from crate_layer("crate_b", "3.2.x")


def test_crate(crate):
    assert crate.dsn().startswith("http://127.0.0.1:42")


def test_cursor(crate_cursor):
    crate_cursor.execute("SELECT 1")
    assert crate_cursor.fetchone() == [1]


def test_execute(crate_execute, crate_cursor):
    for stmt in [
        "CREATE TABLE pytest (name STRING, version INT)",
        "INSERT INTO pytest (name, version) VALUES ('test_execute', 1)",
        "REFRESH TABLE pytest",
    ]:
        crate_execute(stmt)
    crate_cursor.execute("SELECT name, version FROM pytest")
    assert crate_cursor.fetchall() == [["test_execute", 1]]


def test_custom_crate(custom_crate_a, custom_crate_b):
    assert custom_crate_a.name == "crate_a"
    assert custom_crate_b.name == "crate_b"
