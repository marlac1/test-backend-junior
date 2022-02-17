from datetime import datetime
from http import HTTPStatus
from random import randint

from apiritif import http
from faker import Faker
from pytest import fixture
from tests.tools import SqliteAssertions


db = SqliteAssertions()
fake = Faker()

genders = ["male", "female", "others"]


@fixture
def test_player():
    player = {
        "nickname": fake.user_name(),
        "phone_number": fake.phone_number(),
        "gender": genders[randint(0, 1000) % 3],
    }

    id = db.ensure_exists(
        "players", {field: {"operator": "=", "value": value} for field, value in player.items()}
    )
    player["id"] = id

    yield player

    db.delete("players", id)


class TestDirectConversation:
    _BASE_URL = "http://localhost:8000/social/conversation"

    class TestCreate:
        def test_creation_should_be_ok(self):
            res = http.post(
                TestDirectConversation._BASE_URL,
                json={"nickname": "Test", "phone_number": "+33678958614"},
            )

            res.assert_ok()
            db.assert_exists(
                "players",
                {
                    "nickname": {"operator": "=", "value": "Test"},
                    "phone_number": {"operator": "=", "value": "+33678958614"},
                },
            )

        def test_creation_should_failed_on_duplicate(self):
            res = http.post(
                TestDirectConversation._BASE_URL,
                json={"nickname": "Test2", "phone_number": "+33668958444"},
            )
            res.assert_ok()

            res = http.post(
                TestDirectConversation._BASE_URL,
                json={"nickname": "Test2", "phone_number": "+33678958674"},
            )
            res.assert_status_code(400)
            res.assert_jsonpath("details[0].key", "players.nickname")
            res.assert_jsonpath("details[0].message", "duplicated")

            res = http.post(
                TestDirectConversation._BASE_URL,
                json={"nickname": "Test3", "phone_number": "+33668958444"},
            )
            res.assert_status_code(400)
            res.assert_jsonpath("details[0].key", "players.phone_number")
            res.assert_jsonpath("details[0].message", "duplicated")

            db.assert_exists(
                "players",
                {
                    "nickname": {"operator": "=", "value": "Test2"},
                    "phone_number": {"operator": "=", "value": "+33668958444"},
                },
            )

    class TestRead:
        def test_read_existing_should_return_its_data(self, test_player):
            # Setup
            res = http.get(TestDirectConversation._BASE_URL + f'/{test_player["nickname"]}')

            res.assert_ok()
            for path, value in test_player.items():
                if path == "id":
                    res.assert_not_jsonpath(path, value)
                else:
                    res.assert_jsonpath(path, value)

            res = http.get(TestDirectConversation._BASE_URL + f'/{test_player["id"]}')

            res.assert_ok()
            for path, value in test_player.items():
                if path == "id":
                    res.assert_not_jsonpath(path, value)
                else:
                    res.assert_jsonpath(path, value)

        def test_read_should_be_ok(self):
            # Setup
            res = http.get(TestDirectConversation._BASE_URL + "/nobodywillbeafraidofdeath")

            res.assert_status_code(404)

            res.assert_jsonpath("key", "player")
            res.assert_jsonpath("error", "not_found")
