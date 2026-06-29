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
root.attributes('-fullscreen', True)
root.configure(bg="#1e1e2f")

# ------------ Styling ------------
title_font = ("Segoe UI", 40, "bold")
label_font = ("Segoe UI", 20)
footer_font = ("Segoe UI", 28, "bold italic")
entry_bg = "#2d2d44"
entry_fg = "#ffffff"
btn_bg = "#4e88ff"
btn_fg = "#ffffff"
hover_bg = "#366ed8"

# ------------ Center Frame ------------
frame = tk.Frame(root, bg="#1e1e2f")
frame.place(relx=0.5, rely=0.45, anchor="center")

# ------------ Title ------------
title_label = tk.Label(frame, text="🔒 Admin Login", bg="#1e1e2f", fg="white", font=title_font)
title_label.pack(pady=30)

# ------------ Password Entry ------------
password_entry = tk.Entry(frame, show="*", font=label_font, bg=entry_bg, fg=entry_fg,
                          insertbackground="white", width=30, relief="flat")
password_entry.pack(pady=20)

# ------------ Login Button ------------
def on_enter(e):
    login_btn.config(bg=hover_bg)

def on_leave(e):
    login_btn.config(bg=btn_bg)

login_btn = tk.Button(frame, text="Login", font=label_font, bg=btn_bg, fg=btn_fg,
                      activebackground=hover_bg, width=20, height=2, bd=0,
                      command=check_login, cursor="hand2")
login_btn.pack(pady=30)
login_btn.bind("<Enter>", on_enter)
login_btn.bind("<Leave>", on_leave)

# ------------ Big Footer Welcome Message ------------
footer_label = tk.Label(root, text="🎙️ Welcome to Voice File Manager", font=footer_font,
                        bg="#1e1e2f", fg="#ffffff")
footer_label.place(relx=0.5, rely=0.9, anchor="center")  # Centered at bottom

# ------------ Exit Fullscreen on Esc ------------
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# ------------ Run Mainloop ------------
root.mainloop()
