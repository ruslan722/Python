import unittest
import tkinter as tk
from app import TrafficLight

class TestTrafficLight(unittest.TestCase):

    def setUp(self):
        # root
        self.root = tk.Tk()
        self.root.withdraw()  # скрыть окно, чтобы не открывалось
        self.traffic_light = TrafficLight(self.root)

        # эмул
        self.traffic_light.running = True
        self.traffic_light.saved_location = "Тестовая улица"

    def tearDown(self):
        self.root.destroy()

    def test_next_changes_color_from_red_to_green(self):
        # с красного
        self.traffic_light.current_index = 0
        self.traffic_light.getCurrentColor()
        self.assertEqual(
            self.traffic_light.colors[self.traffic_light.current_index][0],
            "red"
        )

        # переключение на жёлтый
        self.traffic_light.next()
        self.assertEqual(
            self.traffic_light.colors[self.traffic_light.current_index][0],
            "yellow"
        )

        # переключение на зелёный
        self.traffic_light.next()
        self.assertEqual(
            self.traffic_light.colors[self.traffic_light.current_index][0],
            "green"
        )


if __name__ == "__main__":
    unittest.main()
