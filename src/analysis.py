# This is the file where you will run the analysis code.
import psycopg2

def printResults(message, query, cursor):
    cursor.execute(query)
    record = cursor.fetchone()
    print(f"{message}: $ {record[0]} by {record[1]}")

try:
    conn = psycopg2.connect("host=postgres dbname=assessment user=postgres password=example port=5432")
    cur = conn.cursor()

    # Query to get the employee with the greatest TOTAL expenses
    highestExpense = """
        select MAX(a.totalCost), e.name
        from employees e, 
            (select SUM(exp.cost) as totalCost, exp.metadata->>'employeeId' as id
            from expenses exp
            group by(id)) as a 
        where e.employeeId = uuid(a.id)
        group by (e.name);
    """
    printResults('Overall highest expense', highestExpense, cur)

    # Query to get the employee with the greatest TOTAL expenses in Q1 2022
    highestExpenseQ1 = """
        select MAX(a.totalCost), e.name
        from employees e, 
            (select SUM(exp.cost) as totalCost, exp.metadata->>'employeeId' as id
            from expenses exp
            where TO_DATE(exp.metadata->>'date', 'YYYY/MM/DD') between '2022-01-01' and '2022-01-31'
            group by(id)) as a 
        where e.employeeId = uuid(a.id)
        group by (e.name);
    """
    printResults('Overall highest expense for Q1 2022', highestExpenseQ1, cur)

    # Query to get the employee with the greatest AVERAGE expenses
    highestAvgExpense = """
        select MAX(a.totalCost), e.name
        from employees e, 
            (select AVG(exp.cost) as totalCost, exp.metadata->>'employeeId' as id
            from expenses exp
            group by(id)) as a 
        where e.employeeId = uuid(a.id)
        group by (e.name);
    """
    printResults('Overall highest average expense', highestAvgExpense, cur)

    cur.close()
    conn.close()

except (Exception, psycopg2.Error) as err:
    print(f"Error while querying data: {err}")