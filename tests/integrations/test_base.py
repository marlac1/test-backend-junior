from datetime import datetime

from apiritif import http

_BASE_URL = "http://localhost:8000"


class TestBase:
    def test_ok(self):
        res = http.get(_BASE_URL)
        res.assert_ok()
        res = http.get(_BASE_URL + "/ping")
        res.assert_ok()

    def test_utc(self):
        res = http.get(_BASE_URL + "/utc")
        res.assert_ok()
        res.assert_in_body(datetime.utcnow().strftime("%d/%m/%y - %H:%M"))
