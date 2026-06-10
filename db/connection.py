"""
db/connection.py
----------------
Manages the single shared PostgreSQL connection for the application.
All database access goes through the DBConnection singleton so that
connection details are never scattered across the codebase.
"""

import psycopg2
import psycopg2.extras

from config.settings import DatabaseConfig
from utils.logger import logger


class DBConnection:
    """
    Lightweight wrapper around a single psycopg2 connection.

    Usage
    -----
        conn = DBConnection()
        conn.execute("SELECT * FROM items WHERE item_id = %s", (1,))
        row = conn.fetchone()
        conn.commit()
    """

    def __init__(self):
        self._conn = None
        self._cur = None
        self._connect()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> None:
        """Open the database connection. Raises on failure."""
        try:
            self._conn = psycopg2.connect(
                host=DatabaseConfig.HOST,
                dbname=DatabaseConfig.NAME,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
            )
            self._cur = self._conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            )
            logger.info("Database connection established.")
        except psycopg2.OperationalError as exc:
            logger.error("Could not connect to the database: %s", exc)
            raise

    # ------------------------------------------------------------------
    # Public query interface
    # ------------------------------------------------------------------

    def execute(self, query: str, params=None) -> None:
        """Execute a parameterised query."""
        try:
            if params:
                self._cur.execute(query, params)
            else:
                self._cur.execute(query)
        except psycopg2.Error as exc:
            logger.error("Query execution failed: %s", exc)
            self._conn.rollback()
            raise

    def fetchone(self):
        """Return the next row from the last query result."""
        return self._cur.fetchone()

    def fetchall(self):
        """Return all rows from the last query result."""
        return self._cur.fetchall()

    def commit(self) -> None:
        """Commit the current transaction."""
        self._conn.commit()

    def close(self) -> None:
        """Close cursor and connection gracefully."""
        try:
            if self._cur:
                self._cur.close()
            if self._conn:
                self._conn.close()
            logger.info("Database connection closed.")
        except psycopg2.Error as exc:
            logger.warning("Error while closing the connection: %s", exc)

    # ------------------------------------------------------------------
    # Schema helper
    # ------------------------------------------------------------------

    @property
    def schema(self) -> str:
        return DatabaseConfig.SCHEMA
