import tkinter as tk
from tkinter import messagebox

ADMIN_PASSWORD = "dhruv123"

def check_login():
    entered = password_entry.get()
    if entered == ADMIN_PASSWORD:
        root.destroy()
        import main 
    else:
        messagebox.showerror("Error", "Incorrect Password!")

# ------------------ GUI ------------------
root = tk.Tk()
root.title("🔐 Voice File Manager - Login")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#1e1e2f")  # Dark background

# ------------ Styling ------------
title_font = ("Segoe UI", 16, "bold")
label_font = ("Segoe UI", 12)
entry_bg = "#2d2d44"
entry_fg = "#ffffff"
btn_bg = "#4e88ff"
btn_fg = "#ffffff"
hover_bg = "#366ed8"

# ------------ Title ------------
title_label = tk.Label(root, text="🔒 Admin Login", bg="#1e1e2f", fg="white", font=title_font)
title_label.pack(pady=20)

# ------------ Password Entry ------------
password_entry = tk.Entry(root, show="*", font=label_font, bg=entry_bg, fg=entry_fg, insertbackground="white", width=25, relief="flat")
password_entry.pack(pady=10)

# ------------ Login Button ------------
def on_enter(e):
    login_btn.config(bg=hover_bg)

def on_leave(e):
    login_btn.config(bg=btn_bg)

login_btn = tk.Button(root, text="Login", font=label_font, bg=btn_bg, fg=btn_fg, activebackground=hover_bg,
                      width=15, height=1, bd=0, command=check_login, cursor="hand2")
login_btn.pack(pady=20)

login_btn.bind("<Enter>", on_enter)
login_btn.bind("<Leave>", on_leave)

# ------------ Run ------------
root.mainloop()
