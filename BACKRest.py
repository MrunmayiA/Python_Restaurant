import tkinter as  tk
from tkinter import ttk
from datetime import datetime
import sqlite3
from tkinter import messagebox
import random
import os

def disp_date(dateLabel):
 current_date=datetime.now().strftime("%A, %d %B , %Y")
 dateLabel=dateLabel.config(text =current_date)

def custIDGene():
 return random.randint(1000,9999)

def add_item(self, item, quantity):
 price = self.get_price_for_item(item) 
 self.tree.insert("", "end", values=(item, quantity, price))

def add_item_to_treeview(tree, item, quantity, total_cost):
    tree.insert("", "end", values=(item, quantity,  total_cost))


def get_price_for_item(item):
    # Replace this with your logic to get the price for the item
    prices = {'Coffee': 2.5, 'Tea': 1.8, 'Lemonade': 3.2, 'Samosa': 5.0}
    return prices.get(item, 0.0)

def update_database(tree, orders, tableNoEn, paymethEn,custIdNum):
    # Connect to the SQLite database
    db_file_path = 'Restaurant.db'
    if not os.path.exists(db_file_path):
        conn = sqlite3.connect(db_file_path)
        conn.close()
    conn = sqlite3.connect('Restaurant.db')
    cursor = conn.cursor()

    try:
        # Create the "Orders" table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                CustomerID INTEGER PRIMARY KEY,
                Date TEXT,
                TableNumber INTEGER,
                PaymentMethod TEXT,
                TotalCost REAL
            )
        ''')

        # Create the "OrderItems" table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS OrderItems (
                OrderID INTEGER,
                Item TEXT,
                Quantity INTEGER,
                Cost REAL,
                FOREIGN KEY (OrderID) REFERENCES Orders(CustomerID)
            )
        ''')

        # Insert data into the database
        custId=custIDGene()
        date = datetime.now().strftime("%A, %d %B , %Y")
        table_number = int(tableNoEn.get())  # Get table number from the Entry widget
        payment_method = paymethEn.get()
        total_cost = sum(order[2] for order in orders)

        # Insert order information into the database
        cursor.execute('''
            INSERT INTO Orders (CustomerID, Date, TableNumber, PaymentMethod, TotalCost)
            VALUES (?, ?, ?, ?, ?)
        ''', (custId, date, table_number, payment_method, total_cost))

        # Get the last inserted CustomerID (primary key)
        customer_id = cursor.lastrowid

        # Insert item details into the database
        for order in orders:
            item, quantity, item_cost = order
            cursor.execute('''
                INSERT INTO OrderItems (OrderID, Item, Quantity, Cost)
                VALUES (?, ?, ?, ?)
            ''', (custId, item, quantity, item_cost))

        # Commit the changes to the database
        conn.commit()

        # Show a success message
        messagebox.showinfo("Success", "Order updated in the database.")
        print_database_data(cursor)
        #print_data(cursor)

        

        # Clear the Treeview and orders list
        tree.delete(*tree.get_children())
        orders.clear()

    except Exception as e:
        # Handle errors
        messagebox.showerror("Error", f"Error updating database: {str(e)}")

    finally:
        # Close the database connection
        conn.close()


# def print_data(cursor):
#     cursor.execute('SELECT * FROM Orders')
#     orders_data = cursor.fetchall()
#     print("Orders Table:")
#     print("CustomerID | Date | TableNumber | PaymentMethod | TotalCost")
#     for order in orders_data:
#         print(order)

#     # Fetch and print data from the OrderItems table
#     cursor.execute('SELECT * FROM OrderItems')
#     order_items_data = cursor.fetchall()
#     print("\nOrderItems Table:")
#     print("OrderID | Item | Quantity | Cost")
#     for order_item in order_items_data:
#         print(order_item)

def print_database_data(cursor):
        # Fetch and print data from the Orders table
        cursor.execute('SELECT * FROM Orders')
        orders_data = cursor.fetchall()
        print("Orders Table:")
        print("CustomerID | Date | TableNumber | PaymentMethod | TotalCost")
        for order in orders_data:
            print(order)

        # Fetch and print data from the OrderItems table
        cursor.execute('SELECT * FROM OrderItems')
        order_items_data = cursor.fetchall()
        print("\nOrderItems Table:")
        print("OrderID | Item | Quantity | Cost")
        for order_item in order_items_data:
            print(order_item)
