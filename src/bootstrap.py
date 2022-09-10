# This file is where you will boostrap your Postgres instance.
import psycopg2

try:
    conn = psycopg2.connect("host=postgres dbname=assessment user=postgres password=example port=5432")
    cur = conn.cursor()

    # Create Employees table 
    cur.execute("""
        create table if not exists employees (
            employeeId uuid primary key,
            name varchar
        ) 
    """)

    cur.execute("""
        create table if not exists expenses (
            transactionId uuid primary key,
            cost decimal,
            metadata jsonb
        )
    """)
    
    conn.commit()

    cur.close()
    conn.close()

except (Exception, psycopg2.Error) as err:
    print(f"Error while creating tables {err}")
