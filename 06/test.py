import unittest
from fastapi.testclient import TestClient
import httpx
from connect import SurveyResult, MotivationQuote
from main import app


class TestMotivationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
       
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
        
        SurveyResult._meta.database.close()

    

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

   

    def test_create_survey(self):
        response = self.client.post("/survey/", json={"user_id": 10, "question": "Как настроение?", "score": 9})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("survey_id", data)

        
        created = SurveyResult.get_or_none(SurveyResult.id == data["survey_id"])
        self.assertIsNotNone(created)
        self.assertEqual(created.score, 9)

    def test_update_survey(self):
        survey = SurveyResult.create(user_id=11, question="Тест вопрос", score=4)
        response = self.client.put(f"/survey/{survey.id}", json={"score": 7})
        self.assertEqual(response.status_code, 200)
        updated = SurveyResult.get_by_id(survey.id)
        self.assertEqual(updated.score, 7)

    def test_delete_survey(self):
        survey = SurveyResult.create(user_id=12, question="Удалить", score=5)
        response = self.client.delete(f"/survey/{survey.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(SurveyResult.get_or_none(SurveyResult.id == survey.id))

    def test_delete_survey_not_found(self):
        response = self.client.delete("/survey/99999")
        self.assertEqual(response.status_code, 404)



    def test_create_quote(self):
        response = self.client.post("/quotes/", json={"text": "Будь сильным!", "mood_tag": "neutral"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("quote_id", data)
        created = MotivationQuote.get_by_id(data["quote_id"])
        self.assertEqual(created.text, "Будь сильным!")

    def test_update_quote(self):
        quote = MotivationQuote.create(text="Старый текст", mood_tag="sad")
        response = self.client.put(f"/quotes/{quote.id}", json={"text": "Обновленный текст"})
        self.assertEqual(response.status_code, 200)
        updated = MotivationQuote.get_by_id(quote.id)
        self.assertEqual(updated.text, "Обновленный текст")

    def test_delete_quote(self):
        quote = MotivationQuote.create(text="Удалить цитату", mood_tag="neutral")
        response = self.client.delete(f"/quotes/{quote.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(MotivationQuote.get_or_none(MotivationQuote.id == quote.id))

    def test_delete_quote_not_found(self):
        response = self.client.delete("/quotes/99999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)

