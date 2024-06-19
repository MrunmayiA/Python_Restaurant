from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import NavigationToolbar2
from BACKRest import *
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUIRest:
    def __init__(self, root):
        self.root = root
        self.orders = []  # Initialize the orders list
        
        self.label = tk.Label(root, text="Restaurant Management", font=("arial", 18, "bold"), fg='white', bg='#021024',relief='raised', height=2, width=50)
        self.label.pack(fill=BOTH, padx=2, pady=2)

        menuLabel = Label(root, text="Menu Card",bg='#7DA0CA',fg='#052659', font=("arial", 12, "bold"))
        menuLabel.place(x=20, y=100)

        self.menuCombo = ttk.Combobox(root, height=10, width=40, values=['Coffee', 'Tea', 'Lemonade', 'Samosa'])
        self.item_prices = {'Coffee': 50.00, 'Tea': 25.00, 'Lemonade': 40.00, 'Samosa': 45.00}
        self.menuCombo.place(x=20, y=130)

        qntLabel = Label(root, text="Quantity",bg='#7DA0CA',fg='#052659', font=("arial", 12, "bold"))
        qntLabel.place(x=20, y=160)

        spinbox_var = StringVar()
        self.qntSpin = Spinbox(root, from_=0, to=15, justify=CENTER, font=("arial", 10, "bold"), width=47, textvariable=spinbox_var)
        spinbox_var.set("1")
        self.qntSpin.place(x=20, y=190)

        addButton = Button(root, text="Add Item", width=40, background='#021024', foreground='white',command=self.add_order)
        addButton.place(x=20, y=260)

        self.pie_chart_frame = tk.Frame(root, bg='white', width=350, height=350)
        self.pie_chart_frame.place(x=20, y=340)

        self.update=Button(root,text="Update",width=45,height=1,background='#021024', foreground='white',command=self.update_database_gui)
        self.update.place(x=600,y=750)

        # Order Information Frame
        frameRight = tk.LabelFrame(root, width=800, height=600, text="Order Information", font=("arial", 10, "bold"),background='#7DA0CA')
        frameRight.place(x=400,y=100)
        #frameRight.pack(padx=20,side=RIGHT)

        # Frame components
        date = Label(frameRight, text="Date:", font=("arial", 10, "bold"),fg='#021024',bg='#7DA0CA')
        date.place(x=20, y=10)

        dateLabel = Label(frameRight, text="Date:", font=("arial", 10, "bold"),fg='#021024',bg='#7DA0CA')
        dateLabel.place(x=300, y=10)
        disp_date(dateLabel)

        custId = Label(frameRight, text="Customer ID:", font=("arial", 10, "bold"),fg='#021024',bg='#7DA0CA')
        custId.place(x=20, y=50)

        randomID = custIDGene()
        self.custIdNum = Label(frameRight, text=str(randomID), font=("arial", 10, "bold"),fg='#052659',bg='#7DA0CA')
        self.custIdNum.place(x=300, y=50)

        tabelno = Label(frameRight, text="Table Number:", font=("arial", 10, "bold"),fg='#021024',bg='#7DA0CA')
        tabelno.place(x=20, y=100)

        self.tableNoEn = Entry(frameRight, width=23, justify=LEFT, font=("arial", 10, "bold"),fg='#052659')
        self.tableNoEn.place(x=300, y=100)

        paymeth = Label(frameRight, text="Payment Method:", font=("arial", 10, "bold"),fg='#021024',bg='#7DA0CA')
        paymeth.place(x=20, y=150)

        self.paymethEn = ttk.Combobox(frameRight, height=10, width=20,values=['Cash', 'UPI', 'Credit Card', 'Other'], font=("arial", 10, "bold"),foreground='#052659')
        self.paymethEn.place(x=300, y=150)

        self.tree = ttk.Treeview(frameRight, columns=('Item', 'Quantity', 'Cost'), show='headings', height=10)
        self.tree.heading('Item', text='Item')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Cost', text='Cost')
        self.tree.place(x=20, y=200)

        self.total = Label(frameRight, text="Total Amount Payable: 0.0", font=("arial", 12, "bold"),fg='#021024',bg='#7DA0CA')
        self.total.place(x=20, y=500)



    def calculate_cost(self, item, quantity):
        if item not in self.item_prices:
            raise ValueError(f"Invalid item: {item}")

        price = self.item_prices[item]
        return price * quantity

    def add_order(self):
        item = self.menuCombo.get()
        quantity = int(self.qntSpin.get())

        # Check if an item is selected in the Combobox
        if item:
            # Check if quantity is greater than zero before adding to the tree view
            if quantity > 0:
                total_cost = self.calculate_cost(item, quantity)
                add_item_to_treeview(self.tree, item, quantity, total_cost)
                # Add the order to the orders list
                self.orders.append((item, quantity, total_cost))
                self.update_total_cost()
            else:
                messagebox.showerror("Error", "Quantity should be greater than zero.")
        else:
            messagebox.showerror("Error", "Please select an item from the menu.")

    def update_total_cost(self):
        total_cost = self.get_total_cost()
        self.total.config(text=f"Total Amount Payable: {total_cost:.2f}")

    def get_total_cost(self):
        return sum(order[2] for order in self.orders)
    
    def update_database_gui(self):
        # Call the update_database function from BACKRest
        update_database(self.tree, self.orders, self.tableNoEn, self.paymethEn,self.custIdNum)  # Ensure the correct arguments are passed
        self.update_total_cost()
        self.update_pie_chart(self.orders) 

    
    def update_pie_chart(self, selected_items):
     # Clear previous pie chart
     for widget in self.pie_chart_frame.winfo_children():
        widget.destroy()

        if selected_items:
            pie_data = [item[2] for item in selected_items]

            # Specify colors for each slice
            colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow', 'brown', 'gray']

            # Change the figsize parameter in plt.subplots() to adjust the size of the pie chart
            fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

            # Plot the pie chart with colors
            ax.pie(pie_data, labels=[item[0] for item in selected_items], autopct='%1.1f%%', startangle=90, colors=colors)

         # Embed the pie chart in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.pie_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create a toolbar for the pie chart (optional)
            toolbar = NavigationToolbar2Tk(canvas, self.pie_chart_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Store the canvas reference to prevent it from being garbage collected
            self.pie_chart_canvas = canvas

        # Force an update of the main event loop
            plt.close('all')  # Close the original matplotlib window
        
    def display_pie_chart(self, fig):
          # Clear previous pie chart
        for widget in self.pie_chart_frame.winfo_children():
         widget.destroy()

        # Display new pie chart on the Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.pie_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.get_tk_widget().place(x=0, y=0)  # Adjusted placement

        # Create a toolbar for the pie chart (optional)
        toolbar = NavigationToolbar2Tk(canvas, self.pie_chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.get_tk_widget().pack_forget()
     

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIRest(root)
    root.geometry("1219x1000")
    root.config(background='#7DA0CA')
    root.mainloop()
