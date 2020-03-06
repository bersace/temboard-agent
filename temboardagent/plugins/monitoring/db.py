# coding: utf-8

import json
import os
import sqlite3
from textwrap import dedent


def bootstrap(path, dbname):
    """Create SQLite database model we use to store collected data.

    last_measures table aims to keep a track of the last collected values
    (for some metrics, not all) we need to have to compute delta. This table
    must be purged when the agent starts because we do not want to compute
    delta values with potentially old data resulting with outliers.

    metrics table is used to queued collected data before they are pushed to
    temboard server.
    """

    with sqlite3.connect(os.path.join(path, dbname)) as conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS last_measures")
        c.execute(
            dedent("""
                CREATE TABLE last_measures (
                    time REAL,
                    key TEXT PRIMARY KEY,
                    data TEXT
                )
            """)
        )
        c.execute(
            dedent("""
                CREATE TABLE IF NOT EXISTS metrics (
                    time REAL PRIMARY KEY,
                    data TEXT
                )
            """)
        )


def add_metric(path, dbname, time, data):
    with sqlite3.connect(os.path.join(path, dbname)) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO metrics VALUES(?, ?)",
            (time, json.dumps(data))
        )


def delete_metric(path, dbname, time):
    with sqlite3.connect(os.path.join(path, dbname)) as conn:
        c = conn.cursor()
        c.execute(
            "DELETE FROM metrics WHERE time = ?",
            (time,)
        )


def get_metrics(path, dbname):
    with sqlite3.connect(os.path.join(path, dbname)) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT time, data FROM metrics ORDER BY time ASC LIMIT 50"
        )
        return c.fetchall()


def get_last_measure(path, dbname, key):
    with sqlite3.connect(os.path.join(path, dbname)) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT time, data FROM last_measures WHERE key = ?",
            (key,)
        )
        return c.fetchone()


def upsert_last_measure(path, dbname, time, key, data):
    with sqlite3.connect(os.path.join(path, dbname)) as conn:
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO last_measures VALUES(?, ?, ?)",
                (time, key, json.dumps(data))
            )
        except sqlite3.IntegrityError:
            c.execute(
                "UPDATE last_measures SET time = ?, data = ? "
                "WHERE key = ?",
                (time, json.dumps(data), key)
            )