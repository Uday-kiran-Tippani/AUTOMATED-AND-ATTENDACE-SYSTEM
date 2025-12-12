# import tkinter as tk
# from tkinter import filedialog, ttk, messagebox
# from PIL import Image, ImageTk
# from database.firebase_connection import get_classes, add_student, get_students
# from gui.widgets import ScrollableFrame
# from face_recognition_utils import encode_image
# import numpy as np

# class AddStudentsWindow:
#     def __init__(self, master, classes=None):
#         self.window = tk.Toplevel(master)
#         self.window.title("Add Students")
#         self.window.geometry("1100x650")
#         self.students_rows = []

#         # Classes fetched from parameter or database
#         self.classes = classes if classes else get_classes()

#         # Class selection
#         tk.Label(self.window, text="Select Class:").pack(pady=5)
#         self.class_dropdown = ttk.Combobox(
#             self.window, values=list(self.classes.keys()), state="readonly"
#         )
#         self.class_dropdown.pack(pady=5)
#         if self.classes:
#             self.class_dropdown.current(0)

#         # Number of students
#         num_frame = tk.Frame(self.window)
#         num_frame.pack(pady=5)
#         tk.Label(num_frame, text="Number of Students:").pack(side='left', padx=5)
#         self.num_students_entry = tk.Entry(num_frame, width=5)
#         self.num_students_entry.pack(side='left', padx=5)

#         # Auto-increment checkbox
#         self.auto_increment = tk.BooleanVar()
#         tk.Checkbutton(
#             num_frame,
#             text="Auto Increment Roll Numbers",
#             variable=self.auto_increment,
#             command=self.toggle_start_number
#         ).pack(side='left', padx=10)
#         self.start_roll_entry = tk.Entry(num_frame, width=15)
#         self.start_roll_entry.pack(side='left', padx=5)
#         self.start_roll_entry.insert(0, "24886510001")
#         self.start_roll_entry.config(state='disabled')

#         tk.Button(num_frame, text="OK", command=self.create_rows).pack(side='left', padx=10)

#         # Column headers
#         header_frame = tk.Frame(self.window)
#         header_frame.pack(pady=5, fill='x')
#         tk.Label(header_frame, text="Roll Number", width=20, anchor='w').pack(side='left', padx=5)
#         tk.Label(header_frame, text="Full Name", width=30, anchor='w').pack(side='left', padx=5)
#         tk.Label(header_frame, text="Upload Image", width=15, anchor='w').pack(side='left', padx=5)
#         tk.Label(header_frame, text="Remove", width=10, anchor='w').pack(side='left', padx=5)
#         tk.Label(header_frame, text="Preview", width=15, anchor='w').pack(side='left', padx=5)

#         # Scrollable frame
#         self.scroll_frame = ScrollableFrame(self.window, width=1000, height=400)
#         self.scroll_frame.pack(pady=10, fill='both', expand=True)

#         # Buttons
#         btn_frame = tk.Frame(self.window)
#         btn_frame.pack(pady=10)
#         tk.Button(btn_frame, text="Add More Row", command=self.add_student_row).pack(side='left', padx=10)
#         tk.Button(btn_frame, text="Add Students", command=self.save_students).pack(side='left', padx=10)

#     def toggle_start_number(self):
#         if self.auto_increment.get():
#             self.start_roll_entry.config(state='normal')
#             self.start_roll_entry.delete(0, 'end')
#             self.start_roll_entry.insert(0, "24886510001")
#         else:
#             self.start_roll_entry.config(state='disabled')

#     def create_rows(self):
#         try:
#             n = int(self.num_students_entry.get())
#             if n <= 0:
#                 raise ValueError
#         except:
#             return  # Ignore silently

#         # Clear previous rows
#         for widget in self.scroll_frame.scrollable_frame.winfo_children():
#             widget.destroy()
#         self.students_rows = []

#         start_roll = int(self.start_roll_entry.get()) if self.auto_increment.get() else None
#         for i in range(n):
#             self.add_student_row(auto_roll=start_roll+i if start_roll else None)

#     def add_student_row(self, auto_roll=None):
#         row_frame = tk.Frame(self.scroll_frame.scrollable_frame)
#         row_frame.pack(pady=3, fill='x')

#         # Roll number
#         roll_entry = tk.Entry(row_frame, width=20)
#         roll_entry.pack(side='left', padx=5)
#         if auto_roll:
#             roll_entry.insert(0, str(auto_roll))

#         # Name
#         name_entry = tk.Entry(row_frame, width=30)
#         name_entry.pack(side='left', padx=5)

#         # Image upload
#         image_path = tk.StringVar()
#         preview_label = tk.Label(row_frame)
#         preview_label.pack(side='right', padx=5)

#         def upload_image():
#             path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
#             if path:
#                 image_path.set(path)
#                 img = Image.open(path)
#                 img.thumbnail((50, 50))
#                 img = ImageTk.PhotoImage(img)
#                 preview_label.image = img
#                 preview_label.config(image=img)

#         tk.Button(row_frame, text="Upload Image", command=upload_image).pack(side='left', padx=5)

#         # Remove row
#         def remove_row():
#             row_frame.destroy()
#             self.students_rows.remove(row_data)

#         tk.Button(row_frame, text="❌", command=remove_row).pack(side='left', padx=5)

#         # Error label
#         error_label = tk.Label(row_frame, text="", fg="red")
#         error_label.pack(side='left', padx=10)

#         row_data = {
#             'roll': roll_entry,
#             'name': name_entry,
#             'image_path': image_path,
#             'preview_label': preview_label,
#             'error_label': error_label
#         }
#         self.students_rows.append(row_data)

#     def save_students(self):
#         selected_class = self.class_dropdown.get()
#         if not selected_class or not self.students_rows:
#             return

#         # Clear errors
#         for row in self.students_rows:
#             row['error_label'].config(text="")

#         valid_rows = []
#         has_error = False

#         existing_students = get_students(selected_class)
#         seen_rolls, seen_names, seen_images = set(), set(), set()

#         # Validation phase (no insert yet!)
#         for row in self.students_rows:
#             roll = row['roll'].get().strip()
#             name = row['name'].get().strip()
#             img_path = row['image_path'].get()

#             if not roll and not name and not img_path:
#                 continue

#             if not roll or not name or not img_path:
#                 row['error_label'].config(text="All fields required")
#                 has_error = True
#                 continue

#             if len(name.split()) < 2:
#                 row['error_label'].config(text="Enter full name (min 2 words)")
#                 has_error = True
#                 continue

#             norm_name = name.lower().replace(" ", "")

#             if roll in seen_rolls:
#                 row['error_label'].config(text="Duplicate roll in form")
#                 has_error = True
#                 continue
#             seen_rolls.add(roll)

#             if norm_name in seen_names:
#                 row['error_label'].config(text="Duplicate name in form")
#                 has_error = True
#                 continue
#             seen_names.add(norm_name)

#             if img_path in seen_images:
#                 row['error_label'].config(text="Duplicate image in form")
#                 has_error = True
#                 continue
#             seen_images.add(img_path)

#             if roll in existing_students:
#                 row['error_label'].config(text="Roll already exists")
#                 has_error = True
#                 continue

#             for stu in existing_students.values():
#                 existing_name = stu['name'].strip().lower().replace(" ", "")
#                 if existing_name == norm_name:
#                     row['error_label'].config(text="Name already exists")
#                     has_error = True
#                     break
#             else:
#                 encoded = encode_image(img_path)
#                 if not encoded:
#                     row['error_label'].config(text="Face not detected")
#                     has_error = True
#                     continue

#                 for stu in existing_students.values():
#                     try:
#                         existing_encoding = np.array(stu['face_encoding'])
#                         dist = np.linalg.norm(existing_encoding - np.array(encoded))
#                         if dist < 0.45:
#                             row['error_label'].config(
#                                 text=f"Face already exists ({stu['roll_number']})"
#                             )
#                             has_error = True
#                             break
#                     except Exception:
#                         continue

#             if not row['error_label'].cget("text"):
#                 valid_rows.append((roll, name, encoded))

#         # If any error → do NOT save anything
#         if has_error or not valid_rows:
#             return

#         # Save all students at once
#         try:
#             for roll, name, encoded in valid_rows:
#                 student_data = {'roll_number': roll, 'name': name, 'face_encoding': encoded}
#                 add_student(selected_class, student_data)

#             messagebox.showinfo("Success", "All students added successfully!")
#             self.num_students_entry.delete(0, tk.END)
#             for row in self.students_rows:
#                 row['roll'].delete(0, tk.END)
#                 row['name'].delete(0, tk.END)
#                 row['image_path'].set("")
#                 row['preview_label'].config(image="")
#                 row['error_label'].config(text="")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to add students: {e}")


#for globally cheking for duplicates
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from database.firebase_connection import get_classes, add_student, get_students
from gui.widgets import ScrollableFrame
from face_recognition_utils import encode_image
import numpy as np

class AddStudentsWindow:
    def __init__(self, master, classes=None):
        self.window = tk.Toplevel(master)
        self.window.title("Add Students")
        self.window.geometry("1100x650")
        self.students_rows = []

        # Classes fetched from parameter or database
        self.classes = classes if classes else get_classes()

        # Class selection
        tk.Label(self.window, text="Select Class:").pack(pady=5)
        self.class_dropdown = ttk.Combobox(
            self.window, values=list(self.classes.keys()), state="readonly"
        )
        self.class_dropdown.pack(pady=5)
        if self.classes:
            self.class_dropdown.current(0)

        # Number of students
        num_frame = tk.Frame(self.window)
        num_frame.pack(pady=5)
        tk.Label(num_frame, text="Number of Students:").pack(side='left', padx=5)
        self.num_students_entry = tk.Entry(num_frame, width=5)
        self.num_students_entry.pack(side='left', padx=5)

        # Auto-increment checkbox
        self.auto_increment = tk.BooleanVar()
        tk.Checkbutton(
            num_frame,
            text="Auto Increment Roll Numbers",
            variable=self.auto_increment,
            command=self.toggle_start_number
        ).pack(side='left', padx=10)
        self.start_roll_entry = tk.Entry(num_frame, width=15)
        self.start_roll_entry.pack(side='left', padx=5)
        self.start_roll_entry.insert(0, "24886510001")
        self.start_roll_entry.config(state='disabled')

        tk.Button(num_frame, text="OK", command=self.create_rows).pack(side='left', padx=10)

        # Column headers
        header_frame = tk.Frame(self.window)
        header_frame.pack(pady=5, fill='x')
        tk.Label(header_frame, text="Roll Number", width=20, anchor='w').pack(side='left', padx=5)
        tk.Label(header_frame, text="Full Name", width=30, anchor='w').pack(side='left', padx=5)
        tk.Label(header_frame, text="Upload Image", width=15, anchor='w').pack(side='left', padx=5)
        tk.Label(header_frame, text="Remove", width=10, anchor='w').pack(side='left', padx=5)
        tk.Label(header_frame, text="Preview", width=15, anchor='w').pack(side='left', padx=5)

        # Scrollable frame
        self.scroll_frame = ScrollableFrame(self.window, width=1000, height=400)
        self.scroll_frame.pack(pady=10, fill='both', expand=True)

        # Buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Add More Row", command=self.add_student_row).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Add Students", command=self.save_students).pack(side='left', padx=10)

    def toggle_start_number(self):
        if self.auto_increment.get():
            self.start_roll_entry.config(state='normal')
            self.start_roll_entry.delete(0, 'end')
            self.start_roll_entry.insert(0, "24886510001")
        else:
            self.start_roll_entry.config(state='disabled')

    def create_rows(self):
        try:
            n = int(self.num_students_entry.get())
            if n <= 0:
                raise ValueError
        except:
            return  # Ignore silently

        # Clear previous rows
        for widget in self.scroll_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.students_rows = []

        start_roll = int(self.start_roll_entry.get()) if self.auto_increment.get() else None
        for i in range(n):
            self.add_student_row(auto_roll=start_roll+i if start_roll else None)

    def add_student_row(self, auto_roll=None):
        row_frame = tk.Frame(self.scroll_frame.scrollable_frame)
        row_frame.pack(pady=3, fill='x')

        # Roll number
        roll_entry = tk.Entry(row_frame, width=20)
        roll_entry.pack(side='left', padx=5)
        if auto_roll:
            roll_entry.insert(0, str(auto_roll))

        # Name
        name_entry = tk.Entry(row_frame, width=30)
        name_entry.pack(side='left', padx=5)

        # Image upload
        image_path = tk.StringVar()
        preview_label = tk.Label(row_frame)
        preview_label.pack(side='right', padx=5)

        def upload_image():
            path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
            if path:
                image_path.set(path)
                img = Image.open(path)
                img.thumbnail((50, 50))
                img = ImageTk.PhotoImage(img)
                preview_label.image = img
                preview_label.config(image=img)

        tk.Button(row_frame, text="Upload Image", command=upload_image).pack(side='left', padx=5)

        # Remove row
        def remove_row():
            row_frame.destroy()
            self.students_rows.remove(row_data)

        tk.Button(row_frame, text="❌", command=remove_row).pack(side='left', padx=5)

        # Error label
        error_label = tk.Label(row_frame, text="", fg="red")
        error_label.pack(side='left', padx=10)

        row_data = {
            'roll': roll_entry,
            'name': name_entry,
            'image_path': image_path,
            'preview_label': preview_label,
            'error_label': error_label
        }
        self.students_rows.append(row_data)

    def save_students(self):
        selected_class = self.class_dropdown.get()
        if not selected_class or not self.students_rows:
            return

        # Clear errors
        for row in self.students_rows:
            row['error_label'].config(text="")

        valid_rows = []
        has_error = False

        # ----------------------------
        # Fetch all students across all classes for global uniqueness
        all_students_global = {}
        for class_key in get_classes().values():
            class_students = get_students(class_key)
            for roll, data in class_students.items():
                all_students_global[(roll, data['name'].strip().lower())] = np.array(data['face_encoding'])
        # ----------------------------

        seen_rolls, seen_names, seen_images = set(), set(), set()

        # Validation phase
        for row in self.students_rows:
            roll = row['roll'].get().strip()
            name = row['name'].get().strip()
            img_path = row['image_path'].get()

            if not roll and not name and not img_path:
                continue

            if not roll or not name or not img_path:
                row['error_label'].config(text="All fields required")
                has_error = True
                continue

            if len(name.split()) < 2:
                row['error_label'].config(text="Enter full name (min 2 words)")
                has_error = True
                continue

            norm_name = name.lower().replace(" ", "")

            # Check duplicates in current form
            if roll in seen_rolls:
                row['error_label'].config(text="Duplicate roll in form")
                has_error = True
                continue
            seen_rolls.add(roll)

            if norm_name in seen_names:
                row['error_label'].config(text="Duplicate name in form")
                has_error = True
                continue
            seen_names.add(norm_name)

            if img_path in seen_images:
                row['error_label'].config(text="Duplicate image in form")
                has_error = True
                continue
            seen_images.add(img_path)

            # Global duplicates check
            for existing_roll, existing_name in all_students_global.keys():
                if roll == existing_roll:
                    row['error_label'].config(text="Roll already exists in another class")
                    has_error = True
                    break
                if norm_name == existing_name.replace(" ", ""):
                    row['error_label'].config(text="Name already exists in another class")
                    has_error = True
                    break
            if has_error:
                continue

            encoded = encode_image(img_path)
            if not encoded:
                row['error_label'].config(text="Face not detected")
                has_error = True
                continue

            # Check for duplicate face globally
            for existing_encoding in all_students_global.values():
                if np.linalg.norm(encoded - existing_encoding) < 0.45:
                    row['error_label'].config(text="Face already exists in another class")
                    has_error = True
                    break
            if has_error:
                continue

            valid_rows.append((roll, name, encoded))

        # If any error → do NOT save anything
        if has_error or not valid_rows:
            return

        # Save all students at once
        try:
            for roll, name, encoded in valid_rows:
                student_data = {'roll_number': roll, 'name': name, 'face_encoding': encoded}
                add_student(selected_class, student_data)

            messagebox.showinfo("Success", "All students added successfully!")

            # Clear form
            self.num_students_entry.delete(0, tk.END)
            for row in self.students_rows:
                row['roll'].delete(0, tk.END)
                row['name'].delete(0, tk.END)
                row['image_path'].set("")
                row['preview_label'].config(image="")
                row['error_label'].config(text="")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add students: {e}")
