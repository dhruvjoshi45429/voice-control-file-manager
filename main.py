import os 
import speech_recognition as sr
import pyttsx3
from tkinter import *
from tkinter import scrolledtext
from datetime import datetime
from cryptography.fernet import Fernet

# ========== Text-to-Speech Setup ==========
engine = pyttsx3.init()
def speak(text):
    display_output("Assistant: " + text)
    engine.say(text)
    engine.runAndWait()

# ========== Encryption Key Setup ==========
if not os.path.exists("filekey.key"):
    key = Fernet.generate_key()
    with open("filekey.key", "wb") as key_file:
        key_file.write(key)

with open("filekey.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

# ========== GUI Output ==========
def display_output(text):
    command_output.insert(END, text + "\n")
    command_output.see(END)
    root.update()

# ========== File List Refresh ==========
def refresh_file_list():
    file_listbox.delete(0, END)
    for file in os.listdir():
        if file.endswith(".txt"):
            file_listbox.insert(END, file)

# ========== Action Logger ==========
def log_action(action):
    with open("log.txt", "a") as log:
        log.write(f"[{datetime.now()}] {action}\n")
    display_output(f">> {action}")

# ========== Voice Command Listener ==========
def take_command():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        display_output("🎤 Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)

        display_output("Listening...")
        display_output("Speak command...")
        speak("Speak command...")

        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=8)
            command = r.recognize_google(audio, language="en-IN")
            display_output("You: " + command)
            return command.lower()

        except sr.UnknownValueError:
            display_output("❌ Could not understand.")
            speak("I did not understand. Please try again.")
            return ""
        except sr.RequestError:
            display_output("❌ Internet error.")
            speak("Sorry, internet issue.")
            return ""
        except sr.WaitTimeoutError:
            display_output("⏱️ Listening timed out.")
            speak("Too much silence. Try again.")
            return ""

# ========== File Operations ==========
def create_file(name):
    with open(name, 'w') as f:
        f.write("")
    speak(f"{name} created")
    log_action(f"Created file: {name}")
    refresh_file_list()

def delete_file(name):
    if os.path.exists(name):
        os.remove(name)
        speak(f"{name} deleted")
        log_action(f"Deleted file: {name}")
        refresh_file_list()
    else:
        speak("File not found")

def rename_file(old, new):
    if os.path.exists(old):
        os.rename(old, new)
        speak("File renamed")
        log_action(f"Renamed {old} to {new}")
        refresh_file_list()
    else:
        speak("File not found")

def encrypt_file(name):
    if os.path.exists(name):
        with open(name, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(name, 'wb') as f:
            f.write(encrypted)
        speak("File encrypted")
        log_action(f"Encrypted file: {name}")
    else:
        speak("File not found")

def decrypt_file(name):
    if os.path.exists(name):
        with open(name, 'rb') as f:
            data = f.read()
        try:
            decrypted = fernet.decrypt(data)
            with open(name, 'wb') as f:
                f.write(decrypted)
            speak("File decrypted")
            log_action(f"Decrypted file: {name}")
        except:
            speak("Decryption failed")
    else:
        speak("File not found")

def open_file(name):
    if os.path.exists(name):
        os.startfile(name)
        speak("File opened")
        log_action(f"Opened file: {name}")
    else:
        speak("File not found")

# ========== Command Handler ==========
def handle_command():
    command = take_command()

    if "create file" in command:
        speak("File name?")
        name = take_command()
        if name:
            create_file(name + ".txt")

    elif "delete file" in command:
        speak("File name?")
        name = take_command()
        if name:
            delete_file(name + ".txt")

    elif "rename file" in command:
        speak("Old name?")
        old = take_command()
        speak("New name?")
        new = take_command()
        if old and new:
            rename_file(old + ".txt", new + ".txt")

    elif "open file" in command:
        speak("File name?")
        name = take_command()
        if name:
            open_file(name + ".txt")

    elif "encrypt file" in command:
        speak("File name?")
        name = take_command()
        if name:
            encrypt_file(name + ".txt")

    elif "decrypt file" in command:
        speak("File name?")
        name = take_command()
        if name:
            decrypt_file(name + ".txt")

    elif "exit" in command:
        speak("Goodbye!")
        root.destroy()  # 👈 Proper close

    else:
        speak("Command not recognized")

# ========== GUI Setup ==========
root = Tk()
root.title("Voice File Manager")
root.attributes("-fullscreen", True)

# Background Canvas
canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_rectangle(0, 0, root.winfo_screenwidth(), 250, fill="#003366", outline="")
canvas.create_rectangle(0, 250, root.winfo_screenwidth(), root.winfo_screenheight(), fill="#1c1c1c", outline="")

# Header
header = Label(root, text="Voice Controlled File Manager", font=("Helvetica", 20, "bold"), bg="#003366", fg="#00ffcc")
header.place(relx=0.5, y=50, anchor="center")

# Buttons
speak_btn = Button(root, text="Speak Command", font=("Arial", 14), bg="#00cc99", fg="white", command=handle_command)
speak_btn.place(relx=0.5, y=110, anchor="center")

log_btn = Button(root, text="Open Log File", font=("Arial", 14), bg="#3366cc", fg="white", command=lambda: os.startfile("log.txt"))
log_btn.place(relx=0.5, y=170, anchor="center")

exit_btn = Button(root, text="Exit", font=("Arial", 14), bg="#cc0000", fg="white", command=root.destroy)
exit_btn.place(relx=0.5, y=230, anchor="center")

# Terminal Output
command_output = scrolledtext.ScrolledText(root, height=20, width=100, bg="black", fg="lime", font=("Consolas", 12))
command_output.place(relx=0.65, rely=0.65, anchor="center")

# File List
file_listbox = Listbox(root, width=40, height=20, bg="white", font=("Arial", 12))
file_listbox.place(relx=0.05, rely=0.65, anchor="w")

# Init File List
refresh_file_list()

# Escape key to exit fullscreen
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# Start GUI
root.mainloop()
