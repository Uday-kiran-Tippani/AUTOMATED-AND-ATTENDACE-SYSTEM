import tkinter as tk
from gui.admin_pannel import AdminPanel 


def main():
    root = tk.Tk()
    root.title("Admin Software")
    root.geometry("1000x600")  # Adjust screen size
    app = AdminPanel(root)
    root.mainloop()

if __name__ == "__main__":
    main()
