import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database.firebase_connection import get_classes, add_class, delete_class as delete_class_from_db
from gui.add_students import AddStudentsWindow

# -------------------------------
# Sanitize Firebase Key
# -------------------------------
def sanitize_key(name):
    """
    Replace Firebase-invalid characters and normalize to lowercase.
    """
    invalid_chars = ['.', '#', '$', '[', ']']
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip().lower()  # lowercase + strip whitespace


# -------------------------------
# Admin Panel Class
# -------------------------------
class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(pady=50)

        tk.Label(self.frame, text="Admin Panel", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.frame, text="Add Class", width=20, command=self.add_class).pack(pady=10)
        tk.Button(self.frame, text="Delete Class", width=20, command=self.delete_class).pack(pady=10)
        tk.Button(self.frame, text="Add Students", width=20, command=self.add_students).pack(pady=10)

    # -------------------------------
    # Add Class
    # -------------------------------
    def add_class(self):
        class_name = simpledialog.askstring("Add Class", "Enter Class Name:")
        if not class_name:
            return

        try:
            key_name = sanitize_key(class_name)
            existing_classes = get_classes()  # returns {display_name: key}

            # Prevent duplicates (case-insensitive)
            if key_name in [sanitize_key(k) for k in existing_classes.keys()]:
                messagebox.showerror("Error", f"Class '{class_name}' already exists!")
                return

            # ✅ Only pass class_name, since firebase_connection.add_class expects 1 arg
            add_class(class_name)

            messagebox.showinfo("Success", f"Class '{class_name}' added successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add class: {str(e)}")

    # -------------------------------
    # Delete Class
    # -------------------------------
    def delete_class(self):
        try:
            classes = get_classes()  # {display_name: key}
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch classes: {str(e)}")
            return

        if not classes:
            messagebox.showwarning("Warning", "No classes found!")
            return

        # Create a selection dialog
        delete_win = tk.Toplevel(self.root)
        delete_win.title("Delete Class")
        tk.Label(delete_win, text="Select Class to Delete:").pack(pady=5)

        selected_class = tk.StringVar()
        class_dropdown = ttk.Combobox(
            delete_win, values=list(classes.keys()),
            textvariable=selected_class, state="readonly"
        )
        class_dropdown.pack(pady=5)
        class_dropdown.current(0)

        def confirm_delete():
            class_display_name = selected_class.get()
            key_name = classes[class_display_name]  # ✅ Firebase key from get_classes
            confirm = messagebox.askyesno(
                "Confirm", f"Are you sure you want to delete '{class_display_name}'?"
            )
            if confirm:
                delete_class_from_db(key_name)  # ✅ Now passes the correct key
                messagebox.showinfo("Success", f"Class '{class_display_name}' deleted successfully!")
                delete_win.destroy()

        tk.Button(delete_win, text="Delete", command=confirm_delete).pack(pady=10)

    # -------------------------------
    # Add Students
    # -------------------------------
    def add_students(self):
        try:
            classes = get_classes()
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch classes: {str(e)}")
            return

        AddStudentsWindow(self.root, classes=classes)  # pass classes to AddStudentsWindow

    # -------------------------------
    # Validate Student Rows (Optional)
    # -------------------------------
    def validate_student_rows(self):
        """
        Validate all student rows before adding them to Firebase.
        Errors are displayed inline under each row instead of popups.
        """
        is_valid = True

        for row_data in getattr(self, "students_rows", []):
            roll = row_data['roll'].get().strip()
            name = row_data['name'].get().strip()
            image_path = row_data['image_path'].get().strip()

            # Reset error text first
            row_data['error_label'].config(text="")

            # Roll validation
            if not roll.isdigit():
                row_data['error_label'].config(text="Roll number must be numeric")
                is_valid = False
                continue

            # Name validation (must contain at least 2 words)
            if len(name.split()) < 2:
                row_data['error_label'].config(text="Enter full name (min 2 words)")
                is_valid = False
                continue

            # Image validation
            if not image_path:
                row_data['error_label'].config(text="Image required")
                is_valid = False
                continue

        return is_valid
