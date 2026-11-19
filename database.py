import sqlite3

DB_NAME = "employee.db"

def connect_db():
  return sqlite3.connect(DB_NAME)

def create_table():
  conn = connect_db()
  cursor = conn.cursor()

  cursor.execute("""
   CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    email TEXT NOT NULL, 
    department TEXT NOT NULL, 
    salary REAL NOT NULL
   
   )
""")

  conn.commit()
  conn.close() 

def add_employee(name,email,department,salary):
  conn = connect_db()
  cursor = conn.cursor()

  cursor.execute("""
   INSERT INTO employees 
   (name,email,department,salary)
   VALUES(?,?,?,?)
""",(name, email, department, salary))

  conn.commit()
  cursor = conn.cursor()


def get_employees():
  conn = connect_db()
  cursor = conn.cursor()

  cursor.execute("SELECT *FROM employees ORDER BY id")
  row = cursor.fetchall()

  conn.close()
  return rows 
  

def update_employee(emp_id, name, email, department, salary):
  conn = connect_db()
  cursor = conn.cursor()


  cursor.execute("""
    UPDATE employees 
    SET name=?,email=?,department=?,salary=?
    WHERE id=?
 """,(name,email,department,salary,emp_id))

  conn.commit()
  updated = cursor.rowcount
  conn.close()
  return updated

def delete_employee(emp_id):
  conn = connect_db()
  cursor = conn.cursor() 

  cursor.execute(
    "DELETE FROM employees WHERE id=?",(emp_id,)
  )

  conn.commit()
  deleted = cursor.rowcount
  conn.close()
  return deleted 


def search_employee(keyword):
  conn = connect_db()
  cursor = conn.cursor()

  cursor.execute("""
    SELECT *FROM employees 
    WHERE name LIKE ? 
    OR department LIKE ? 
    OR email LIKE ? 
  """,(f"%{keyword}%",f"%{keyword}%",f"%{keyword}%"))


  rows = cursor.fetchall()
  conn.close()
  return rows

if __name__ == "__main__":
  create_table()
  print("Employee database created successfully!")