import pymysql
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
import pandas as pd
from contextlib import contextmanager


class WrapydbConnector:
    def __init__(self, connection_settings):
        self.connection_settings = connection_settings
        self.connection = None

    @contextmanager
    def _tunnel_context(self):
        tunnel = SSHTunnelForwarder(
            (self.connection_settings["ssh_host"], int(self.connection_settings["ssh_port"])),
            ssh_username=self.connection_settings["ssh_username"],
            ssh_private_key=self.connection_settings["ssh_private_key"],
            ssh_private_key_password=self.connection_settings["ssh_private_key_password"],
            remote_bind_address=(
                self.connection_settings["db_host"],
                int(self.connection_settings["db_port"]),
            ),
        )
        tunnel.start()
        try:
            yield tunnel
        finally:
            tunnel.close()

    @contextmanager
    def _db_connection(self, cursorclass=pymysql.cursors.Cursor):
        with self._tunnel_context() as tunnel:
            connection = pymysql.connect(
                host="127.0.0.1",
                user=self.connection_settings["db_user"],
                passwd=self.connection_settings["db_password"],
                db=self.connection_settings["db_name"],
                port=tunnel.local_bind_port,
                cursorclass=cursorclass,
            )
            try:
                yield connection
            finally:
                connection.close()

    def _get_database_url(self, tunnel):
        return f'mysql+pymysql://{self.connection_settings["db_user"]}:{self.connection_settings["db_password"]}@127.0.0.1:{tunnel.local_bind_port}/{self.connection_settings["db_name"]}'

    def execute_query(self, query, params=None, return_dict=False):
        cursorclass = pymysql.cursors.DictCursor if return_dict else pymysql.cursors.Cursor
        with self._db_connection(cursorclass=cursorclass) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                try:
                    result = cursor.fetchall()
                    return result
                except Exception as e:
                    return None

    def execute_update(self, query, params=None):
        with self._db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()

    def execute_batch_update(self, query, params_list, batch_size=100):
        """
        複数のSQL命令を一度に処理するバッチ更新関数
        query: 実行するSQLクエリ（プレースホルダー付き）
        params_list: 各SQLクエリのパラメータのリスト（例: [(param1, param2), (param1, param2), ...]）
        batch_size: 一度に実行するSQL命令の数
        """
        with self._db_connection() as connection:
            with connection.cursor() as cursor:
                for i in range(0, len(params_list), batch_size):
                    batch = params_list[i : i + batch_size]
                    cursor.executemany(query, batch)
                connection.commit()

    def df_to_sql(self, df, table_name, if_exists="append", index=False):
        with self._tunnel_context() as tunnel:
            database_url = self._get_database_url(tunnel)
            engine = create_engine(database_url)
            df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=index)

    def query_to_df(self, query):
        with self._tunnel_context() as tunnel:
            database_url = self._get_database_url(tunnel)
            engine = create_engine(database_url)
            return pd.read_sql_query(query, engine)

    @contextmanager
    def cursor(self):
        with self._db_connection() as connection:
            cursor = connection.cursor()
            try:
                yield cursor
            finally:
                cursor.close()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
