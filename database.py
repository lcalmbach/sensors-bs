# from multiprocessing import connection
import streamlit as st
import psycopg2
import sqlalchemy as sql
import pandas as pd
from typing import Tuple

from db_config import dbcn

TEMP_TABLE = 'temp'
conn = psycopg2.connect(
    host=dbcn['DB_HOST'],
    database=dbcn["DATABASE"],
    user=dbcn["DB_USER"],
    password=dbcn["DB_PASS"])


def save_db_table(table_name: str, df: pd.DataFrame, fields: list, password: str, database: str) -> bool:
    ok, msg = False, ''
    engine = sql.create_engine(f'postgresql+psycopg2://postgres:{password}@localhost:5432/{database}')
    conn = engine.raw_connection()
    # conn.cursor().execute("SET search_path TO 'imp'")
    try:
        if len(fields) > 0:
            df = df[fields]

        df.to_sql(table_name, engine, if_exists='replace', chunksize=20000, index=False)
        ok = True
        msg = f'Table {table_name} was successfully saved'
        conn.commit
    except ValueError as vx:
        msg = f"ValueError saving station: {vx}"
    except Exception as ex:
        msg = f"Exception saving station: {ex}"
    finally:
        return ok, msg


def execute_non_query(cmd: str) -> Tuple[bool, str]:
    """Executes an insert or update statement on the database

    Args:
        cmd (str): command string
        conn (object): connection to the db

    Returns:
        _type_: _description_
    """
    ok = True
    err_msg = ''
    try:
        mycursor = db.conn.cursor()
        mycursor.execute(cmd)
        conn.commit()
    except Exception as ex:
        ok = False
        err_msg = ''  # ex.message
    print(cmd)
    return ok, err_msg


# @st.cache(suppress_st_warning=True)
def execute_query(query: str) -> Tuple[pd.DataFrame, bool, str]:
    """
    Executes a query and returns a dataframe with the results
    """
    ok = False
    err_msg = ''
    try:
        ok = True
        result = pd.read_sql_query(query, conn)
    except Exception as ex:
        # err_msg = ex.message
        result = pd.DataFrame()
    return result, ok, err_msg


def get_value(query) -> Tuple[str, bool, str]:
    df, ok, err_msg = execute_query(query)
    if len(df) > 0:
        result = df.iloc[0][df.columns[0]]
    else:
        ok = False
        result = None
    return result, ok, err_msg


def truncate_table(table_name) -> Tuple[bool, str]:
    """truncates a table from the public schema

    Args:
        table_name (_type_): table name

    Returns:
        _type_: _description_
    """
    sql = f"TRUNCATE TABLE public.{table_name} RESTART IDENTITY;"
    ok, err_msg = execute_non_query(sql)
    return ok, err_msg
