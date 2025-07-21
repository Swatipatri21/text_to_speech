import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
import pdfplumber

# Initialize engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

# Create main window
root = tk.Tk()
root.title("Text-to-Speech App")
root.geometry("500x500")
root.configure(bg='lavender')

# Text input box
entry = tk.Text(root, height=8, width=50, font=('Arial', 14), bg='lightyellow', fg='purple', highlightbackground='purple', highlightthickness=2)
entry.pack(pady=10)

# Volume slider
def set_volume(val):
    engine.setProperty('volume', float(val)/100)

volume_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Volume', command=set_volume, bg='lavender')
volume_slider.set(100)
volume_slider.pack(pady=5)

# Voice selector
voices = engine.getProperty('voices')
voice_var = tk.StringVar(value=voices[1].id)

def update_voice(*args):
    engine.setProperty('voice', voice_var.get())

voice_menu = tk.OptionMenu(root, voice_var, *[v.id for v in voices], command=update_voice)
voice_menu.pack(pady=5)

# Speak function
def speak_text():
    text = entry.get("1.0", tk.END).strip()
    if text:
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showwarning("No Text", "Please enter some text first.")

# PDF Import function
def import_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                entry.delete("1.0", tk.END)
                entry.insert(tk.END, text.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Could not read PDF: {e}")

# Buttons
pdf_btn = tk.Button(root, text="Import PDF", command=import_pdf, fg='white', bg='darkgreen', font=('Arial', 12, 'bold'))
pdf_btn.pack(pady=10)

speak_btn = tk.Button(root, text="Speak", command=speak_text, fg='white', bg='blue', font=('Arial', 12, 'bold','underline'), relief='raised')
speak_btn.pack(pady=10)

root.mainloop()