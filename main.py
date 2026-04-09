import tkinter as tk
from ui.LoginForm import LoginForm


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()