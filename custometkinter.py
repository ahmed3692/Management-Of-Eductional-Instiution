import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sqlite3

# Function to handle login


def login():
    email = entry_email.get().strip()  # Get email from entry widget
    password = entry_password.get().strip()

    # Connect to SQLite database
    db = sqlite3.connect(
        "employees.db")
    x = db.cursor()

    # Query to select user by email
    x.execute("SELECT * FROM employee WHERE email = ?", (email,))
    data = x.fetchall()

    # If the email is found in the database
    if data:
        # Check if the password matches
        # Assuming password is the third field in the result
        stored_password = data[0][2]
        if str(stored_password) == password:
            role = data[0][3].strip().upper()
            if role == "ADMIN":
                show_admin_gui()
            elif role == "TEACHER":
                show_teacher_gui()
            elif role == "STAFF":
                show_employee_gui()

        else:
            messagebox.showerror("Login Error", "Incorrect password!")
    else:
        messagebox.showerror("Login Error", "Email not found!")

    db.close()  # Close the database connection


# Admin GUI

def show_admin_gui():
    root.withdraw()  # Hide the main window
    admin_window = ctk.CTkToplevel()  # Create a new Toplevel window
    admin_window.title("Admin Panel")
    admin_window.geometry("800x500")

    # Dashboard label
    ctk.CTkLabel(
        admin_window,
        text="Admin Dashboard",
        font=("Arial", 16),  # No bold
        text_color="#007BFF"  # Primary blue color
    ).pack(pady=10)

    # Employee and Student Management Buttons
    management_buttons = [
        {"text": "Manage Employees", "color": "#007BFF",
            "command": lambda: manage_employees(admin_window)},
        {"text": "Manage Students", "color": "#007BFF",
            "command": lambda: manage_students(admin_window)},
    ]

    # Create buttons for management options
    for btn in management_buttons:
        ctk.CTkButton(
            admin_window,
            text=btn["text"],
            fg_color=btn["color"],  # Blue background color
            text_color="white",  # White text for contrast
            font=("Arial", 14),  # No bold, slightly larger size
            width=200,  # Wider buttons
            height=40,  # Height for better usability
            corner_radius=10,  # Rounded corners for a modern look
            command=btn["command"],
        ).pack(pady=10)

    # Logout Button
    ctk.CTkButton(
        admin_window,
        text="Logout",
        fg_color="#1E90FF",  # Blue shade for the logout button
        text_color="white",  # White text for readability
        font=("Arial", 14),  # No bold
        width=200,  # Consistent width
        height=40,  # Consistent height
        corner_radius=10,  # Rounded corners
        command=lambda: logout(admin_window),
    ).pack(pady=20)


# Separate Employee and Student Management GUIs
def manage_employees(parent_window):
    parent_window.withdraw()
    employee_window = ctk.CTkToplevel()
    employee_window.title("Employee Management")
    employee_window.geometry("800x500")

    # Label for the Employee Management header
    ctk.CTkLabel(
        employee_window,
        text="Employee Management",
        font=("Arial", 16, "bold"),
        text_color="#007BFF"  # Blue header for employee management
    ).pack(pady=10)

    # Button configurations with blue shades
    employee_buttons = [
        {"text": "Add Employee", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: add_employee(employee_window)},
        {"text": "Remove Employee", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: remove_employee(employee_window)},
        {"text": "Search Employee", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: search_employee(employee_window)},
        {"text": "Update Employee", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: update_employee(employee_window)},
    ]

    # Create buttons dynamically
    for btn in employee_buttons:
        ctk.CTkButton(
            employee_window,
            text=btn["text"],
            fg_color=btn["fg_color"],  # Background color
            text_color=btn["text_color"],  # Foreground color
            font=("Arial", 14),  # Font size consistent with `show_admin_gui`
            width=200,  # Button width
            height=40,  # Button height
            corner_radius=10,  # Rounded corners
            command=btn["command"],
        ).pack(pady=10)

    # Back button to return to parent window
    ctk.CTkButton(
        employee_window,
        text="Back",
        fg_color="#1E90FF",  # Blue shade for the Back button
        text_color="white",
        font=("Arial", 14),  # Font size consistent with other buttons
        width=200,  # Button width
        height=40,  # Button height
        corner_radius=10,  # Rounded corners
        command=lambda: back_to_main(employee_window, parent_window),
    ).pack(pady=20)


def manage_students(parent_window):
    parent_window.withdraw()
    student_window = ctk.CTkToplevel()
    student_window.title("Student Management")
    student_window.geometry("800x500")

    # Label for the Student Management header
    ctk.CTkLabel(
        student_window,
        text="Student Management",
        font=("Arial", 16),  # No bold
        text_color="#007BFF"  # Blue text color
    ).pack(pady=10)

    # Button configurations with blue shades
    student_buttons = [
        {"text": "Add Student", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: add_student(student_window)},
        {"text": "Remove Student", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: remove_student(student_window)},
        {"text": "Search Student", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: search_student(student_window)},
        {"text": "Update Student", "fg_color": "#007BFF", "text_color": "white",
            "command": lambda: update_student(student_window)},
    ]

    # Create buttons dynamically
    for btn in student_buttons:
        ctk.CTkButton(
            student_window,
            text=btn["text"],
            fg_color=btn["fg_color"],  # Background color
            text_color=btn["text_color"],  # Foreground color
            font=("Arial", 14),  # Font size increased for readability
            width=200,  # Wider buttons
            height=40,  # Height in pixels
            corner_radius=10,  # Rounded corners for modern look
            command=btn["command"],
        ).pack(pady=10)

    # Back button to return to parent window
    ctk.CTkButton(
        student_window,
        text="Back",
        fg_color="#1E90FF",  # Blue shade for Back button
        text_color="white",
        font=("Arial", 14),  # Font size consistent with other buttons
        width=200,
        height=40,
        corner_radius=10,
        command=lambda: back_to_main(student_window, parent_window),
    ).pack(pady=20)


# Example placeholder functions for employee and student management


def add_employee(employee_window):
    def save_employee():
        # Get data from entry fields
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()
        role = selected_role.get()
        ID10 = entry_id.get().strip()

        # Check if all fields are filled
        if not name or not email or not password or not role or not ID10:
            messagebox.showerror("Error", "All fields are required!")
            return
        dbstnd = sqlite3.connect("student.db")
        stnd = dbstnd.cursor()
        # Check if ID already exists
        stnd.execute("SELECT ID FROM student WHERE ID = ?", (ID10,))
        if stnd.fetchone():
            messagebox.showerror("Error", "ID already exists!")
            dbstnd.close()
            return

        # Check if Email already exists
        stnd.execute("SELECT EMAIL FROM student WHERE EMAIL = ?", (email,))
        if stnd.fetchone():
            messagebox.showerror("Error", "Email already exists!")
            dbstnd.close()
            return
        dbstnd.close()

        # Connect to the database
        db = sqlite3.connect('employees.db')
        cursor = db.cursor()

        # Check if ID already exists
        cursor.execute("SELECT ID FROM employee WHERE ID = ?", (ID10,))
        if cursor.fetchone():
            messagebox.showerror("Error", "ID already exists!")
            db.close()
            return

        # Check if Email already exists
        cursor.execute("SELECT EMAIL FROM employee WHERE EMAIL = ?", (email,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Email already exists!")
            db.close()
            return

        # Insert the new employee into the database
        cursor.execute(
            "INSERT INTO employee (NAME, EMAIL, PASSWORD, ROLE, ID) VALUES (?, ?, ?, ?, ?)",
            (name, email, password, role, ID10)
        )
        db.commit()
        db.close()

        # Show success message and close window
        messagebox.showinfo("Success", "Employee added successfully!")
        add_window.destroy()
        if role == "teacher":
            add_timetable(email, ID10, employee_window)
        employee_window.deiconify()

# Create the add employee window
    employee_window.withdraw()
    add_window = ctk.CTkToplevel()
    add_window.title("Add Employee")
    add_window.geometry("800x600")

# Input fields and labels
    ctk.CTkLabel(add_window, text="Name").pack(pady=5)
    entry_name = ctk.CTkEntry(add_window, width=250, height=30)
    entry_name.pack(pady=5)

    ctk.CTkLabel(add_window, text="Email").pack(pady=5)
    entry_email = ctk.CTkEntry(add_window, width=250, height=30)
    entry_email.pack(pady=5)

    ctk.CTkLabel(add_window, text="Password").pack(pady=5)
    entry_password = ctk.CTkEntry(add_window, width=250, height=30, show="*")
    entry_password.pack(pady=5)

    ctk.CTkLabel(add_window, text="Role").pack(pady=5)
# Dropdown menu for role selection
    roles = ["staff", "teacher"]
    selected_role = ctk.StringVar(value=roles[0])  # Default to "staff"
    role_menu = ctk.CTkOptionMenu(
        add_window, variable=selected_role, values=roles, width=250, height=30)
    role_menu.pack(pady=5)

    ctk.CTkLabel(add_window, text="ID").pack(pady=5)
    entry_id = ctk.CTkEntry(add_window, width=250, height=30)
    entry_id.pack(pady=5)

# Buttons for save and back
    ctk.CTkButton(add_window, text="Save", width=150, height=40,
                  fg_color="#007BFF", command=save_employee).pack(pady=10)
    ctk.CTkButton(add_window, text="Back", width=150, height=40, fg_color="#007BFF",
                  command=lambda: back_to_main(add_window, employee_window)).pack(pady=20)


def remove_employee(employee_window):

    def remove():
        id = entry_ID.get().strip()
        if not id:
            messagebox.showerror("Error", "All fields are required!")
            return

        db = sqlite3.connect('employees.db')
        r = db.cursor()
        r.execute("SELECT * FROM employee WHERE ID=?", (id,))
        role = r.fetchone()
        if role is None:
            messagebox.showerror("Error", "ID not found!")

            db.close()
            return

        ch_role = role[3].strip().upper()

        if ch_role == "ADMIN":
            messagebox.showinfo("Error", "ADMIN not remove")
            db.close()
            remove_window.destroy()
            employee_window.deiconify()
            return

        r.execute("DELETE FROM employee WHERE ID=?", (id,))
        db.commit()

        if ch_role == "TEACHER":
            messagebox.showinfo("Success", "Teacher removed successfully!")
            z = sqlite3.connect("timetable.db")
            D = z.cursor()
            D.execute("DELETE FROM tae WHERE ID=?", (id,))
            z.commit()
            z.close()
            remove_window.destroy()
            employee_window.deiconify()
        elif ch_role == "STAFF":
            messagebox.showinfo("Success", "STAFF removed successfully!")
            remove_window.destroy()
            employee_window.deiconify()
        db.close()

    employee_window.withdraw()
    remove_window = ctk.CTkToplevel()
    remove_window.title("Remove Employee")
    remove_window.geometry("800x500")

    ctk.CTkLabel(remove_window, text="ID").pack(pady=5)
    entry_ID = ctk.CTkEntry(remove_window, width=150, height=30)
    entry_ID.pack(pady=5)

    ctk.CTkButton(remove_window, text="Remove", width=150, height=40,
                  fg_color="#007BFF", command=remove).pack(pady=20)
    ctk.CTkButton(remove_window, text="Back", width=150, height=40, fg_color="#007BFF",
                  command=lambda: back_to_main(remove_window, employee_window)).pack(pady=20)


def search_employee(employee_window):
    def search_emp():
        search = entry_search.get().strip()
        if not search:
            messagebox.showerror("Error", "Search parameter is required!")
            return

        found = False
        db = sqlite3.connect("employees.db")
        sear = db.cursor()

        # Search by EMAIL
        sear.execute("SELECT * FROM employee WHERE EMAIL = ?", (search,))
        data = sear.fetchall()
        for row in data:
            result = row
            result_text = f"ID: {result[4]}\nName: {
                result[0]}\nEmail: {result[1]}\nRole: {result[3]}"
            # Use configure for CustomTkinter
            label_result.configure(text=result_text, text_color="green")
            found = True

        # Search by ID
        sear.execute("SELECT * FROM employee WHERE ID = ?", (search,))
        s1 = sear.fetchall()
        for row in s1:
            result = row
            result_text = f"ID: {result[4]}\nName: {
                result[0]}\nEmail: {result[1]}\nRole: {result[3]}"
            # Use configure for CustomTkinter
            label_result.configure(text=result_text, text_color="blue")
            found = True

        if not found:
            messagebox.showerror("Error", "Parameter not found")

        db.close()
# Create the search window
    employee_window.withdraw()
    search_window = ctk.CTkToplevel()
    search_window.title("Search Employee")
    search_window.geometry("800x500")

    ctk.CTkLabel(search_window, text="ID or EMAIL").pack(pady=5)
    entry_search = ctk.CTkEntry(search_window, width=200, height=20)
    entry_search.pack(pady=5)

    ctk.CTkButton(search_window, text="Search", fg_color="#007BFF",
                  width=100, height=20, command=search_emp).pack(pady=20)

    label_result = ctk.CTkLabel(
        search_window, text="", wraplength=500, justify="left", text_color="blue")
    label_result.pack(pady=20)

    ctk.CTkButton(search_window, text="Back", width=100, height=20, fg_color="#007BFF",
                  command=lambda: back_to_main(search_window, employee_window)).pack(pady=20)


def update_employee(employee_window):
    def update_emp():
        id = entry_id.get().strip()
        if not id:
            messagebox.showerror("Error", "ID field is required!")
            return

        # Connect to the database to fetch the employee record
        db = sqlite3.connect("employees.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employee WHERE ID=?", (id,))
        data = cursor.fetchone()

        if data is None:
            messagebox.showerror("Error", "ID not found!")
            db.close()
            return
        ch_role = data[3].strip().upper()
        if ch_role == "ADMIN":
            messagebox.showinfo("Error", "ADMIN not able to update")
            db.close()
            update_window.destroy()
            employee_window.deiconify()
            return

        # Open a new window to update employee details

        def new_value_emp():
            name = entry_name.get().strip()
            email = entry_email.get().strip()
            password = entry_password.get().strip()

            if not name or not email or not password:
                messagebox.showerror("Error", "All fields are required!")
                return

            db = sqlite3.connect("employees.db")
            cursor = db.cursor()

            cursor.execute(
                "SELECT ID FROM employee WHERE EMAIL = ? AND ID != ?", (email, id))
            existing_email = cursor.fetchone()

            if existing_email:
                db.close()
                messagebox.showerror(
                    "Error", "Email already exists! Update failed.")
                return

            db_stnd = sqlite3.connect("student.db")
            stnd_cursor = db_stnd.cursor()
            stnd_cursor.execute(
                "SELECT EMAIL FROM student WHERE EMAIL = ?", (email,))
            stnd_email = stnd_cursor.fetchone()
            if stnd_email:
                db_stnd.close()
                messagebox.showerror(
                    "Error", "Email already exists! Update failed.")
                return

            # Update the employee in the database
            db = sqlite3.connect("employees.db")
            cursor = db.cursor()
            cursor.execute(
                "UPDATE employee SET NAME = ?, EMAIL = ?, PASSWORD = ? WHERE ID = ?",
                (name, email, password, id)
            )
            db.commit()
            db.close()
            dbd = sqlite3.connect("timetable.db")
            cursor1 = dbd.cursor()
            cursor1.execute("UPDATE tae SET EMAIL = ? WHERE ID = ?",
                            (email, id))
            dbd.commit()
            dbd.close()

            messagebox.showinfo("Success", "Employee updated successfully!")
            new_value_window.destroy()

            employee_window.deiconify()

# Create a new window for updating employee details
        update_window.withdraw()
        new_value_window = ctk.CTkToplevel()
        new_value_window.title("Update Employee Details")
        new_value_window.geometry("800x500")

# Input fields and labels
        ctk.CTkLabel(new_value_window, text="Name").pack(pady=5)
        entry_name = ctk.CTkEntry(new_value_window, width=250, height=30)
        entry_name.insert(0, data[0])  # Pre-fill with existing name
        entry_name.pack(pady=5)

        ctk.CTkLabel(new_value_window, text="Email").pack(pady=5)
        entry_email = ctk.CTkEntry(new_value_window, width=250, height=30)
        entry_email.insert(0, data[1])  # Pre-fill with existing email
        entry_email.pack(pady=5)

        ctk.CTkLabel(new_value_window, text="Password").pack(pady=5)
        entry_password = ctk.CTkEntry(
            new_value_window, width=250, height=30, show="*")
        entry_password.insert(0, data[2])  # Pre-fill with existing password
        entry_password.pack(pady=5)

        ctk.CTkButton(new_value_window, text="Save", fg_color="#007BFF",
                      width=150, height=40, command=new_value_emp).pack(pady=20)
        ctk.CTkButton(new_value_window, text="Back", fg_color="#007BFF", width=150, height=40,
                      command=lambda: back_to_main(new_value_window, employee_window)).pack(pady=20)

    # Create the main update window
    employee_window.withdraw()
    update_window = ctk.CTkToplevel()
    update_window.title("Update Employee")
    update_window.geometry("800x500")

# Input field for Employee ID
    ctk.CTkLabel(update_window, text="Enter Employee ID").pack(pady=5)
    entry_id = ctk.CTkEntry(update_window, width=250,
                            height=30)  # Adjusted size
    entry_id.pack(pady=5)

    ctk.CTkButton(update_window, text="Find & Update", fg_color="#007BFF",
                  width=150, height=40, command=update_emp).pack(pady=20)
    ctk.CTkButton(update_window, text="Back", width=150, height=40, fg_color="#007BFF",
                  command=lambda: back_to_main(update_window, employee_window)).pack(pady=20)


def update_student(student_window):
    def update_std():
        student_id = entry_id.get().strip()
        if not student_id:
            messagebox.showerror("Error", "ID field is required!")
            return

        # Connect to the database to fetch the student record
        db = sqlite3.connect("student.db")
        cursor = db.cursor()
        cursor.execute(
            "SELECT NAME, EMAIL, Attendance, EXAMS FROM student WHERE ID=?", (student_id,))
        data = cursor.fetchone()
        db.close()

        if data is None:
            messagebox.showerror("Error", "Student ID not found!")
            return

        # Open a new window to update student details
        def new_value_std():
            name = entry_name.get().strip()
            email = entry_email.get().strip()
            attendance = entry_attendance.get().strip()
            degree = entry_examdegree.get().strip()

            if not name or not email or not attendance or not degree:
                messagebox.showerror("Error", "All fields are required!")
                return

            db = sqlite3.connect("student.db")
            cursor = db.cursor()

            cursor.execute(
                "SELECT ID FROM student WHERE EMAIL = ? AND ID != ?", (email, student_id))
            existing_email = cursor.fetchone()

            if existing_email:
                db.close()
                messagebox.showerror(
                    "Error", "Email already exists! Update failed.")
                return

            db_emp = sqlite3.connect("employees.db")
            emp_cursor = db_emp.cursor()
            emp_cursor.execute(
                "SELECT EMAIL FROM employee WHERE EMAIL = ?", (email,))
            emp_email = emp_cursor.fetchone()
            if emp_email:
                db_emp.close()
                messagebox.showerror(
                    "Error", "Email already exists! Update failed.")
                return
            degree = float(degree)
            if degree > 100 or degree < 0:
                messagebox.showerror("Error", "Degree between 0 to 100.")
                return
            attendance = int(attendance)
            if attendance < 0:
                messagebox.showerror("Error", "Attendance must more than 0.")
                return

            # Update the student in the database
            db = sqlite3.connect("student.db")
            cursor = db.cursor()
            cursor.execute(
                "UPDATE student SET NAME = ?, EMAIL = ?, Attendance = ?, EXAMS = ? WHERE ID = ?",
                (name, email, attendance, degree, student_id)
            )
            db.commit()
            db.close()

            messagebox.showinfo("Success", "Student updated successfully!")
            new_value_window.destroy()
            update_swindow.deiconify()

# Create window for updating student
        update_swindow.withdraw()
        new_value_window = ctk.CTkToplevel()
        new_value_window.title("Update Student Details")
        new_value_window.geometry("800x500")

        ctk.CTkLabel(new_value_window, text="Name").pack(pady=5)
        entry_name = ctk.CTkEntry(
            new_value_window, width=250, height=30)  # Adjusted size
        entry_name.insert(0, data[0])  # Pre-fill with existing name
        entry_name.pack(pady=5)

        ctk.CTkLabel(new_value_window, text="Email").pack(pady=5)
        entry_email = ctk.CTkEntry(
            new_value_window, width=250, height=30)  # Adjusted size
        entry_email.insert(0, data[1])  # Pre-fill with existing email
        entry_email.pack(pady=5)

        ctk.CTkLabel(new_value_window, text="Attendance").pack(pady=5)
        entry_attendance = ctk.CTkEntry(
            new_value_window, width=250, height=30)  # Adjusted size
        # Pre-fill with existing attendance
        entry_attendance.insert(0, data[2])
        entry_attendance.pack(pady=5)

        ctk.CTkLabel(new_value_window, text="Exams Degree").pack(pady=5)
        entry_examdegree = ctk.CTkEntry(
            new_value_window, width=250, height=30)  # Adjusted size
        # Pre-fill with existing exams degree
        entry_examdegree.insert(0, data[3])
        entry_examdegree.pack(pady=5)

        ctk.CTkButton(new_value_window, text="Save", fg_color="#007BFF",
                      width=150, height=40, command=new_value_std).pack(pady=20)
        ctk.CTkButton(new_value_window, text="Back", fg_color="#007BFF", width=150, height=40, command=lambda: (
            new_value_window.destroy(), student_window.deiconify())).pack(pady=10)


# Main update window
    student_window.withdraw()
    update_swindow = ctk.CTkToplevel()
    update_swindow.title("Update Student")
    update_swindow.geometry("800x500")  # Adjusted height for better spacing

    ctk.CTkLabel(update_swindow, text="Enter Student ID").pack(pady=5)
    entry_id = ctk.CTkEntry(update_swindow, width=250,
                            height=30)  # Adjusted size
    entry_id.pack(pady=5)

    ctk.CTkButton(update_swindow, text="Find", width=150,
                  fg_color="#007BFF", height=40, command=update_std).pack(pady=20)
    ctk.CTkButton(update_swindow, text="Back", width=150, fg_color="#007BFF", height=40,
                  command=lambda: back_to_main(update_swindow, student_window)).pack(pady=10)


def add_student(student_window):
    def save_student():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        student_id = entry_id.get().strip()

        if not name or not email or not student_id:
            messagebox.showerror("Error", "All fields are required!")
            return

        db_emp = sqlite3.connect("employees.db")
        emp = db_emp.cursor()
        emp.execute("SELECT ID FROM employee WHERE ID = ?", (student_id,))
        if emp.fetchone():
            messagebox.showerror("Error", "ID already exists!")
            db_emp.close()
            return

        # Check if the email already exists
        emp.execute("SELECT EMAIL FROM employee WHERE EMAIL = ?", (email,))
        if emp.fetchone():
            messagebox.showerror("Error", "Email already exists!")
            db_emp.close()
            return
        db_emp.close()

        # Connect to the database and insert the student
        db = sqlite3.connect('student.db')
        cursor = db.cursor()
        # Check if the student ID already exists
        cursor.execute("SELECT ID FROM student WHERE ID = ?", (student_id,))
        if cursor.fetchone():
            messagebox.showerror("Error", "ID already exists!")
            db.close()
            return

        # Check if the email already exists
        cursor.execute("SELECT EMAIL FROM student WHERE EMAIL = ?", (email,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Email already exists!")
            db.close()
            return

        # Insert the new student record into the database
        cursor.execute("INSERT INTO student (NAME, EMAIL, Attendance, EXAMS, ID) VALUES (?, ?, ?, ?, ?)",
                       (name, email, 0, 0, student_id))
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Student added successfully!")
        add_swindow.destroy()
        student_window.deiconify()

    # Create the add student window
    student_window.withdraw()
    add_swindow = ctk.CTkToplevel()
    add_swindow.title("Add Student")
    add_swindow.geometry("800x500")

    ctk.CTkLabel(add_swindow, text="Name").pack(pady=5)
    entry_name = ctk.CTkEntry(add_swindow, width=250,
                              height=30)  # Adjusted size
    entry_name.pack(pady=5)

    ctk.CTkLabel(add_swindow, text="Email").pack(pady=5)
    entry_email = ctk.CTkEntry(
        add_swindow, width=250, height=30)  # Adjusted size
    entry_email.pack(pady=5)

    ctk.CTkLabel(add_swindow, text="ID").pack(pady=5)
    entry_id = ctk.CTkEntry(add_swindow, width=250, height=30)  # Adjusted size
    entry_id.pack(pady=5)

    ctk.CTkButton(add_swindow, text="Save", width=150, fg_color="#007BFF",
                  height=40, command=save_student).pack(pady=20)
    ctk.CTkButton(add_swindow, text="Back", width=150, fg_color="#007BFF", height=40,
                  command=lambda: back_to_main(add_swindow, student_window)).pack(pady=20)


def remove_student(student_window):
    def remove():
        student_id = entry_ID.get().strip()

        if not student_id:
            messagebox.showerror("Error", "ID field is required!")
            return

        # Connect to the database and remove the student
        db = sqlite3.connect('student.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student WHERE ID=?", (student_id,))
        role = cursor.fetchone()
        if role is None:
            messagebox.showerror("Error", "ID not found!")

            db.close()
            return

        # Delete the student record from the database
        cursor.execute("DELETE FROM student WHERE ID=?", (student_id,))
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Student removed successfully!")
        remove_swindow.destroy()
        student_window.deiconify()

# Create the remove student window
    student_window.withdraw()
    remove_swindow = ctk.CTkToplevel()
    remove_swindow.title("Remove Student")
    remove_swindow.geometry("800x500")  # Adjusted height for better spacing

    ctk.CTkLabel(remove_swindow, text="ID").pack(pady=5)
    entry_ID = ctk.CTkEntry(remove_swindow, width=250,
                            height=30)  # Adjusted size
    entry_ID.pack(pady=5)

    ctk.CTkButton(remove_swindow, text="Remove", fg_color="#007BFF",
                  width=150, height=40, command=remove).pack(pady=20)
    ctk.CTkButton(remove_swindow, text="Back", fg_color="#007BFF", width=150, height=40,
                  command=lambda: back_to_main(remove_swindow, student_window)).pack(pady=20)


def search_student(student_window):
    def search_std():
        search = entry_search.get().strip()

        if not search:
            messagebox.showerror("Error", "Search parameter is required!")
            return

        found = False
        db = sqlite3.connect("student.db")
        cursor = db.cursor()

        # Search by EMAIL
        cursor.execute("SELECT * FROM student WHERE EMAIL = ?", (search,))
        data = cursor.fetchall()

        for row in data:
            result = row
            result_text = f"ID: {result[4]}\nName: {
                result[0]}\nEmail: {result[1]}"
            label_result.configure(
                text=result_text, text_color="green")  # Fixed line
            found = True

        # Search by ID
        cursor.execute("SELECT * FROM student WHERE ID = ?", (search,))
        s1 = cursor.fetchall()

        for row in s1:
            result = row
            result_text = f"ID: {result[4]}\nName: {
                result[0]}\nEmail: {result[1]}"
            label_result.configure(
                text=result_text, text_color="green")  # Fixed line
            found = True

        # If no result found, show error
        if not found:
            messagebox.showerror("Error", "Parameter not found")
            return

        db.close()

# Create the search student window
    student_window.withdraw()
    search_swindow = ctk.CTkToplevel()
    search_swindow.title("Search Student")
    search_swindow.geometry("800x500")  # Adjusted height for better spacing

    ctk.CTkLabel(search_swindow, text="ID or EMAIL").pack(pady=10)
    entry_search = ctk.CTkEntry(
        search_swindow, width=250, height=30)  # Adjusted size
    entry_search.pack(pady=5)

    ctk.CTkButton(search_swindow, text="Search", fg_color="#007BFF",
                  width=150, height=40, command=search_std).pack(pady=20)

    label_result = ctk.CTkLabel(
        search_swindow, text="", wraplength=500, justify="left")
    label_result.pack(pady=20)

    ctk.CTkButton(search_swindow, text="Back", fg_color="#007BFF", width=150, height=40,
                  command=lambda: back_to_main(search_swindow, student_window)).pack(pady=20)


# الدالة الرئيسية لعرض نافذة المدرس
def show_teacher_gui():
    root.withdraw()
    teacher_window = ctk.CTkToplevel()
    teacher_window.title("Teacher Panel")
    teacher_window.geometry("800x500")

    ctk.CTkLabel(teacher_window, text="Teacher Dashboard",
                 font=("Arial", 16, "bold")).pack(pady=10)

    buttons = [
        {"text": "Timetable", "fg": "#007BFF",
            "command": lambda: show_timetable(teacher_window)},
        {"text": "My Information", "fg": "#007BFF",
            "command": lambda: show_info(teacher_window)},
        {"text": "Exams", "fg": "#007BFF",
            "command": lambda: manage_exam_degrees(teacher_window)},
        {"text": "Attendance", "fg": "#007BFF",
            "command": lambda: manage_attendance(teacher_window)},
    ]

    for btn in buttons:
        ctk.CTkButton(
            teacher_window,
            text=btn["text"],
            text_color="white",
            fg_color=btn["fg"],    # White text
            font=("Arial", 12),
            width=200,  # Adjusted size for better button display
            height=40,  # Adjusted size for better button display
            command=btn["command"],
        ).pack(pady=5)

    ctk.CTkButton(
        teacher_window,
        text="Logout",
        fg_color="#007BFF",
        text_color="white",  # White text
        font=("Arial", 12),
        width=200,  # Adjusted size for better button display
        height=40,  # Adjusted size for better button display
        command=lambda: logout(teacher_window),
    ).pack(pady=20)


# Teacher GUI
def show_timetable(teacher_window):
    teacher_window.withdraw()
    timetable_window = ctk.CTkToplevel()
    timetable_window.title("Timetable")
    timetable_window.geometry("800x500")

    # Ensure entry_email is defined and contains the email
    email = entry_email.get()  # Make sure entry_email is accessible here

    # Establish database connection
    d = sqlite3.connect('timetable.db')
    x1 = d.cursor()
    x1.execute("SELECT * FROM tae WHERE email = ?", (email,))
    data = x1.fetchall()

    # Check if data is found for the given email
    if not data:
        messagebox.showerror("Error", "No timetable found for this email")
        d.close()
        return

    # Create label for timetable title
    label = ctk.CTkLabel(
        timetable_window, text="Today's Timetable", font=("Arial", 20, "bold"))
    label.pack(pady=20)

    # Define the timetable based on the fetched data
    timetable = {
        # Assuming each entry in 'data' corresponds to a specific time slot
        "9 to 10.50": data[0][0],
        "11 to 12.50": data[0][1],
        "1 to 2.50": data[0][2],
        "3 to 4.50": data[0][3],
    }

    # Display each time slot in the timetable
    for key, value in timetable.items():
        ctk.CTkLabel(timetable_window, text=f"{key}: {
                     value}", font=("Arial", 14)).pack(pady=5)

    # Create Back button
    ctk.CTkButton(
        timetable_window,
        text="Back",
        fg_color="#007BFF",
        text_color="white",
        font=("Arial", 12),
        width=150,
        height=20,
        command=lambda: back_to_main(timetable_window, teacher_window),
    ).pack(pady=20)

    # Close the database connection
    d.close()


# دالة لعرض المعلومات الشخصية
def show_info(teacher_window):
    teacher_window.withdraw()
    info_window = ctk.CTkToplevel()
    info_window.title("My Information")
    info_window.geometry("800x500")

    # Ensure entry_email is defined and contains the correct email value
    email = entry_email.get()  # Make sure entry_email is accessible here

    # Establish database connection
    db = sqlite3.connect('employees.db')
    x = db.cursor()
    x.execute("SELECT * FROM employee WHERE email = ?", (email,))
    data = x.fetchall()

    # Check if data is found for the given email
    if not data:
        messagebox.showerror("Error", "No information found for this email")
        db.close()
        return

    # Create label for teacher information title
    label = ctk.CTkLabel(info_window, text="Information",
                         font=("Arial", 20, "bold"))
    label.pack(pady=20)

    # Define the teacher's info
    info = {
        "Name": data[0][0],  # Assuming Name is in the first column
        "ID": data[0][4],    # Assuming ID is in the 5th column
        "Email": data[0][1],  # Assuming Email is in the second column
    }

    # Display each piece of teacher information
    for key, value in info.items():
        ctk.CTkLabel(info_window, text=f"{key}: {
                     value}", font=("Arial", 14)).pack(pady=5)

    # Create Back button
    ctk.CTkButton(
        info_window,
        text="Back",
        fg_color="#007BFF",
        text_color="white",
        font=("Arial", 12),
        width=150,
        height=20,
        command=lambda: back_to_main(info_window, teacher_window),
    ).pack(pady=20)

    # Close the database connection
    db.close()


# دالة لإدارة الامتحانات
def manage_exam_degrees(teacher_window):
    teacher_window.withdraw()
    exam_window = ctk.CTkToplevel()
    exam_window.title("Manage Exam Degrees")
    exam_window.geometry("800x500")

    def fetch_students_grades():
        """Fetch student names, IDs, and current exam degrees from the database."""
        db = sqlite3.connect("student.db")
        cursor = db.cursor()
        cursor.execute("SELECT ID, NAME, EXAMS FROM student")
        students = cursor.fetchall()
        db.close()
        return students

    def save_grades():
        """Save updated grades to the database."""
        db = sqlite3.connect("student.db")
        cursor = db.cursor()
        for student_id, var in grades_vars.items():
            new_grade = var.get()
            if not new_grade.replace('.', '', 1).isdigit() or not (0 <= float(new_grade) <= 100):
                messagebox.showerror("Error", f"Invalid grade for Student ID: {
                                     student_id}. Must be 0-100.")
                db.close()
                return

            # Fetch the current grade
            cursor.execute(
                "SELECT EXAMS FROM student WHERE ID = ?", (student_id,))
            current_grade = cursor.fetchone()[0] or 0

            # Add new grade to old
            updated_grade = float(current_grade) + float(new_grade)

            if updated_grade > 100:  # Ensure grades do not exceed 100
                messagebox.showerror("Error", f"Total grade for Student ID: {
                                     student_id} exceeds 100.")
                db.close()
                return

            cursor.execute(
                "UPDATE student SET EXAMS = ? WHERE ID = ?", (updated_grade, student_id))

        db.commit()
        db.close()
        messagebox.showinfo("Success", "Exam grades updated successfully!")
        exam_window.destroy()
        teacher_window.deiconify()

    # Scrollable Frame
    scrollable_frame = ctk.CTkFrame(
        exam_window, fg_color="#3b3b3b", corner_radius=15)
    scrollable_frame.pack(fill="both", expand=True, pady=10, padx=10)

    # Add a canvas for the scrollable area
    canvas = ctk.CTkCanvas(
        scrollable_frame, bg="#3b3b3b", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar
    scrollbar = ctk.CTkScrollbar(
        scrollable_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    table_frame = ctk.CTkFrame(canvas, fg_color="#3b3b3b")
    table_window = canvas.create_window(
        (0, 0), window=table_frame, anchor="nw")

    def on_canvas_configure(event):
        """Update the scroll region when the canvas size changes."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    table_frame.bind("<Configure>", on_canvas_configure)

    # Create a table header
    headers = ["ID", "Name", "Add Grade"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            table_frame, text=header, font=("Arial", 14, "bold"), text_color="white"
        )
        header_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

    # Fetch student data and populate the table
    students = fetch_students_grades()
    grades_vars = {}

    for row, (student_id, name, exam_grade) in enumerate(students, start=1):
        # Student ID
        ctk.CTkLabel(table_frame, text=str(student_id), font=("Arial", 12), text_color="white").grid(
            row=row, column=0, padx=10, pady=5, sticky="w"
        )

        # Student Name
        ctk.CTkLabel(table_frame, text=name, font=("Arial", 12), text_color="white").grid(
            row=row, column=1, padx=10, pady=5, sticky="w"
        )

        # Editable Exam Grade (new grade to add to existing)
        var = ctk.StringVar(value="0")  # Default to 0 for adding new grades
        grades_vars[student_id] = var
        grade_entry = ctk.CTkEntry(
            table_frame, textvariable=var, font=("Arial", 12), width=100, justify="center"
        )
        grade_entry.grid(row=row, column=2, padx=10, pady=5)

    # Add Save and Back buttons
    button_frame = ctk.CTkFrame(
        exam_window, fg_color="#2b2b2b", corner_radius=15)
    button_frame.pack(fill="x", pady=10)

    ctk.CTkButton(
        button_frame,
        text="Save",
        fg_color="#007BFF",
        text_color="white",
        font=("Arial", 12),
        command=save_grades,
    ).pack(side="right", padx=10, pady=5)

    ctk.CTkButton(
        button_frame,
        text="Back",
        fg_color="#007BFF",
        text_color="white",
        font=("Arial", 12),
        command=lambda: back_to_main(exam_window, teacher_window),
    ).pack(side="left", padx=10, pady=5)


# دالة لإدارة الحضور
def manage_attendance(teacher_window):
    # Withdraw the teacher window when attendance window opens
    teacher_window.withdraw()

    # Create the attendance window
    attendance_window = ctk.CTkToplevel()
    attendance_window.title("Manage Attendance")
    attendance_window.geometry("800x500")  # Adjust the window size

    # Function to fetch students and attendance data from the database
    def fetch_students_attendance():
        """Fetch student names, IDs, and current attendance from the database."""
        db = sqlite3.connect("student.db")
        cursor = db.cursor()
        cursor.execute("SELECT ID, NAME, ATTENDANCE FROM student")
        students = cursor.fetchall()
        db.close()
        return students

    # Function to update attendance in the database (will be called after saving)
    def update_attendance(student_id, present):
        """Update attendance in the database when a checkbox is toggled."""
        db = sqlite3.connect("student.db")
        cursor = db.cursor()
        if present:
            cursor.execute(
                "UPDATE student SET ATTENDANCE = ATTENDANCE + 1 WHERE ID = ?", (student_id,))
        db.commit()
        db.close()

    # Create a scrollable canvas and frame
    canvas = ctk.CTkCanvas(attendance_window, width=700, height=500,
                           bg="#212121", highlightthickness=0)  # Set dark background
    scrollbar = ctk.CTkScrollbar(
        attendance_window, orientation="vertical", command=canvas.yview)
    # Set frame background to match
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="#212121")

    # Configure the canvas and scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Fetch student data
    students = fetch_students_attendance()
    attendance_vars = {}

    # Create table headers
    headers = ["ID", "Name", "Present"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            scrollable_frame, text=header, font=("Arial", 18, "bold"), text_color="white"
        )
        header_label.grid(row=0, column=col, padx=20, pady=15, sticky="w")

    # Populate rows with student data
    for row, (student_id, name, attendance) in enumerate(students, start=1):
        # Student ID
        ctk.CTkLabel(scrollable_frame, text=str(student_id), font=("Arial", 16), text_color="white").grid(
            row=row, column=0, padx=20, pady=15, sticky="w"
        )

        # Student Name
        ctk.CTkLabel(scrollable_frame, text=name, font=("Arial", 16), text_color="white").grid(
            row=row, column=1, padx=20, pady=15, sticky="w"
        )

        # Checkbox for attendance
        var = ctk.IntVar(value=0)  # Default to unchecked
        attendance_vars[student_id] = var

        ctk.CTkCheckBox(
            scrollable_frame,
            text="",
            variable=var,
            onvalue=1,
            offvalue=0,
        ).grid(row=row, column=2, padx=20, pady=15)

    # Save Button
    def save_changes():
        """Save the attendance changes to the database."""
        for student_id, var in attendance_vars.items():
            update_attendance(student_id, var.get() == 1)

        # Close attendance window and show the teacher window
        attendance_window.withdraw()
        teacher_window.deiconify()

    save_button = ctk.CTkButton(
        attendance_window,
        text="Save",
        fg_color="#28a745",
        text_color="white",
        font=("Arial", 16),
        command=save_changes,
    )
    save_button.grid(row=1, column=0, pady=20, sticky="w", padx=20)

    # Back Button
    def back_to_main():
        """Return to the teacher's main window."""
        attendance_window.withdraw()
        teacher_window.deiconify()

    back_button = ctk.CTkButton(
        attendance_window,
        text="Back",
        fg_color="#007BFF",
        text_color="white",
        font=("Arial", 16),
        command=back_to_main,
    )
    back_button.grid(row=1, column=1, pady=20, sticky="e", padx=20)

    # Update scroll region to fit content
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def show_employee_gui():
    root.withdraw()  # Hide the main window
    staff_window = ctk.CTkToplevel()  # Create a new top-level window
    staff_window.title("Staff Panel")  # Set window title
    staff_window.geometry("800x500")  # Adjusted window size for better UI

    # Title Label for Staff Dashboard
    ctk.CTkLabel(staff_window, text="Staff Dashboard", font=(
        # Blue text color
        "Arial", 16, "bold"), text_color="white").pack(pady=20)

    # Buttons configuration
    buttons = [
        {"text": "My Information", "command": lambda: show_info(staff_window)},
    ]

    # Create and pack buttons with blue color for bg_color and fg_color
    for btn in buttons:
        ctk.CTkButton(
            staff_window,
            text=btn["text"],
            text_color="white",
            fg_color="#007BFF",  # Blue color for the text
            font=("Arial", 12),
            width=250,  # Increased width for better display
            height=40,  # Increased height for better display
            command=btn["command"],
        ).pack(pady=10)

    # Logout button with blue color and updated size
    ctk.CTkButton(
        staff_window,
        text="Logout",
        text_color="white",
        fg_color="#007BFF",
        font=("Arial", 12),
        width=250,  # Adjusted width
        height=40,  # Adjusted height
        command=lambda: logout(staff_window),
    ).pack(pady=20)


def add_timetable(email_teacher, id_teacher, employee_window):
    def save_timetable():
        sec1 = entry_1.get()
        sec2 = entry_2.get()
        sec3 = entry_3.get()
        sec4 = entry_4.get()

        if not sec1 or not sec2 or not sec3 or not sec4:
            messagebox.showerror("Error", "All fields are required!")
            return

        db_timetable = sqlite3.connect("timetable.db")
        time_table = db_timetable.cursor()
        # Insert the new student record into the database
        time_table.execute("INSERT INTO tae  VALUES (?, ?, ?, ?,?, ?)",
                           (sec1, sec2, sec3, sec4, email_teacher, id_teacher))
        db_timetable.commit()
        db_timetable.close()

        messagebox.showinfo("Success", "TimeTable added successfully!")
        timetable_window.destroy()
        employee_window.deiconify()

    # Create the add timetable window
    employee_window.withdraw()
    timetable_window = ctk.CTkToplevel()
    timetable_window.title("Add TimeTable")
    timetable_window.geometry("800x500")

    ctk.CTkLabel(timetable_window, text="9:10.50").pack(pady=5)
    entry_1 = ctk.CTkEntry(timetable_window, width=250,
                           height=30)  # Adjusted size
    entry_1.pack(pady=5)

    ctk.CTkLabel(timetable_window, text="11:12.50").pack(pady=5)
    entry_2 = ctk.CTkEntry(timetable_window, width=250,
                           height=30)  # Adjusted size
    entry_2.pack(pady=5)

    ctk.CTkLabel(timetable_window, text="1:2.50").pack(pady=5)
    entry_3 = ctk.CTkEntry(timetable_window, width=250,
                           height=30)  # Adjusted size
    entry_3.pack(pady=5)

    ctk.CTkLabel(timetable_window, text="3:4.50").pack(pady=5)
    entry_4 = ctk.CTkEntry(timetable_window, width=250,
                           height=30)  # Adjusted size
    entry_4.pack(pady=5)

    ctk.CTkButton(timetable_window, text="Save", width=150,
                  height=40, command=save_timetable).pack(pady=20)

# Back to main window


def back_to_main(current_window, main_window):
    current_window.destroy()
    main_window.deiconify()

# Logout function


def logout(window):
    window.destroy()
    root.deiconify()


# main gui
root = ctk.CTk()
root.title("Login Page")
root.geometry("800x500")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ctk.CTkLabel(root, text="Login", font=("Arial", 16)).pack(pady=10)

ctk.CTkLabel(root, text="Email:").pack(pady=5)
entry_email = ctk.CTkEntry(root, width=200)
entry_email.pack()

ctk.CTkLabel(root, text="Password:").pack(pady=5)
entry_password = ctk.CTkEntry(root, show="*", width=200)
entry_password.pack()

ctk.CTkButton(
    root, text="Login", font=("Arial", 12), text_color="white",
    fg_color="#007BFF", width=150, height=35, command=login
).pack(pady=20)

root.mainloop()
