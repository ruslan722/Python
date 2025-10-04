import unittest
from fastapi.testclient import TestClient
from connect import SurveyResult, MotivationQuote
from main import app


class TestMotivationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание таблиц в MySQL, если их ещё нет"""
        SurveyResult._meta.database.connect(reuse_if_open=True)
        SurveyResult._meta.database.create_tables([SurveyResult, MotivationQuote], safe=True)
        cls.client = TestClient(app)

        
        if MotivationQuote.select().count() == 0:
            MotivationQuote.create(text="Улыбнись миру!", mood_tag="happy", author="Автор 1")
            MotivationQuote.create(text="Все пройдет.", mood_tag="neutral", author="Автор 2")
            MotivationQuote.create(text="Не сдавайся!", mood_tag="sad", author="Автор 3")

        if SurveyResult.select().count() == 0:
            SurveyResult.create(user_id=1, mood="happy", score=8)
            SurveyResult.create(user_id=1, mood="happy", score=6)
            SurveyResult.create(user_id=2, mood="sad", score=2)

    @classmethod
    def tearDownClass(cls):
        """Закрытие соединения с базой"""
        SurveyResult._meta.database.close()

    # ---------------------- ТЕСТЫ ----------------------

    def test_get_all_surveys(self):
        response = self.client.get("/survey/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("surveys", data)
        self.assertGreaterEqual(len(data["surveys"]), 3)  

    def test_get_quotes_found(self):
        response = self.client.get("/quotes/happy")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Улыбнись миру!", data["quotes"])

    def test_get_quotes_not_found(self):
        response = self.client.get("/quotes/unknown")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Quotes not found")

    def test_get_user_state_positive(self):
        response = self.client.get("/state/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["state"], "positive")
        self.assertAlmostEqual(data["average_score"], 7.0, delta=0.1)

    def test_get_user_state_negative(self):
        response = self.client.get("/state/2")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["state"], "negative")

    def test_get_user_state_not_found(self):
        response = self.client.get("/state/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "No surveys found for this user")

    def test_get_motivation_positive(self):
        response = self.client.get("/motivation/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["state"], "positive")
        self.assertIn("Улыбнись миру!", data["quotes"][0])

    def test_get_motivation_negative(self):
        response = self.client.get("/motivation/2")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["state"], "negative")
        self.assertIn("Не сдавайся!", data["quotes"][0])

    def test_get_motivation_not_found(self):
        response = self.client.get("/motivation/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "No surveys found for this user")


if __name__ == "__main__":
    unittest.main(verbosity=2)
