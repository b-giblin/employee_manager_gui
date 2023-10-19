import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Database:
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def insert_employee(self, name, position):
        self.cursor.execute("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))
        self.conn.commit()

    def get_all_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def update_employee(self, id, name, position):
        self.cursor.execute("UPDATE employees SET name=?, position=? WHERE id=?", (name, position, id))
        self.conn.commit()

    def delete_employee(self, id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


class EmployeeManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Manager")
        self.geometry("400x400")
        self.db = Database()

        # UI elements
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("ID", "Name", "Position")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=30)
        self.tree.column("Name", anchor=tk.W, width=150)
        self.tree.column("Position", anchor=tk.W, width=100)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Position", text="Position", anchor=tk.W)

        self.tree.pack(pady=20)

        add_button = tk.Button(self, text="Add Employee", command=self.add_employee)
        add_button.pack()

        update_button = tk.Button(self, text="Update Employee", command=self.update_employee)
        update_button.pack()

        delete_button = tk.Button(self, text="Delete Employee", command=self.delete_employee)
        delete_button.pack()

        self.list_employees()

    def add_employee(self):
        name = simpledialog.askstring("Input", "Enter employee name:")
        position = simpledialog.askstring("Input", "Enter employee position:")
        if name and position:
            self.db.insert_employee(name, position)
            self.list_employees()

    def list_employees(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        employees = self.db.get_all_employees()
        for emp in employees:
            self.tree.insert(parent="", index=tk.END, iid=emp[0], text="", values=(emp[0], emp[1], emp[2]))

    def update_employee(self):
        selected = self.tree.selection()[0]
        emp_id, name, position = self.tree.item(selected, "values")

        new_name = simpledialog.askstring("Input", "Enter the new name:", initialvalue=name)
        new_position = simpledialog.askstring("Input", "Enter the new position:", initialvalue=position)

        if new_name and new_position:
            self.db.update_employee(emp_id, new_name, new_position)
            self.list_employees()

    def delete_employee(self):
        selected = self.tree.selection()[0]
        emp_id = self.tree.item(selected, "values")[0]
        self.db.delete_employee(emp_id)
        self.tree.delete(selected)

if __name__ == "__main__":
    manager = EmployeeManager()
    manager.mainloop()