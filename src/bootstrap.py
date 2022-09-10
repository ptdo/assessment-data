# This file is where you will boostrap your Postgres instance.
import psycopg2

try:
    conn = psycopg2.connect("dbname=assessment user=postgres password=example port=5432")
except Exception as err:
    print(err)