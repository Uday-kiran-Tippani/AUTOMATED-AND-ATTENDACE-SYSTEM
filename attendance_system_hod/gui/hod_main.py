# hod_main.py
import tkinter as tk
from tkinter import messagebox
from register_lecturer import RegisterLecturer
from update_lecturer import UpdateLecturer

class HODMainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HOD / Principal Dashboard")
        self.root.geometry("400x250")

        # Label
        tk.Label(root, text="Welcome HOD / Principal", font=("Arial", 16)).pack(pady=20)

        # Buttons
        tk.Button(root, text="Register New Lecturer", font=("Arial", 12), width=25, command=self.open_register).pack(pady=10)
        tk.Button(root, text="Update / Remove Lecturer", font=("Arial", 12), width=25, command=self.open_update).pack(pady=10)

    def open_register(self):
        # Open the Register Lecturer Interface
        register_window = tk.Toplevel(self.root)
        RegisterLecturer(register_window)

    def open_update(self):
        # Open the Update / Remove Lecturer Interface
        update_window = tk.Toplevel(self.root)
        UpdateLecturer(update_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = HODMainApp(root)
    root.mainloop()
