"""Sanity checks of the database contents."""
import os
import sqlite3

# Where is the database file?
WORKDIR = os.path.abspath(os.path.dirname(__file__))
DBFILE = os.path.join(WORKDIR, '..', 'k2-target-pixel-files.db')

# Setup a database connection
DB_CONNECTION = sqlite3.connect(DBFILE)
DB_CURSOR = DB_CONNECTION.cursor()


def query_one(sql):
    DB_CURSOR.execute(sql)
    return DB_CURSOR.fetchone()[0]


def test_unique_keplerids():
    """Ensure we don't include the same file twice."""
    total_count = query_one("SELECT COUNT(*) FROM tpf;")
    filename_count = query_one("SELECT COUNT(DISTINCT filename) FROM tpf;")
    assert total_count == filename_count
