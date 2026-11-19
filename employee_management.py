import tkinter as tk
from tkinter import ttk, messagebox 
import database 

database.create_table() 

root = tk.Tk()
root.title("Employee Management System")
root.geometry("1050x650")
root.configure(bg="#eef2f7")

# ---- Heading ---------- 
heading = tk.Label(
    root, 
    text="EMPLOYEE MANAGEMENT SYSTEM", 
    font=("Arial",22,"bold"), 
    bg="#1f3a5f", 
    fg="white", 
    pady=15
)
heading.pack(fill="x")

# Form 
form = tk.Frame(root, bg="#eef2f7",padx=20,pady=15)
form.pack(fill="x")

fields = ["Name","Email","Department","Salary"]
entries = {}

for i, field in enumerate(fields):
   tk.Label(
      form, 
      text=field, 
      font=("Arial",11,"bold"), 
      bg="#eef2f7"
   ).grid(row=i//2,column=(i % 2) * 2,padx=10,pady=10,sticky="W")

   entry = tk.Entry(form, font=("Arial",11),width=25)
   entry.grid(row=i//2,column=(i%2)*2 + 1,padx=10,pady=10)

   entries[field] = entry 

# ---- Search 
search_frame = tk.Frame(root,bg="#eef2f7")
search_frame.pack(pady=10)


tk.Label(
   search_frame, 
   text="Search Employee:", 
   bg="#eef2f7",
   font=("Arial",11,"bold")
).pack(side="left",padx=5)


# -- Tables 
table_frame = tk.Frame(root, padx=20,pady=10)
table_frame.pack(fill="both",expand=True)

columns = ("ID","Name","Email","Department","Salary")

tree = ttk.Treeview(
   table_frame, 
   columns=columns, 
   show="headings"
)

for col in columns:
   tree.heading(col,text=col)
   tree.column(col,width=180,anchor="center")
   tree.pack(fill="both",expand=True)   


def clear_fields():
   for entry in entries.values():
      entry.delete(0,tk.END)

def load_employees(rows=None):
   for item in tree.get_children():
      tree.delete(item) 

   if rows is None:
       rows  = database.get_employees()

   for row in rows:
      tree.insert("",tk.END,values=row)


def add_employee():
  name = entries["Name"].get().strip()
  email = entries["Email"].get().strip()
  department = entries["Department"].get().strip()
  salary_text = entries["Salary"].get().strip()

  if not all([name, email, department, salary_text]):
     messagebox.showwarning(
        "Vaildation","please fill all fields."
     )        
     return 
  
  try:
     salary = float(salary_text)
     if salary <= 0:
        raise ValueError
  except ValueError:
     messagebox.showerror(
        "Invaild Salary","Enter a vaild positive salary."
     )
     return
  
  try:
     database.add_employee(
        name,email,department,salary
     )
     messagebox.showinfo(
        "Success","Employee added successfully!"
     )
     clear_fields()
     load_employees() 

  except Exception as error:
     messagebox.showerror("Database Error",str(error))

def search_employee(event):
   selected = tree.selection()

   if not selected:
      return 

   values = tree.items(selected[0],"values")

   clear_fields()

   entries["Name"].insert(0, values[1])
   entries["Email"].insert(0,values[2])
   entries["Department"].insert(0,values[3])
   entries["Salary"].insert(0, values[4])


def update_employee():
   selected = tree.selection() 

   if not selected:
      messagebox.showwarning(
         "Selection","Select an employee first."
      )         
      return 

   emp_id = tree.item(selected[0],"values")[0]

   name = entries["Name"].get().strip()
   email = entries["email"].get().strip()
   department = entries["Department"].get().strip()
   salary_text = entries["salary"].get().strip()

   if not all([name,email,department,salary_text]):
      messagebox.showwarning(
         "Vaildation","please fill all fields."
      )  
      return 

   try:
      salary = float(salary_text)
      if salary <= 0:
         raise ValueError
   except ValueError:
      messagebox.showerror(
         "invaild Salary","Enter a vaild positive salary."
      )   
      return 

   try:
      result = database.update_employee(
         emp_id,name,email,department,salary
      )

      if result:
         messagebox.showinfo(
            "Success","Employee updated successfully!"
         )
      else:
         messagebox.showwarning(
            "Not Found","Employee records not found."
         ) 

         clear_fields()
         load_employees()

   except Exception as error:
      messagebox.showerror("Database Error str",(error))

def delete_employee():
   selected = tree.selection() 

   if not selected:
      messagebox.showwarning(
         "Selection","Select an employee first."
      )         
      return 

   emp_id = tree.items(selected[0],"values")[0]

   confirm = messagebox.askyesno(
      "Confirm Delete", 
      "Are you sure you want to delete this employees?"
   )

   if confirm:
      database.delete_employee(emp_id)
      messagebox.showinfo(
         "Success","Employee deleted successfully!"
      )
      clear_fields()
      load_employees()

def search_employee():
   keyword = search_entry.get().strip()

   if not keyword:
      load_employees()
      return 

   rows = database.search_employee(keyword)
   load_employees(rows)

def reset_search():
  search_entry.delete(0, tk.END)
  load_employees() 


# ----- Buttons -------- 
button_frame = tk.Frame(root, bg="#eef2f7",pady=15)
button_frame.pack()

tk.Button(
   button_frame, text="Add Employee", 
   command=add_employee, width=16, 
   bg="#198754",fg="white"
).grid(row=0, column=0, padx=8)


tk.Button(
   button_frame, text="Update Employees", 
   command=update_employee,width=16, 
   bg="#0d6efd",fg="white"
).grid(row=0,column=1,padx=8)

tk.Button(
   button_frame, text="Delete Employee", 
   command=delete_employee, width=16, 
   bg="#dc3545",fg="white"
).grid(row=0,column=2,padx=8)

tk.Button(
   button_frame, text="Search", 
   command=search_employee,width=16
).grid(row=0,column=3,padx=8)


tk.Button(
   button_frame, text="Reset", 
   command=reset_search, width=16
).grid(row=0,column=4,padx=8)

tree.bind("<<TreeviewSelect>>",search_employee)

load_employees()

root.mainloop()




     
     

