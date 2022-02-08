import re

from app.domain.errors import Details, Optional

get_details_re = re.compile(r"(?P<kind>.*) constraint.*failed: (?P<key>.*)")

constraint_to_error = {"unique": "duplicated"}


def get_details(sql_error_info: str) -> Optional[Details]:
    result = get_details_re.search(sql_error_info.lower().replace("\n", "").replace("\r", ""))
    if not result:
        return None

    kind = result.group("kind")
    return Details(
        key=result.group("key"),
        message=constraint_to_error.get(kind, kind),
    )
