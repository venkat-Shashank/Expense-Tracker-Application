# 💰 My Expense Tracker Application

Welcome to my **Expense Tracker Application**! This is one of the first major Python desktop applications I've built entirely from scratch. I created this project to solidify my understanding of Object-Oriented Programming (OOP), database management, and building graphical user interfaces.

It was an incredible learning experience that pushed me out of my comfort zone, and I'm excited to share the code, my thought process, and the hurdles I overcame along the way.

---

## 🚀 The Motivation

I wanted to build something practical that I could actually use in my daily life, rather than just solving isolated coding exercises. Tracking expenses seemed like the perfect challenge because it required me to handle real user input, securely store that data, and retrieve it in a meaningful way (like generating monthly reports).

---

## 📚 Libraries Used & Why I Chose Them

Instead of relying on heavy third-party frameworks, I challenged myself to build this using Python's built-in libraries to truly understand the core mechanics of the language:

*   **`tkinter`**: I used this for the Graphical User Interface (GUI). It allowed me to build the windows, buttons, input fields, and the interactive data table (`Treeview`). It taught me a lot about event-driven programming and managing window lifecycles.
*   **`sqlite3`**: For the database! Instead of using simple text files, I wanted a real relational database. SQLite is lightweight and built right into Python, making it perfect for a local desktop app. It challenged me to write raw SQL queries for creating, reading, updating, and deleting data (CRUD).
*   **`hashlib`**: Security is important. I used `hashlib` (specifically the SHA-256 algorithm) to encrypt user passwords before saving them to the database. Even for a local app, I wanted to practice secure coding habits.
*   **`datetime`**: Handling dates is notoriously tricky. I used this module to strictly validate user input (ensuring the `YYYY-MM-DD` format) so my database wouldn't crash from bad formatting.

---

## 🧗‍♂️ My Journey & The Struggles I Faced

Building this wasn't a straight, easy path. Here are a few major roadblocks I hit and how I solved them:

1.  **Taming the Tkinter Layout Manager**: 
    Initially, getting the input form to sit nicely next to the data table was a nightmare. I struggled with the `.pack()` manager, often having widgets overlap, stretch weirdly, or disappear altogether. 
    *The Fix:* I learned to use `Frame` widgets as containers. By creating a `left_frame` for inputs and a `right_frame` for the table, and packing them side-by-side, I finally achieved the clean, split layout you see today.
2.  **Preventing SQL Injection**: 
    When I first wrote my database insertion code, I was using Python f-strings to pass variables directly into my SQL commands. I quickly learned through research that this is a huge security risk!
    *The Fix:* I refactored all my database functions to use parameterized queries (using the `?` placeholder), letting the `sqlite3` library safely escape the user input for me.
3.  **The "Silent" Database Errors**: 
    Early on, I would click "Add Expense" and nothing would happen. No crash, but no data in the database either. 
    *The Fix:* I realized I was forgetting to call `conn.commit()` after inserting data! I also learned the hard way to wrap my database calls in `try...except` blocks so the app would use `messagebox` to actually tell me *why* it failed instead of failing silently in the background.
4.  **Date Aggregation for Reports**: 
    Figuring out how to group daily expenses into Monthly Reports was tough. I didn't want to pull all the data into Python and sort it manually if the database could do it for me.
    *The Fix:* I had to dive deep into SQLite documentation and discovered the `substr()` function. By using `SELECT substr(date, 1, 7)`, I was able to extract just the Year and Month dynamically, allowing me to `GROUP BY` month and category in a single, efficient query!

---

## 🧠 Key Takeaways / What I Learned

By completing this project, I significantly leveled up my skills in:
*   **Object-Oriented Programming**: Organizing my entire UI and logic inside a single, cohesive `ExpenseTrackerApp` class.
*   **CRUD Operations**: Mastering Create, Read, Update, and Delete database fundamentals.
*   **Data Validation**: Never trusting user input! Catching `ValueErrors` before they break the application.
*   **Debugging**: Reading traceback errors and using them to trace logic flaws in my code.

---

## 🛠️ How to Run It Yourself

If you'd like to check out my code and run the app, follow these steps:

### Prerequisites
*   Python 3.8 or higher installed on your system.

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/expense-tracker.git
    cd expense-tracker
    ```
2.  **Initialize the Database**:
    Run the `database.py` script once. This creates the local `expense_tracker.db` file and sets up the `users` and `expenses` tables.
    ```bash
    python database.py
    ```
    *(Note: On Windows, use `py database.py`)*

3.  **Launch the App**:
    ```bash
    python main.py
    ```

---

## 📸 Application Previews

*(Tip: Take some screenshots of your app using Windows Snipping Tool, save them in the project folder, and add their filenames below!)*

*   **Login & Registration Screen**
    `![Login Screen](login_screenshot.png)`
*   **Main Expense Dashboard**
    `![Dashboard](dashboard_screenshot.png)`
*   **Monthly Reports View**
    `![Reports](reports_screenshot.png)`

---

Thank you for checking out my project! If you have any feedback or suggestions, feel free to open an issue or reach out.

**Author**: G. Venkata Shashank
