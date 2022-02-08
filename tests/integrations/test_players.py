from datetime import datetime
from http import HTTPStatus

from apiritif import http

_BASE_URL = "http://localhost:8000/players"


class TestPlayers:
    def test_creation_should_be_ok(self):
        res = http.post(
            _BASE_URL,
            json={"nickname": "Test", "birthday": "26/08/94", "phone_number": "+33678958614"},
        )
        res.assert_ok()

    def test_creation_should_failed_on_duplicate(self):
        res = http.post(
            _BASE_URL,
            json={"nickname": "Test2", "birthday": "26/08/94", "phone_number": "+33678958644"},
        )
        res.assert_ok()
        res.assert_2xx()

        res = http.post(
            _BASE_URL,
            json={"nickname": "Test2", "birthday": "26/08/94", "phone_number": "+33678958674"},
        )
        res.assert_status_code(HTTPStatus.BAD_REQUEST)
        res.assert_regex_in_body("nickname.{4}duplicated")

        res = http.post(
            _BASE_URL,
            json={"nickname": "Test3", "birthday": "26/08/94", "phone_number": "+33678958674"},
        )
        res.assert_status_code(HTTPStatus.BAD_REQUEST)
        res.assert_regex_in_body("phone_number.{4}duplicated")
