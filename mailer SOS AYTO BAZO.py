# STABLE !!!
# version 2
'''
added some more info,like successfully sent message,and autoclose the form

'''

from tkinter import *
from tkinter import Label, messagebox
import sqlite3
import ssl
import smtplib
from email.message import EmailMessage
import ctypes  # This library will help us to hide the console
#bg = '#616A6B' # background color
#fg = '#34495A' # foreground color

# Hide the console window
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

mailerwindow = Tk()
mailerwindow.geometry('700x900')
#mailerwindow.configure(bg=bg)
mailerwindow.title('Mailer')
#mailerwindow.state('zoomed')#Maximize the window using state property
mailerwindow.state('normal')# use the defined dimensions

# Define and initialize search_by_var
search_by_var = StringVar()
search_by_var.set("Last Name")  # Set default value

# Radio buttons for search options
search_option_last_name = Radiobutton(mailerwindow, text="Search by Last Name", variable=search_by_var, value="Last Name", font=('', 12))#, fg=fg, bg=bg)
search_option_last_name.place(x=100, y=80)
search_option_customer_id = Radiobutton(mailerwindow, text="Search by Customer ID", variable=search_by_var, value="Customer ID", font=('', 12))#, fg=fg, bg=bg)
search_option_customer_id.place(x=300, y=80)

def send_mail():
    email_sender = 'leras1970@gmail.com'
    email_password = 'osjv weiu oymr sfsz'
    receiver_address = receiver.get()
    # Define msg here
    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = receiver_address
    # Get the message from the Text widget
    body = msg_body.get("1.0", END)
    msg.set_content(body)
    context = ssl.create_default_context()
    #chech if mail sent,wherever the email goes, and then close the form
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        messagebox.showinfo("Success", "Email sent successfully!")
        mailerwindow.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")


def clear_results():
    for widget in result_widgets:
        widget.destroy()

def search_name():
    search_term = search_entry.get().strip()
    connection = sqlite3.connect('crmdatabase200.db')
    cursor = connection.cursor()
    
    if search_by_var.get() == "Last Name":
        cursor.execute("SELECT email FROM customers WHERE last_name COLLATE NOCASE = ?", (search_term,))
    elif search_by_var.get() == "Customer ID":
        try:
            customer_id = int(search_term)
            cursor.execute("SELECT email FROM customers WHERE customerid = ?", (customer_id,))
        except ValueError:
            messagebox.showerror("Error", "Customer ID must be an integer.")
            connection.close()
            return
    else:
        messagebox.showerror("Error", "Invalid search option.")
        connection.close()
        return
    
    results = cursor.fetchall()
    connection.close()
    clear_results()
    
    recipient_label = Label(mailerwindow, text="EMAIL RECIPIENT:", font=('', 10))#, fg=fg, bg=bg)
    recipient_label.place(x=100, y=150)
    
    for i, result in enumerate(results):
        email = result[0]
        label = Label(mailerwindow, text=email, font=('', 10))#, fg=fg, bg=bg)
        label.place(x=100, y=230 + i * 30)
        add_to_receiver_btn = Button(mailerwindow, text="<== Select Customer", font=('', 10), command=lambda email=email: add_to_receiver(email))
        add_to_receiver_btn.place(x=450, y=230 + i * 30)
        result_widgets.append(label)
        result_widgets.append(add_to_receiver_btn)

def add_to_receiver(email):
    receiver.delete(0, END)
    receiver.insert(0, email)

# Function to clear the search entry field and displayed results
def clear_search():
    search_entry.delete(0, END)
    clear_results()
	
# Button to clear the search
clear_search_button = Button(mailerwindow, text="Clear Search", font=('', 10),  command=clear_search)
clear_search_button.place(x=280, y=10)  # Adjust position as needed    

Label(mailerwindow, text="Message: ", font=('', 10)).place(x=100, y=420) # y=118   

receiver = Entry(mailerwindow, font=('', 10), width=50)
receiver.place(x=100, y=180)#x= 128 , y=78

# the message box
msg_body = Text(mailerwindow, height=18, width=50, font=('', 10))
msg_body.place(x=100, y=450)#x= 128, y=118

# display the results of customers search
search_entry = Entry(mailerwindow, font=('', 10), width=50)
search_entry.place(x=100, y=50)# on top

search_button = Button(mailerwindow, text="Search Customer", font=('', 10), command=search_name, activebackground='green', activeforeground='green')
search_button.place(x=100, y=10) # (x=128, y=80)

# the send button
Button(mailerwindow, text="Send email", font=('', 10),  command=send_mail, activebackground='green', activeforeground='green').place(x=100, y=800)# x=100, y=600

result_widgets = []
mailerwindow.mainloop()
##########################