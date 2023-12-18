import psycopg2
import pymongo
import mysql.connector
import redis
from typing import List

from cores.utils.common.store_util import GetUtil
from cores.utils.common.string_util import StringUtil

from cores.decorators import parse_db_config
from cores.const.common import EnvironmentConst as const
from cores.model import DbConn
from cores.utils.logger_util import logger


class SQLQuery:

    @parse_db_config(const.Database.MYSQL)
    def __init__(self):
        __mysql: DbConn = GetUtil.suite_get(const.Database.MYSQL)
        self.conn = mysql.connector.connect(
            host=__mysql.db_host,
            user=__mysql.db_username,
            password=StringUtil.base64_decode_text(__mysql.db_pwd)
        )

    def execute_statement(self, statement: str = None):
        """
        Execute sql statement
        :param statement: sql query
        :return: result in json format
        """
        if statement:
            logger.debug(f'[SQL] Execute Statement:\n {statement}')
            cursor = self.conn.cursor()
            cursor.execute(statement)
            r = cursor.fetchall()
            # close cursor connection to db right after return data.
            cursor.close()
            logger.debug(f'[SQL] Result: \n{r}')
            return r
        else:
            raise ValueError('No Statement found!')

    def __del__(self):
        """
        Terminate connection to the DB
        """
        self.conn.close()


class RedisQuery:

    @parse_db_config(const.Database.REDIS)
    def __init__(self):
        __redis: DbConn = GetUtil.suite_get(const.Database.REDIS)
        self.conn = redis.Redis(host=__redis.db_host,
                                port=__redis.db_port,
                                username=__redis.db_username,
                                password=StringUtil.base64_decode_text(
                                    __redis.db_pwd),
                                decode_responses=True)

    def get(self, v: str) -> List:
        r = self.conn.get(v)
        logger.debug(f'[Redis] Result: \n{[r]}')
        return [r]

    def set(self, data: dict):
        logger.debug('[Redis] Insert data ')
        for k, v in data.items():
            self.conn.set(k, v)

    def flush_all(self):
        logger.debug('[Redis] Flush all data!')
        self.conn.flushdb()

    def __del__(self):
        self.conn.close()


class MongoDBQuery:

    @parse_db_config(const.Database.MONGODB)
    def __init__(self):
        __mongodb: DbConn = GetUtil.suite_get(const.Database.MONGODB)
        __myclient = pymongo.MongoClient(
            f"mongodb://{__mongodb.db_host}:{__mongodb.db_port}/")
        self.conn = __myclient[__mongodb.db_name]

    def insert(self, table: str, data: list):
        logger.debug(f'[MongoDB] Insert data to {table}:\n {data}')
        if len(data) == 1:
            self.conn[table].insert_one(data[0])
        else:
            self.conn[table].insert_many(data)

    def query(self, table: str, query: dict = None, limit: int = 10) -> list[dict]:
        logger.debug(f'[MongoDB] Execute Statement in {table}:\n{query}')
        if query:
            r = [x for x in self.conn[table].find(query).limit(limit)]
        else:  # return all results limit at limit
            r = [x for x in self.conn[table].find().limit(limit)]
        logger.debug(f'[MongoDB] Result:\n{r}')
        return r

    def truncate_data(self, table: str):
        logger.debug(f'[MongoDB] Truncate all data in {table}!')
        self.conn[table].delete_many({})


class PostgresQuery:

    @parse_db_config(const.Database.POSTGRES)
    def __init__(self):
        __postgres: DbConn = GetUtil.suite_get(const.Database.POSTGRES)
        self.conn = psycopg2.connect(database=__postgres.db_name,
                                     user=__postgres.db_username,
                                     host=__postgres.db_host,
                                     password=StringUtil.base64_decode_text(
                                         __postgres.db_pwd),
                                     port=__postgres.db_port)

    def query(self, command: str):
        logger.debug(f'[Postgres] Executed query:\n{command}')
        cur = self.conn.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        self.conn.commit()
        logger.debug(f'[Postgres] Result:\n{rows}')
        return rows

    def __del__(self):
        self.conn.close()
