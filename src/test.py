# This is the file where you will run the analysis code.
import psycopg2

def printResults(message, query, cursor):
    cursor.execute(query)
    records = cursor.fetchall()

    if records:
        print(f"{message}: \n")
        for record in records:
            print(f"{round(record[0], 2)} by {record[1]}")
    else:
        print(f"{message}: No results")

def print2(message, query, cursor):
    cursor.execute(query)
    records = cursor.fetchall()

    if records:
        print(f"{message}: \n")
        for record in records:
            print(f"{record}")
    else:
        print(f"{message}: No results")

try:
    conn = psycopg2.connect("host=postgres dbname=assessment user=postgres password=example port=5432")
    cur = conn.cursor()

    # Query to get the employee with the greatest TOTAL expenses
    highestExpense = """
        select totalCost, e.name
        from employees e, 
            (select SUM(exp.cost) as totalCost, exp.metadata->>'employeeId' as id
            from expenses exp
            group by(id)) as a 
        where e.employeeId = uuid(a.id)
        order by totalCost desc;
    """
    printResults('Overall highest expense', highestExpense, cur)

    # Query to get the employee with the greatest TOTAL expenses in Q1 2022
    highestExpenseQ1 = """
        select totalCost, e.name
        from employees e, 
            (select SUM(exp.cost) as totalCost, exp.metadata->>'employeeId' as id
            from expenses exp
            where TO_DATE(exp.metadata->>'date', 'YYYY/MM/DD') between '2022-01-01' and '2022-01-31'
            group by(id)) as a 
        where e.employeeId = uuid(a.id)
        order by totalCost desc;
    """
    printResults('Overall highest expense for Q1 2022', highestExpenseQ1, cur)

    # Query to get the employee with the greatest AVERAGE expenses (per month)
    highestAvgExpense = """
        select (a.totalCost/a.totalDays) as avgCost, e.name
        from employees e, 
            (select SUM(exp.cost) as totalCost, exp.metadata->>'employeeId' as id, count(*) as totalDays
            from expenses exp
            group by(exp.metadata)) as a 
        where e.employeeId = uuid(a.id)
        order by avgCost desc;
    """
    printResults('Overall highest monthly average expense', highestAvgExpense, cur)

    cur.close()
    conn.close()

except (Exception, psycopg2.Error) as err:
    print(f"Error while querying data: {err}")