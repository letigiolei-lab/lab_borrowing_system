"""Database connection and parameterized query execution."""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            print(f"\n[!] Database Connection Error: {e}")
            return None

    @classmethod
    def execute_query(cls, query, params=(), commit=False):
        conn = cls.get_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
                return cursor.lastrowid or True
            return cursor.fetchall()
        except Error as err:
            print(f"\n[!] SQL Error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def execute_single(cls, query, params=()):
        results = cls.execute_query(query, params)
        if results and len(results) > 0:
            return results[0]
        return None
