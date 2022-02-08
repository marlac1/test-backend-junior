import sqlite3
from typing import Dict, TypedDict
from uuid import uuid4

from tests import conf


class SqliteAssertions:
    class FieldsMatcher(TypedDict):
        operator: str
        value: str

    def __init__(self):
        conf.get("db", "name")
        self.__conn = sqlite3.connect(conf.get("db", "name"))

    def __del__(self):
        self.__conn.close()

    def assert_exists(
        self, table: str, fields: Dict[str, FieldsMatcher], clear_if_exists: bool = True
    ):
        curs = self.__conn.cursor()

        query = f"SELECT id FROM {table} WHERE "
        args = []

        is_first = True
        for field, expected_val in fields.items():
            op = expected_val.get("operator", "=")
            args.append(expected_val.get("value"))
            if is_first:
                query += f"{field} {op} ?"
                is_first = False
            else:
                query += f" AND {field} {op} ?"

        curs.execute(query, args)
        exists = curs.fetchone()

        if clear_if_exists and exists:
            query = f"DELETE FROM {table} WHERE id = ?"
            curs.execute(query, [exists[0]])
            self.__conn.commit()

        assert exists is not None

    def ensure_exists(
        self,
        table: str,
        fields: Dict[str, FieldsMatcher],
        id_field: str = "id",
    ) -> str:
        def __insert_arg(nb: int):
            res = ""
            for i in range(0, nb):
                res += "? ,"

            return res.removesuffix(" ,")

        curs = self.__conn.cursor()

        query = f"SELECT id FROM {table} WHERE "
        insert_query = f"INSERT INTO {table} "
        args = []
        values = []
        id = None
        is_first = True
        for field, expected_val in fields.items():
            if field == id_field:
                id = expected_val.get("value")

            op = expected_val.get("operator", "=")
            args.append(expected_val.get("value"))
            values.append(field)

            if is_first:
                query += f"{field} {op} ?"
                is_first = False
            else:
                query += f" AND {field} {op} ?"

        curs.execute(query, args)
        exists = curs.fetchone()

        if exists:
            return exists[0]

        if id is None:
            id = str(uuid4())
            args.append(id)
            values.append(id_field)

        insert_query += "(" + ", ".join(values) + ") VALUES (" + __insert_arg(len(args)) + ")"

        curs.execute(insert_query, args)
        self.__conn.commit()

        return id

    def delete(self, table: str, id: str, id_field: str = "id"):
        curs = self.__conn.cursor()
        query = f"DELETE FROM {table} WHERE {id_field} = ?"
        curs.execute(query, [id])
        self.__conn.commit()


# SELECT id FROM players WHERE nickname = '' AND phone_number = ''
