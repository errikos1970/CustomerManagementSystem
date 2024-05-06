'''
e-Customer_Management_System Version: 0.0.5
Date: 06/05/2024
Author: Errikos Ntinos
Status: stable

changelog:
----------
* added sales functionality
* updated the treeview after sale
* add functionality to sale more than one product
* changed id in customers table to customerid

todo:
-----
fix treeview sizes
adjust frames
move search below CSV section to the final place
add send email functionality

'''
# import necessary libs
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
import webbrowser
import csv
import os
import re

mainwindow = tk.Tk()
mainwindow.title("Customer Management System 0.0.5")
mainwindow.geometry("1920x768")
mainwindow.state('zoomed')#Maximize the window using state property
#mainwindow.resizable(False,False) #locks the dimensions
mydata = []

# Create style Object for the hover effect in the buttons
style = Style()
style.configure('TButton', font =
               ('calibri', 9, 'bold'),
                    borderwidth = '4')
# Changes will be reflected by the movement of mouse.
style.map('TButton', foreground = [('active', '!disabled', 'green')],
                     background = [('active', 'blue')])

# the database functionality

# Connect to SQLite database
mydb = sqlite3.connect('crmdatabase005.db')
cursor = mydb.cursor()

# Create customers table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS customers
                  (customerid INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, email TEXT, phone TEXT, registration_date DATE)''')
mydb.close()# close connection,and restart it to make the new table

# reconnect to SQLite database,to create the other table
mydb = sqlite3.connect('crmdatabase005.db')
cursor = mydb.cursor()

# Create product table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS products
                  (product_id INTEGER PRIMARY KEY, product_name TEXT, stock INTEGER, product_price REAL, product_desc TEXT)''')
mydb.close()

mydb = sqlite3.connect('crmdatabase005.db')
cursor = mydb.cursor()

# Create sales table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS sales
                  (sale_id INTEGER PRIMARY KEY, customerid INTEGER, stock INTEGER, product_id INTEGER, sale_date DATE)''')


# Create a notebook (tabbed interface) to contain different searches
notebook = ttk.Notebook(mainwindow)

# Define variables to hold search queries
q_customers = StringVar()
q_products = StringVar()

# Define functions to open search tabs
def open_customer_search_window():
    create_search_tab("customers")  # Create the customers search tab if not already created
    notebook.select(notebook.tabs()[0])  # Select the first tab in the notebook

def open_product_search_window():
    create_search_tab("products")  # Create the products search tab if not already created
    notebook.select(notebook.tabs()[1])  # Select the second tab in the notebook   

# Function to create a search tab or update existing tab
def create_search_tab(search_type):
    # Check if a tab for the specified search type already exists
    for tab_id in notebook.tabs():
        tab_text = notebook.tab(tab_id, "text")
        if tab_text == f"Search {search_type.capitalize()}":
            # If the tab exists, update its contents with the new search query and results
            update_search_tab(tab_id, search_type)
            return

    # If the tab doesn't exist, create a new one
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=f"Search {search_type.capitalize()}")

    lbl = ttk.Label(tab, text=f"Enter {search_type} search query:")
    lbl.pack()

    entry = ttk.Entry(tab, textvariable=q_customers if search_type == "customers" else q_products)
    entry.pack()

    btn = ttk.Button(tab, text="Search", command=lambda: search(search_type, q_customers if search_type == "customers" else q_products, results_text))
    btn.pack()

    results_label = ttk.Label(tab, text="Search Results:")
    results_label.pack()

    results_text = Text(tab, height=10, width=100)
    results_text.pack()

# Function to update the contents of an existing search tab
def update_search_tab(tab_id, search_type):
    tab = notebook.nametowidget(tab_id)
    entry = tab.winfo_children()[1]  # Assuming entry widget is the second child of the tab
    entry.delete(0, END)  # Clear previous search query
    entry.insert(0, "")  # Reset entry widget
    results_text = tab.winfo_children()[4]  # Assuming results text widget is the fifth child of the tab
    results_text.delete(1.0, END)  # Clear previous search results

# Function to perform the search
def search(search_type, query_var, results_text):
    query = query_var.get()
    if not query:
        messagebox.showwarning("Empty Query", "Please enter a search query.")
        return

    if search_type == "customers":
        columns = ("customerid", "first_name", "last_name", "age", "email", "phone")
        table_name = "customers"
    elif search_type == "products":
        columns = ("product_id", "product_name", "stock", "product_price", "product_desc")
        table_name = "products"
    else:
        messagebox.showerror("Error", "Invalid search type.")
        return

    # Construct the SQL query dynamically
    sql_query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {' OR '.join([f'{col} LIKE ?' for col in columns])}"

    # Perform the search query
    cursor.execute(sql_query, tuple(['%' + query + '%'] * len(columns)))
    rows = cursor.fetchall()

    # Clear previous results
    results_text.delete(1.0, END)

    # Display search results
    if rows:
        for row in rows:
            # Format each row with better spacing
            for i, col in enumerate(columns):
                results_text.insert(END, f"{col.capitalize()}: {row[i]}\n")
            results_text.insert(END, "-" * 40 + "\n")  # Add a separator between entries
    else:
        results_text.insert(END, "No results found.")
   
# Pack and display the notebook
notebook.pack(expand=True, fill="both")

# Function to display the help file
def open_html_file():
    file_path = r".\help.html"  # Using a raw string to avoid escaping
    webbrowser.open_new_tab(file_path)

# Function to display the message box
def show_message_box():
    messagebox.showinfo("Information", "e-Customer Management System\n"
    "\n"
    "Version name: Igor\n"
    "\n"
    "Developed with love and Python""\n"
    "\n"
    "Epsilon Datum Web and I.T. Services""\n"
    "\n"
    "2024""\n"
    "\n"
    )

# Function to update the Treeview with data
def update_treeview(trv, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    trv.delete(*trv.get_children())
    for row in rows:
        trv.insert('', 'end', values=row)
        
def updateCustomersView(rows):
    global mydata
    mydata = rows
    trv_customers.delete(*trv_customers.get_children())  # Use trv_customers here
    for i in rows:
        trv_customers.insert('', 'end', values=i)

def updateProductsView(rows):
    global mydata
    mydata = rows
    trv_products.delete(*trv_products.get_children())  # Use trv_products here
    for i in rows:
        trv_products.insert('', 'end', values=i)

def clearCustomersView():
    # Query to fetch data from the customers table
    customer_query = "SELECT customerid, first_name, last_name, age, email, phone FROM customers"
    cursor.execute(customer_query)
    customer_rows = cursor.fetchall()
    rows = customer_rows
    # Update the GUI
    updateCustomersView(rows)

def clearProductsView():
    # Query to fetch data from the products table
    product_query = "SELECT product_id, product_name, stock, product_price, product_desc FROM products"
    cursor.execute(product_query)
    product_rows = cursor.fetchall()
    rows = product_rows
    # Update the GUI
    updateProductsView(rows)
    
def get_customers_row(event):
    #item = trv.item(trv.focus())
    item = trv_customers.item(trv_customers.focus())  # Use trv_customers here
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])
    t5.set(item['values'][4])# for email
    t6.set(item['values'][5])# for phone
    
def get_products_row(event):    
    item = trv_products.item(trv_products.focus())  # Use trv_products here
    t7.set(item['values'][0])# for product_id
    t8.set(item['values'][1])# for product_name
    t9.set(item['values'][2])# for stock
    t10.set(item['values'][3])# for product_price
    t11.set(item['values'][4])# for product_desc
    #t12.set(item['values'][5])#product_stock    
    
def add_new_customer():
    fname = t2.get().upper()
    lname = t3.get().upper()
    age = t4.get()
    email = t5.get().upper()
    phone = t6.get() 
    # Check if any required field is empty
    if not fname or not lname or not age or not email or not phone:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return
    # Check if email is valid
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return
    # All required fields are filled and email is valid, proceed with adding the customer
    query = "INSERT INTO customers(customerid, first_name, last_name, age, email, phone, registration_date) VALUES(NULL, ?, ?, ?, ?, ?, DATE('now'))"
    cursor.execute(query, (fname, lname, age, email, phone))
    mydb.commit()
    clearCustomersView()

def delete_customer():
    customerid = t1.get()
    if messagebox.askyesno("DELETE CUSTOMER", "DELETE CUSTOMER ?"):
        query = "DELETE FROM customers WHERE customerid = ?"
        cursor.execute(query, (customerid,))
        mydb.commit()
        clearCustomersView()
    else:
        return True

def update_customer():
    fname = t2.get().upper()
    lname = t3.get().upper()
    age = t4.get()
    custid = t1.get()
    email = t5.get().upper()
    phone = t6.get()
    
    if messagebox.askyesno("UPDATE CUSTOMER", "UPDATE CUSTOMER ?"):
        query = "UPDATE customers SET first_name = ?, last_name = ?, age = ? , email = ? , phone = ? WHERE customerid = ?" 
        cursor.execute(query, (fname, lname, age, email, phone, custid))
        mydb.commit()
        clearCustomersView()
    else:
        return True          
# valid email check
def is_valid_email(email):
    # Regular expression for email validation
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(regex, email):
        return True
    else:
        return False
        
def add_new_product():
    product_id = t7.get()
    product_name = t8.get().upper()
    stock = t9.get()
    product_price = t10.get()
    product_desc = t11.get().upper()
    #product_stock = t12.get()
    # Check if any required field is empty
    if not product_id or not product_name or not stock or not product_price or not product_desc:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return  
    # All required fields are filled, proceed with adding the product 
    query = "INSERT INTO products(product_id, product_name, stock, product_price, product_desc) VALUES(?, ?, ?, ?, ?)" 
    cursor.execute(query, (product_id, product_name, stock, product_price, product_desc))
    mydb.commit()
    clearProductsView()

def delete_product():
    product_id = t7.get()
    if messagebox.askyesno("DELETE PRODUCT", "DELETE PRODUCT ?"):
        query = "DELETE FROM products WHERE product_id = ?"
        cursor.execute(query, (product_id,))
        mydb.commit()
        clearProductsView()
    else:
        return True    

def update_product():
    product_id = t7.get()
    product_name = t8.get().upper()
    stock = t9.get()
    product_price = t10.get()
    product_desc = t11.get().upper()
    #product_stock = t12.get()
    
    if messagebox.askyesno("UPDATE PRODUCT", "UPDATE PRODUCT ?"):
        query = "UPDATE products SET product_name = ?, stock = ?, product_price = ? , product_desc = ? WHERE product_id = ?"
        cursor.execute(query, (product_name, stock, product_price, product_desc, product_id))
        mydb.commit()
        clearProductsView()
    else:
        return True


# Function to handle the sale operation
def sell_product():
    customerid = ent_sale_customer_id.get()
    product_id = ent_sale_product_id.get()
    quantity = ent_sale_quantity.get()  # Get the quantity from the entry field

    # Check if customer ID, product ID, and quantity are provided
    if not customerid or not product_id or not quantity:
        messagebox.showerror("Error", "Please provide customer ID, product ID, and quantity.")
        return

    # Fetch product details from the database
    cursor.execute("SELECT stock FROM products WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    if not row:
        messagebox.showerror("Error", "Product not found.")
        return

    current_stock = row[0]
    if current_stock < int(quantity):
        messagebox.showerror("Error", "Not enough stock available.")
        return

    # Update the stock in the database
    new_stock = current_stock - int(quantity)
    cursor.execute("UPDATE products SET stock = ? WHERE product_id = ?", (new_stock, product_id))

    # Record the sale in the database for each quantity sold
    for _ in range(int(quantity)):
        cursor.execute("INSERT INTO sales (customerid, product_id, sale_date) VALUES (?, ?, DATE('now'))", (customerid, product_id))

    mydb.commit()  # Commit the transaction

    messagebox.showinfo("Success", "Product sold successfully. Stock updated.")

    # Clear the entry fields
    ent_sale_customer_id.delete(0, tk.END)
    ent_sale_product_id.delete(0, tk.END)
    ent_sale_quantity.delete(0, tk.END)
    
    # Refresh the Treeview after the sale for both customers and products
    clearCustomersView()
    clearProductsView()    


def confirm_quit():
    if messagebox.askokcancel("Exit Customer Management System", "Are you sure you want to quit?"):
        mainwindow.destroy()

# 344

# top main menu
menu = tk.Menu(mainwindow)
mainwindow.configure(menu=menu)
# help
help_menu = tk.Menu(menu, tearoff=False)
help_menu.add_command(label='Help file', command=open_html_file)
menu.add_cascade(label='Help', menu=help_menu)
# about
about_menu = tk.Menu(menu, tearoff=False)
about_menu.add_command(label='About', command=show_message_box)
menu.add_cascade(label='About', command=show_message_box)

# Add the Search menu on top
search_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Search", menu=search_menu)

# Add menu items for searching customers and products
search_menu.add_command(label="Search Customers", command=open_customer_search_window)
search_menu.add_command(label="Search Products", command=open_product_search_window)

# exit - Add the exit_menu to the main menu, not directly to the window
exit_menu = tk.Menu(menu, tearoff=False)
exit_menu.add_command(label='Exit', command=confirm_quit)
menu.add_cascade(label='Exit', menu=exit_menu)

# the variables we'll use
q1 = tk.StringVar()
q2 = tk.StringVar()
t1 = tk.StringVar()
t2 = tk.StringVar()
t3 = tk.StringVar()
t4 = tk.StringVar()
t5 = tk.StringVar()# email
t6 = tk.StringVar()# phone

t7 = tk.StringVar() # product_id
t8 = tk.StringVar()# product_name
t9 = tk.StringVar()# stock
t10 = tk.StringVar()# product_price
t11 = tk.StringVar()# product_desc
#t12 = tk.StringVar()# product_stock

# Create the customers Treeview
wrapper1 = ttk.LabelFrame(mainwindow, text="Customer List")
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
trv_customers = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6), show="headings", height="5")
trv_customers.pack(side=tk.LEFT)
trv_customers.place(x=0, y=0)

for col in (1, 2, 3, 4, 5, 6):
    trv_customers.heading(col, text=f"Column {col}")
    trv_customers.column(col, width=150, minwidth=100) # original: (col, width=150, minwidth=100)
update_treeview(trv_customers, "SELECT customerid, first_name, last_name, age, email, phone FROM customers")
# end of customers treeview

# Create the products Treeview 
wrapper2 = ttk.LabelFrame(mainwindow, text="Product List")
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
trv_products = ttk.Treeview(wrapper2, columns=(1, 2, 3, 4, 5, 6), show="headings", height="5")
trv_products.pack(side=tk.LEFT)
trv_products.place(x=0, y=0)

for col in (1, 2, 3, 4, 5):
    trv_products.heading(col, text=f"Column {col}")
    trv_products.column(col, width=150, minwidth=100)
update_treeview(trv_products, "SELECT product_id, product_name, stock, product_price, product_desc FROM products")
# end of products treeview


#wrapper1 = ttk.LabelFrame(mainwindow, text="Customer Data test")
wrapper4 = ttk.LabelFrame(mainwindow, text="CSV Functions")
wrapper3 = ttk.LabelFrame(mainwindow, text="Products Data")
# wrapper6 = ttk.LabelFrame(mainwindow, text="Copyright: Epsilon Datum - Errikos Ntinos , 2024") #commented on 06.7.3

#wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper4.pack(fill="both", expand="yes", padx=20, pady=10)
#wrapper5.pack(fill="both", expand="yes", padx=20, pady=10)
#wrapper6.pack(fill="both", expand="yes", padx=20, pady=10)#commented on 06.7.3A

trv_customers.pack(side=LEFT)# for the scrollbar
trv_customers.place(x=0, y=0) #added to show the scrollbar
#trv.heading('#0', text="ZABARAKATRANEMIA")#added on 4.03 - do i need it? COMMENTED TO TEST
trv_customers.heading(1, text="Customer ID")
trv_customers.heading(2, text="First Name")
trv_customers.heading(3, text="Last Name")
trv_customers.heading(4, text="Age")
trv_customers.heading(5, text="Email")
trv_customers.heading(6, text="Phone")

trv_products.heading(1, text="Product ID") 
trv_products.heading(2, text="Product Name") 
trv_products.heading(3, text="Product Stock") 
trv_products.heading(4, text="Product Price") 
trv_products.heading(5, text="Product Description")
#trv_products.heading(6, text="Product Stock")

# SETTINGS FOR FIELDS WIDTH
#trv.column('#0', width=75, minwidth=75)# original value width=50, minwidth=100)
trv_customers.column('#1', width=250, minwidth=200)#original value width=250, minwidth=200) changed to 150 and 100
trv_customers.column('#2', width=250, minwidth=200)#original value width=250, minwidth=200) changed to 150 and 100
trv_customers.column('#3', width=250, minwidth=200)#original value width=250, minwidth=200)
trv_customers.column('#4', width=250, minwidth=200)#original value width=250, minwidth=200) change to width=60, minwidth=45
trv_customers.column('#5', width=250, minwidth=200)# change to width=250, minwidth=100
trv_customers.column('#6', width=250, minwidth=200)# change to width=150, minwidth=100)

trv_products.column('#1', width=250, minwidth=200)# original width=75, minwidth=75) 
trv_products.column('#2', width=250, minwidth=200)#original width=200, minwidth=100
trv_products.column('#3', width=250, minwidth=200)#original width=200, minwidth=90
trv_products.column('#4', width=250, minwidth=200)#original width=200, minwidth=100
trv_products.column('#5', width=250, minwidth=200)#original width=200, minwidth=100
#trv_products.column('#6', width=250, minwidth=200)#original width=200, minwidth=100

# add double click on customers and products,use to update their fields
trv_customers.bind('<Double 1>', get_customers_row)
trv_products.bind('<Double 1>', get_products_row)

# edo 462#

# customers scrollbar 
yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=trv_customers.yview)
yscrollbar.pack(side=RIGHT, fill="y")
trv_customers.configure(yscrollcommand=yscrollbar.set)
# products scrollbar
yscrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=trv_products.yview)
yscrollbar.pack(side=RIGHT, fill="y")
trv_products.configure(yscrollcommand=yscrollbar.set)
# end of scrollbars

# Create a frame for the CUSTOMER labels, entries, and buttons
frame_customers = ttk.Frame(mainwindow)
frame_customers.pack(side=tk.RIGHT, padx=20, pady=10, anchor=tk.NE)  # Align to upper right corner

# Create a label for "Customer Data" and place it above the frame
#lbl_customer_data = ttk.Label(mainwindow, text="Customer Data")
#lbl_customer_data.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.NE)  # Align to top right

# OUR customer LABELS
lbl1 = ttk.Label(frame_customers, text="Customer ID:")
lbl1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

lbl2 = ttk.Label(frame_customers, text="First Name:")
lbl2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

lbl3 = ttk.Label(frame_customers, text="Last Name:")
lbl3.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

lbl4 = ttk.Label(frame_customers, text="Age:")
lbl4.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

lbl5 = ttk.Label(frame_customers, text="Email:")
lbl5.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

lbl6 = ttk.Label(frame_customers, text="Phone:")
lbl6.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

# Adjust grid positions for customer entries
ent1 = ttk.Entry(frame_customers, textvariable=t1)
ent1.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

ent2 = ttk.Entry(frame_customers, textvariable=t2)
ent2.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

ent3 = ttk.Entry(frame_customers, textvariable=t3)
ent3.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

ent4 = ttk.Entry(frame_customers, textvariable=t4)
ent4.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

ent5 = ttk.Entry(frame_customers, textvariable=t5)
ent5.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

ent6 = ttk.Entry(frame_customers, textvariable=t6)
ent6.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

# Adjust grid positions for customer buttons
add_btn = ttk.Button(frame_customers, text="Add New Customer", command=add_new_customer)
add_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

update_btn = ttk.Button(frame_customers, text="Update Customer", command=update_customer)
update_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

delete_btn = ttk.Button(frame_customers, text="Delete Customer", command=delete_customer)
delete_btn.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Create a frame for the PRODUCT labels, entries, and buttons
frame_products = ttk.Frame(mainwindow)
frame_products.pack(side=tk.LEFT, padx=20, pady=10, anchor=tk.NW)  # Align to upper LEFT corner 

# Create a label for "PRODUCT Data" and place it above the frame
#lbl_product_data = ttk.Label(mainwindow, text="Product Data")
#lbl_product_data.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.NW)  # Align to top LEFT

# products labels 
lbl7 = ttk.Label(frame_products, text="Product ID")
lbl7.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

lbl8 = ttk.Label(frame_products, text="Product Name")
lbl8.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

lbl9 = ttk.Label(frame_products, text="Product Stock")
lbl9.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

lbl10 = ttk.Label(frame_products, text="Product Price")
lbl10.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

lbl11 = ttk.Label(frame_products, text="Product Description")
lbl11.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

#lbl12 = ttk.Label(frame_products, text="Product Stock")
#lbl12.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

# Adjust grid positions for products entries
ent7 = ttk.Entry(frame_products, textvariable=t7)
ent7.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

ent8 = ttk.Entry(frame_products, textvariable=t8)
ent8.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

ent9 = ttk.Entry(frame_products, textvariable=t9)
ent9.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

ent10 = ttk.Entry(frame_products, textvariable=t10)
ent10.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

ent11 = ttk.Entry(frame_products, textvariable=t11)
ent11.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

#ent12 = ttk.Entry(frame_products, textvariable=t12)
#ent12.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

# Adjust grid positions for products buttons
add_product_btn = ttk.Button(frame_products, text="Add New Product", command=add_new_product)
add_product_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

update_product_btn = ttk.Button(frame_products, text="Update Product", command=update_product)
update_product_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

delete_product_btn = ttk.Button(frame_products, text="Delete Product", command=delete_product)
delete_product_btn.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)


# Add labels, entries, and buttons for the sale operation
lbl_sale_customer_id = ttk.Label(mainwindow, text="Customer ID for Sale:")
lbl_sale_customer_id.pack(side=tk.LEFT, padx=10, pady=5)

ent_sale_customer_id = ttk.Entry(mainwindow)
ent_sale_customer_id.pack(side=tk.LEFT, padx=10, pady=5)

lbl_sale_product_id = ttk.Label(mainwindow, text="Product ID for Sale:")
lbl_sale_product_id.pack(side=tk.LEFT, padx=10, pady=5)

ent_sale_product_id = ttk.Entry(mainwindow)
ent_sale_product_id.pack(side=tk.LEFT, padx=10, pady=5)



# Add entry field for quantity
lbl_sale_quantity = ttk.Label(mainwindow, text="Quantity:")
lbl_sale_quantity.pack(side=tk.LEFT, padx=10, pady=5)

ent_sale_quantity = ttk.Entry(mainwindow)
ent_sale_quantity.pack(side=tk.LEFT, padx=10, pady=5)

btn_sale_product = ttk.Button(mainwindow, text="Sell Product", command=sell_product)
btn_sale_product.pack(side=tk.LEFT, padx=10, pady=5)

mainwindow.mainloop()

######### END OF MAIN CODE - DO NOT EDIT BELOW THIS LINE !!!! #########
