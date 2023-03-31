import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # create database
    con = psycopg2.connect(
        dbname="postgres",
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
    )

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()
    con.autocommit = True

    # Use the psycopg2.sql module instead of string concatenation
    # in order to avoid sql injection attacks.
    cur.execute(
        sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(os.environ.get("POSTGRES_DB"))
        )
    )
