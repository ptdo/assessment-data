# This is the file where you will run the analysis code.
import psycopg2

def printResults(message, query, cursor):
    cursor.execute(query)
    record = cursor.fetchone()

    if record:
        print(f"{message}: $ {round(record[0], 2)} by {record[1]}")
    else:
        print(f"{message}: No results")

try:
    conn = psycopg2.connect("host=postgres dbname=assessment user=postgres password=example port=5432")
    cur = conn.cursor()

    print("Summary of transactions:\n")

    # Query to get the employee with the greatest TOTAL expenses
    highestExpense = """
        select totalCost, e.name, e.employeeId
        from employees e, 
            (select SUM(exp.cost) as totalCost, uuid(exp.metadata->>'employeeId') as id
            from expenses exp
            group by(id)) as a 
        where e.employeeId = a.id
        order by totalCost desc;
    """
    printResults('Overall highest expense', highestExpense, cur)

    # Query to get the employee with the greatest TOTAL expenses in Q1 2022
    highestExpenseQ1 = """
        select totalCost, e.name, e.employeeId
        from employees e, 
            (select SUM(exp.cost) as totalCost, uuid(exp.metadata->>'employeeId') as id
            from expenses exp
            where TO_DATE(exp.metadata->>'date', 'YYYY/MM/DD') between '2022-01-01' and '2022-01-31'
            group by(id)) as a 
        where e.employeeId = a.id
        order by totalCost desc;
    """
    printResults('Overall highest expense for Q1 2022', highestExpenseQ1, cur)

    # Query to get the employee with the greatest AVERAGE daily expenses
    highestAvgExpense = """
        select SUM(dailyCost)/SUM(totalDays) as avgCost, e.name
        from employees e,
            (select SUM(exp.cost) as dailyCost, exp.metadata, count(distinct exp.metadata->>'date') as totalDays
            from expenses exp
            group by(exp.metadata)) as a
        where e.employeeId = uuid(a.metadata->>'employeeId')
        group by (e.employeeId)
        order by avgCost desc;
    """
    printResults('Overall highest daily average expense', highestAvgExpense, cur)

    cur.close()
    conn.close()

except (Exception, psycopg2.Error) as err:
    print(f"Error while querying data: {err}")