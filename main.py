import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import hashlib
import datetime
from database import connect_db

# We'll use a simple SHA-256 hash for passwords.
# Note: In a real-world app, you should use a salt with a library like bcrypt.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x500")
        
        # We will use a sleek dark mode color palette (Nord Theme colors)
        self.bg_color = "#2E3440"
        self.fg_color = "#ECEFF4"
        self.input_bg = "#3B4252"
        self.accent_color = "#88C0D0"
        self.success_color = "#A3BE8C"
        
        self.root.configure(bg=self.bg_color)
        
        # We start by showing the login frame
        self.current_user_id = None
        self.show_login_frame()

    def clear_window(self):
        # Destroy all widgets currently on the window
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_frame(self):
        self.clear_window()
        self.root.geometry("400x500") # Ensure window size is correct for login
        
        # Create a frame to hold the login UI
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Title
        title_label = tk.Label(frame, text="Welcome Back", font=("Helvetica", 24, "bold"), fg=self.fg_color, bg=self.bg_color)
        title_label.pack(pady=(0, 30))
        
        # Username Input
        tk.Label(frame, text="Username", font=("Helvetica", 12), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.login_username = tk.Entry(frame, font=("Helvetica", 12), bg=self.input_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.login_username.pack(fill="x", pady=(5, 15), ipady=8)
        
        # Password Input
        tk.Label(frame, text="Password", font=("Helvetica", 12), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.login_password = tk.Entry(frame, font=("Helvetica", 12), show="*", bg=self.input_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.login_password.pack(fill="x", pady=(5, 25), ipady=8)
        
        # Login Button
        login_btn = tk.Button(frame, text="LOGIN", font=("Helvetica", 12, "bold"), bg=self.accent_color, fg=self.bg_color, activebackground="#81A1C1", relief="flat", command=self.process_login)
        login_btn.pack(fill="x", pady=10, ipady=8)
        
        # Register Link
        register_link = tk.Label(frame, text="Don't have an account? Register", font=("Helvetica", 10, "underline"), fg="#8FBCBB", bg=self.bg_color, cursor="hand2")
        register_link.pack(pady=10)
        # Bind left mouse click to switch to the registration frame
        register_link.bind("<Button-1>", lambda e: self.show_register_frame())

    def show_register_frame(self):
        self.clear_window()
        self.root.geometry("400x500")
        
        # Register UI Frame
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        title_label = tk.Label(frame, text="Create Account", font=("Helvetica", 24, "bold"), fg=self.fg_color, bg=self.bg_color)
        title_label.pack(pady=(0, 30))
        
        # Username Input
        tk.Label(frame, text="Username", font=("Helvetica", 12), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.reg_username = tk.Entry(frame, font=("Helvetica", 12), bg=self.input_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.reg_username.pack(fill="x", pady=(5, 15), ipady=8)
        
        # Password Input
        tk.Label(frame, text="Password", font=("Helvetica", 12), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.reg_password = tk.Entry(frame, font=("Helvetica", 12), show="*", bg=self.input_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.reg_password.pack(fill="x", pady=(5, 25), ipady=8)
        
        # Register Button
        reg_btn = tk.Button(frame, text="REGISTER", font=("Helvetica", 12, "bold"), bg=self.success_color, fg=self.bg_color, activebackground="#8FBCBB", relief="flat", command=self.process_register)
        reg_btn.pack(fill="x", pady=10, ipady=8)
        
        # Login Link
        login_link = tk.Label(frame, text="Already have an account? Login", font=("Helvetica", 10, "underline"), fg="#8FBCBB", bg=self.bg_color, cursor="hand2")
        login_link.pack(pady=10)
        login_link.bind("<Button-1>", lambda e: self.show_login_frame())

    def process_register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        hashed_pw = hash_password(password)
        
        try:
            conn = connect_db()
            cursor = conn.cursor()
            # We use parameterized queries (?) to prevent SQL Injection!
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.show_login_frame()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        hashed_pw = hash_password(password)
        
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
            user = cursor.fetchone() # Fetches the first row that matches our query
            conn.close()
            
            if user:
                # user[0] is the 'id' column from our database
                self.current_user_id = user[0]
                messagebox.showinfo("Success", "Logged in successfully!")
                self.show_dashboard_frame()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_dashboard_frame(self):
        self.clear_window()
        self.root.geometry("800x600") # Enlarge window for dashboard
        
        # Main Layout
        left_frame = tk.Frame(self.root, bg=self.bg_color, width=250)
        left_frame.pack(side="left", fill="y", padx=20, pady=20)
        
        right_frame = tk.Frame(self.root, bg=self.bg_color)
        right_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        # --- LEFT FRAME (Input Form) ---
        tk.Label(left_frame, text="Add Expense", font=("Helvetica", 16, "bold"), fg=self.fg_color, bg=self.bg_color).pack(pady=(0, 20))
        
        # Date
        tk.Label(left_frame, text="Date (YYYY-MM-DD)", font=("Helvetica", 10), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.exp_date = tk.Entry(left_frame, bg=self.input_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.exp_date.pack(fill="x", pady=(2, 10), ipady=5)
        
        # Category
        tk.Label(left_frame, text="Category", font=("Helvetica", 10), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.exp_category = ttk.Combobox(left_frame, values=["Food", "Transport", "Utilities", "Entertainment", "Other"])
        self.exp_category.pack(fill="x", pady=(2, 10), ipady=5)
        
        # Amount
        tk.Label(left_frame, text="Amount", font=("Helvetica", 10), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.exp_amount = tk.Entry(left_frame, bg=self.input_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.exp_amount.pack(fill="x", pady=(2, 10), ipady=5)
        
        # Description
        tk.Label(left_frame, text="Description", font=("Helvetica", 10), fg="#D8DEE9", bg=self.bg_color).pack(anchor="w")
        self.exp_desc = tk.Entry(left_frame, bg=self.input_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.exp_desc.pack(fill="x", pady=(2, 20), ipady=5)
        
        # Buttons
        tk.Button(left_frame, text="ADD EXPENSE", font=("Helvetica", 10, "bold"), bg=self.accent_color, fg=self.bg_color, relief="flat", command=self.add_expense).pack(fill="x", pady=5, ipady=5)
        tk.Button(left_frame, text="VIEW REPORTS", font=("Helvetica", 10, "bold"), bg="#B48EAD", fg=self.fg_color, relief="flat", command=self.show_reports_window).pack(fill="x", pady=5, ipady=5)
        tk.Button(left_frame, text="LOGOUT", font=("Helvetica", 10, "bold"), bg="#BF616A", fg=self.fg_color, relief="flat", command=self.show_login_frame).pack(fill="x", pady=20, ipady=5)
        
        # --- RIGHT FRAME (Treeview) ---
        tk.Label(right_frame, text="Your Expenses", font=("Helvetica", 16, "bold"), fg=self.fg_color, bg=self.bg_color).pack(pady=(0, 20))
        
        # Setup Treeview (Table)
        columns = ("id", "date", "category", "amount", "description")
        
        # Add a scrollbar
        tree_scroll = tk.Scrollbar(right_frame)
        tree_scroll.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=0, stretch=tk.NO) # Hide ID column
        self.tree.heading("date", text="Date")
        self.tree.column("date", width=100)
        self.tree.heading("category", text="Category")
        self.tree.column("category", width=100)
        self.tree.heading("amount", text="Amount")
        self.tree.column("amount", width=80)
        self.tree.heading("description", text="Description")
        self.tree.column("description", width=200)
        
        self.tree.pack(fill="both", expand=True)
        
        # Delete Button
        tk.Button(right_frame, text="DELETE SELECTED", font=("Helvetica", 10, "bold"), bg="#EBCB8B", fg=self.bg_color, relief="flat", command=self.delete_expense).pack(anchor="e", pady=10, ipady=5)
        
        self.load_expenses()

    def add_expense(self):
        date = self.exp_date.get().strip()
        category = self.exp_category.get().strip()
        amount_str = self.exp_amount.get().strip()
        desc = self.exp_desc.get().strip()
        
        if not date or not category or not amount_str:
            messagebox.showerror("Error", "Date, Category, and Amount are required.")
            return
            
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format.")
            return
            
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.")
            return
            
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (user_id, date, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                           (self.current_user_id, date, category, amount, desc))
            conn.commit()
            conn.close()
            
            # Clear inputs
            self.exp_date.delete(0, tk.END)
            self.exp_amount.delete(0, tk.END)
            self.exp_desc.delete(0, tk.END)
            self.exp_category.set('')
            
            self.load_expenses()
            messagebox.showinfo("Success", "Expense added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {e}")

    def load_expenses(self):
        # Clear existing items in tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, date, category, amount, description FROM expenses WHERE user_id = ? ORDER BY date DESC", (self.current_user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                # We format the amount dynamically to show 2 decimal places
                formatted_row = (row[0], row[1], row[2], f"${row[3]:.2f}", row[4])
                self.tree.insert("", tk.END, values=formatted_row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load expenses: {e}")

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to delete.")
            return
            
        # Get the ID of the selected expense from the hidden first column
        expense_id = self.tree.item(selected_item[0])['values'][0]
        
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?")
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, self.current_user_id))
                conn.commit()
                conn.close()
                
                self.load_expenses()
                messagebox.showinfo("Success", "Expense deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete expense: {e}")

    def show_reports_window(self):
        reports_win = tk.Toplevel(self.root)
        reports_win.title("Monthly Reports")
        reports_win.geometry("500x400")
        reports_win.configure(bg=self.bg_color)
        
        tk.Label(reports_win, text="Monthly Expenses by Category", font=("Helvetica", 16, "bold"), fg=self.fg_color, bg=self.bg_color).pack(pady=20)
        
        columns = ("month", "category", "total")
        
        # Add a scrollbar for reports
        tree_scroll = tk.Scrollbar(reports_win)
        tree_scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(reports_win, columns=columns, show="headings", height=10, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading("month", text="Month (YYYY-MM)")
        tree.column("month", width=120, anchor="center")
        tree.heading("category", text="Category")
        tree.column("category", width=150, anchor="center")
        tree.heading("total", text="Total Amount")
        tree.column("total", width=120, anchor="e")
        
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        try:
            conn = connect_db()
            cursor = conn.cursor()
            # SQLite substr(date, 1, 7) extracts YYYY-MM
            cursor.execute("""
                SELECT substr(date, 1, 7) as month, category, SUM(amount) as total
                FROM expenses
                WHERE user_id = ?
                GROUP BY month, category
                ORDER BY month DESC, total DESC
            """, (self.current_user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                formatted_row = (row[0], row[1], f"${row[2]:.2f}")
                tree.insert("", tk.END, values=formatted_row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reports: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
