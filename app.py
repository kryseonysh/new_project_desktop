#app.py
import tkinter as tk
from gui import UserManagementGUI

def main():
    root = tk.Tk()
    app = UserManagementGUI(root, None)
    root.mainloop()

if __name__ == "__main__":
    main()