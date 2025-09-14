import tkinter as tk
from tkinter import messagebox

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = []
        self.load_expenses()

        tk.Label(root, text="Description:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(root, text="Amount:").grid(row=1, column=0, padx=5, pady=5)

        self.desc_entry = tk.Entry(root, width=30)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)

        self.amount_entry = tk.Entry(root, width=30)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.grid(row=3, column=0, columnspan=2, padx=5)

        self.total_label = tk.Label(root, text="Total Spent: $0.00", font=("Arial", 14))
        self.total_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.update_listbox()

    def add_expense(self):
        desc = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()
        if not desc or not amount:
            messagebox.showwarning("Input Error", "Please enter both description and amount.")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for amount.")
            return
        self.expenses.append({"desc": desc, "amount": amount})
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.update_listbox()
        self.save_expenses()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        total = 0
        for expense in self.expenses:
            self.listbox.insert(tk.END, f"{expense['desc']}: ${expense['amount']:.2f}")
            total += expense['amount']
        self.total_label.config(text=f"Total Spent: ${total:.2f}")

    def save_expenses(self):
        with open("expenses.txt", "w") as f:
            for expense in self.expenses:
                f.write(f"{expense['desc']}|{expense['amount']}\n")

    def load_expenses(self):
        try:
            with open("expenses.txt", "r") as f:
                for line in f:
                    desc, amount = line.strip().split("|")
                    self.expenses.append({"desc": desc, "amount": float(amount)})
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
