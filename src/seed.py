# This file is where you will seed your Postgres database with the sample data from the data directory.
import psycopg2

EMPLOYEE_DATA_FILE = './data/employees.csv'
EXPENSE_DATA_FILE = './data/employees.csv'
EMPLOYEE_TABLE_NAME = 'employees'
EXPENSE_TABLE_NAME = 'expenses'

def copyFromFile(filePath, tableName, cursor):
    f = open(rf'{filePath}', 'r')
    # Skip header row
    next(f) 
    cursor.copy_from(file=f, table=tableName, sep="|")
    f.close()

try:
    conn = psycopg2.connect("host=postgres dbname=assessment user=postgres password=example port=5432")
    cur = conn.cursor()

    copyFromFile(EMPLOYEE_DATA_FILE, EMPLOYEE_TABLE_NAME, cur)
    copyFromFile(EXPENSE_DATA_FILE, EXPENSE_TABLE_NAME, cur)

    conn.commit()

    cur.close()
    conn.close()

except (Exception, psycopg2.Error) as err:
    print(f"Error while inserting entries {err}")
