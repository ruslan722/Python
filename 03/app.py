import tkinter as tk
from tkinter import Label, PhotoImage

# === Создаём окно ===
root = tk.Tk()
root.title("Симулятор Светофора")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg='#FFFFFF')

# === Шапка приложения ===
header = Label(root, text="Симулятор Светофора", font=("Helvetica", 14), bg="#0991D5", fg="white")
header.place(x=0, y=0, width=800, height=50)

# === Логотип ===
logo = PhotoImage(file="logo.png")
logo = logo.subsample(30)     
logo_label = Label(root, image=logo, bg="#0991D5")
logo_label.image = logo            
logo_label.place(x=0, y=2)

# === Запуск приложения ===
root.mainloop()
