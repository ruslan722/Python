import tkinter as tk
from tkinter import Label, PhotoImage, Button, Entry, messagebox
from datetime import datetime
from connect import TrafficLight as TrafficLightModel   

# === Создаём окно приложения ===
root = tk.Tk()
root.title("Симулятор Светофора")
root.geometry("800x950")
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

# === Класс TrafficLight (логика светофора) ===
class TrafficLight:
    def __init__(self, root):
        self.root = root

        # Цвета и их длительность (секунды)
        self.colors = [
            ("red", 60),
            ("yellow", 3),
            ("green", 30)
        ]
        self.current_index = 0
        self.running = False
        self.remaining_time = 0
        self.saved_location = None
        self.timer_job = None

        # === Поле для ввода названия улицы ===
        Label(root, text="Улица:", font=("Helvetica", 12), bg="white").place(x=50, y=100)
        self.location_entry = Entry(root, font=("Helvetica", 12))
        self.location_entry.place(x=120, y=100, width=150)

        # === Canvas для светофора ===
        self.canvas = tk.Canvas(root, width=200, height=400, bg="black")
        self.canvas.place(x=300, y=150)

        # Лампы
        self.red_light = self.canvas.create_oval(50, 20, 150, 120, fill="gray")
        self.yellow_light = self.canvas.create_oval(50, 140, 150, 240, fill="gray")
        self.green_light = self.canvas.create_oval(50, 260, 150, 360, fill="gray")

        # === Метки для статуса и таймера ===
        self.status_label = Label(root, text="", font=("Helvetica", 20), bg="white")
        self.status_label.place(x=330, y=520)

        self.timer_label = Label(root, text="", font=("Helvetica", 14), bg="white")
        self.timer_label.place(x=330, y=560)

        # === Кнопки управления ===
        self.start_button = Button(root, text="Старт", command=self.start, bg="lightgreen")
        self.start_button.place(x=250, y=590, width=120, height=30)

        self.stop_button = Button(root, text="Стоп", command=self.stop, bg="lightcoral")
        self.stop_button.place(x=400, y=590, width=120, height=30)

    # === Запуск светофора ===
    def start(self):
        if self.running:
            return

        location = self.location_entry.get().strip()
        if not location:
            messagebox.showerror("Ошибка", "Введите название улицы!")
            return

        # сохранение улицы в БД при старте
        TrafficLightModel.create(
            location=location,
            status="init",
            last_updated=datetime.now(),
            duration=0
        )
        self.saved_location = location
        self.running = True
        self.getCurrentColor()

    # === Остановка светофора ===
    def stop(self):
        if self.running:
            self.running = False
            if self.timer_job:
                self.root.after_cancel(self.timer_job)
                self.timer_job = None
            self.status_label.config(text="Остановлен", fg="black")
            self.timer_label.config(text="")
            # === Выключить лампы ===
            self.canvas.itemconfig(self.red_light, fill="gray")
            self.canvas.itemconfig(self.yellow_light, fill="gray")
            self.canvas.itemconfig(self.green_light, fill="gray")

    # === Установка текущего цвета ===
    def getCurrentColor(self):
        if not self.running:
            return

        color, duration = self.colors[self.current_index]

        # Сброс всех ламп
        self.canvas.itemconfig(self.red_light, fill="gray")
        self.canvas.itemconfig(self.yellow_light, fill="gray")
        self.canvas.itemconfig(self.green_light, fill="gray")

        #=== Включить нужную лампу и обновить статус ===
        if color == "red":
            self.canvas.itemconfig(self.red_light, fill="red")
            self.status_label.config(text="Красный", fg="red")
        elif color == "yellow":
            self.canvas.itemconfig(self.yellow_light, fill="yellow")
            self.status_label.config(text="Жёлтый", fg="orange")
        elif color == "green":
            self.canvas.itemconfig(self.green_light, fill="green")
            self.status_label.config(text="Зелёный", fg="green")

        # === Сохраняем данные в БД ===
        if self.saved_location:  # защита, чтобы тесты не падали
            TrafficLightModel.create(
                location=self.saved_location,
                status=color,
                last_updated=datetime.now(),
                duration=duration
            )

        # Устанавливаем таймер
        self.remaining_time = duration
        self.update_timer()

    # === Обновление таймера обратного отсчёта ===
    def update_timer(self):
        if not self.running:
            return

        if self.remaining_time > 0:
            next_color_index = (self.current_index + 1) % len(self.colors)
            next_color_name = self.colors[next_color_index][0]

            names = {"red": "Красный", "yellow": "Жёлтый", "green": "Зелёный"}
            self.timer_label.config(
                text=f"Переключение на {names[next_color_name]} через: {self.remaining_time} сек"
            )
            self.remaining_time -= 1
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.next()

    # === Переключение на следующий цвет ===
    def next(self):
        if not self.running:
            return
        self.current_index = (self.current_index + 1) % len(self.colors)
        self.getCurrentColor()


# === Запуск приложения  ===
if __name__ == "__main__":
    app = TrafficLight(root)
    root.mainloop()

