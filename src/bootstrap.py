# This file is where you will boostrap your Postgres instance.
import psycopg

connect = psycopg.connect(host='localhost', dbname='assessment', \
    user='postgres', password='example', port=5432)

