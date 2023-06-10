import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re

conn = sqlite3.connect("mydatabase.db")
conn.execute("CREATE TABLE mytable (id INTEGER PRIMARY KEY, phone TEXT, name TEXT, email TEXT, age INTEGER)")

# ქმნის ახალ rows
def add_row():
    # უისერისგან იღებს ინფუთს
    phone = phone_entry.get()
    name = name_entry.get()
    email = email_entry.get()
    age = age_entry.get()

    #Phone ვალიდაცია
    phone_pattern = ('^\+9955\d{8}$')
    if not re.match(phone_pattern, phone):
        messagebox.showerror("Hmmm","Enter a valid phone number")
        phone_entry.get() == False
        return

    if phone == '' or name == '' or email == '' or phone == '':
        messagebox.showerror('Hmmm', 'Please fill in all fields.')
        return
    
    #Name ვალიდაცია
    name_pattern = r'^[A-Z][a-z]+$'
    if not re.match(name_pattern, name):
        messagebox.showerror("Hmmm","Enter a valid name. (უნდა იწყებოდეს დიდი ასოთი, გრძელდებოდეს პატარა ასოებით)")
        name_entry.get() == False
        return
    
    #Email ვალიდაცია
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        messagebox.showerror("Hmmm","Enter a valid email")
        email_entry.get() == False
        return
    
    #Age ვალიდაცია
    if not age.isdigit():
        messagebox.showerror("Hmmm",'Enter a valid age')
        return
    
    
    # ახალ rows ამატებს მონაცემთა ბაზაში
    conn = sqlite3.connect("mydatabase.db")
    conn.execute("DROP TABLE IF EXISTS mytable")
    conn.execute("CREATE TABLE mytable (id INTEGER PRIMARY KEY, phone TEXT, name TEXT, email TEXT, age INTEGER)")
    conn.execute("INSERT INTO mytable (phone, name, email, age) VALUES (?, ?, ?, ?)", (phone, name, email, age))
    conn.commit()
    conn.close()

    # ახალ rows ამატებს ცხრილში
    row_id = table.insert("", "end", values=(phone, name, email, age))

    # ასუფთავებს ინფუთის ადგილებს
    phone_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    


window = tk.Tk()

table = ttk.Treeview(window, columns=("phone", "name", "email", "age"), show="headings")

# სვეტის ჰედერები
table.heading("phone", text="Phone Number")
table.heading("name", text="Name")
table.heading("email", text="Email")
table.heading("age", text="Age")

table.pack()

# ინფუთის ადგილები
phone_label = tk.Label(window, text="Phone Number:")
phone_label.pack()
phone_entry = tk.Entry(window)
phone_entry.pack()

name_label = tk.Label(window, text="Name:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

email_label = tk.Label(window, text="Email:")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

age_label = tk.Label(window, text="Age:")
age_label.pack()
age_entry = tk.Entry(window)
age_entry.pack()

search_label = tk.Label(window, text="Search:")
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(window)
search_entry.pack(side=tk.LEFT)


# ფუნქცია, რომელიც შლის მონიშნულ rows მონაცემთა ბაზიდან
def delete_row():
    # იღებს არჩეულ rows
    selected_row = table.selection()
    if selected_row:
        # იღებს არჩეული rows აიდის
        id = table.item(selected_row)['values'][0]
        # შლის მონაცემთა ბაზიდან
        conn = sqlite3.connect("mydatabase.db")
        conn.execute("DELETE FROM mytable WHERE id=?", (id,))
        conn.commit()
        conn.close()
        # Delete the row from the table
        table.delete(selected_row)

#---
def search():
    # იღებს საძებნ ინფუთს იუზერისგან
    search_text = search_entry.get()
    
    for row in table.get_children():
        table.delete(row)

    # იღებს მონაცემს მონაცემთა ბაზიდან და ამატებს ცხრილში
    conn = sqlite3.connect("mydatabase.db")
    data = conn.execute("SELECT * FROM mytable WHERE phone LIKE ? OR name LIKE ? OR email LIKE ? OR age LIKE ?", 
                         ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
    for row in data:
        table.insert("", "end", values=row)
    conn.close()

#search button
search_button = tk.Button(window, text="Search", command=search)
search_button.pack(side=tk.LEFT)

# add button
add_button = tk.Button(window, text="Add", command=add_row)
add_button.pack()


#delete button
delete_button = tk.Button(window, text="Delete", command=delete_row)
delete_button.pack()


# იღებს მონაცემს მონაცემთა ბაზიდან და ამატებს ცხრილში
conn = sqlite3.connect("mydatabase.db")
data = conn.execute("SELECT * FROM mytable")
for row in data:
    table.insert("", "end", values=row)
conn.close()

# დახურვის და ცხრილის გასუფთავება
def clear_table(conn):
    conn.close()
    for row in table.get_children():
        table.delete(row)
window.protocol("WM_DELETE_WINDOW", clear_table(conn))

window.mainloop()
