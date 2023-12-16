from typing import Optional
from typing import List

from rick_db import fieldmapper
from rick_db.conn import Connection


@fieldmapper
class FieldRecord:
    field = "field"
    type = "type"
    primary = "primary"


@fieldmapper()
class UserRecord:
    name = "name"
    superuser = "superuser"
    createdb = "createdb"


class Metadata:
    def __init__(self, db: Connection):
        self._db = db

    def tables(self, schema=None) -> List:
        """
        List all available tables on the indicated schema. If no schema is specified, assume public schema
        :param schema: optional schema name
        :return: list of tablenames
        """
        raise NotImplementedError("abstract method")

    def views(self, schema=None) -> List:
        """
        List all available views on the indicated schema. If no schema is specified, assume public schema
        :param schema: optional schema name
        :return: list of tablenames
        """
        raise NotImplementedError("abstract method")

    def schemas(self) -> List:
        """
        List all available schemas
        :return: list of schema names
        """
        raise NotImplementedError("abstract method")

    def databases(self) -> List:
        """
        List all available databases
        :return: list of database names
        """
        raise NotImplementedError("abstract method")

    def table_indexes(self, table_name: str, schema=None) -> List[FieldRecord]:
        """
        List all indexes on a given table
        :param table_name:
        :param schema:
        :return:
        """
        raise NotImplementedError("abstract method")

    def table_pk(self, table_name: str, schema=None) -> Optional[FieldRecord]:
        """
        Get primary key from table
        :param table_name:
        :param schema:
        :return:
        """
        raise NotImplementedError("abstract method")

    def table_fields(self, table_name: str, schema=None) -> List[FieldRecord]:
        """
        Get fields of table
        :param table_name:
        :param schema:
        :return:
        """
        raise NotImplementedError("abstract method")

    def view_fields(self, view_name: str, schema=None) -> List[FieldRecord]:
        """
        Get fields of view
        :param view_name:
        :param schema:
        :return:
        """
        raise NotImplementedError("abstract method")

    def users(self) -> List[UserRecord]:
        """
        List all available users
        :return:
        """
        raise NotImplementedError("abstract method")

    def user_groups(self, user_name: str) -> List[str]:
        """
        List all groups associated with a given user
        :param user_name: username to check
        :return: list of group names
        """
        raise NotImplementedError("abstract method")

    def table_exists(self, table_name: str, schema=None) -> bool:
        """
        Check if a given table exists
        :param table_name: table name
        :param schema: optional schema
        :return:
        """
        raise NotImplementedError("abstract method")

    def view_exists(self, view_name: str, schema=None) -> bool:
        """
        Check if a given view exists
        :param view_name: table name
        :param schema: optional schema
        :return:
        """
        raise NotImplementedError("abstract method")

    def create_database(self, database_name: str, **kwargs):
        """
        Create a database
        :param database_name: database name
        :param kwargs: optional parameters
        :return:
        """
        raise NotImplementedError("abstract method")

    def database_exists(self, database_name: str) -> bool:
        """
        Checks if a given database exists
        :param database_name: database name
        :return: bool
        """
        raise NotImplementedError("abstract method")

    def drop_database(self, database_name: str):
        """
        Removes a database
        :param database_name: database name
        :return:
        """
        raise NotImplementedError("abstract method")

    def create_schema(self, schema: str, **kwargs):
        """
        Create a new schema in the current database
        :param schema:
        :return:
        """
        raise NotImplementedError("abstract method")

    def schema_exists(self, schema: str) -> bool:
        """
        Check if a given schema exists on the current database
        :param schema:
        :return: bool
        """
        raise NotImplementedError("abstract method")

    def drop_schema(self, schema: str, cascade: bool = False):
        """
        Removes a schema
        :param schema:
        :param cascade:
        :return:
        """
        raise NotImplementedError("abstract method")

    def kill_clients(self, database_name: str):
        """
        Kills all active connections to the database
        :param database_name:
        :return:
        """
        raise NotImplementedError("abstract method")

    def drop_table(self, table_name: str, cascade: bool = False, schema: str = None):
        """
        Removes a table
        :param table_name:
        :param cascade:
        :param schema:
        :return:
        """
        dialect = self._db.dialect()
        sql = "DROP TABLE IF EXISTS {name}".format(
            name=dialect.table(table_name, schema=schema)
        )
        if cascade:
            sql = sql + " CASCADE"
        with self._db.cursor() as c:
            c.exec(sql)

    def drop_view(self, view_name: str, cascade: bool = False, schema: str = None):
        """
        Removes a view
        :param view_name:
        :param cascade:
        :param schema:
        :return:
        """
        dialect = self._db.dialect()
        sql = "DROP VIEW IF EXISTS {name}".format(
            name=dialect.table(view_name, schema=schema)
        )
        if cascade:
            sql = sql + " CASCADE"
        with self._db.cursor() as c:
            c.exec(sql)
