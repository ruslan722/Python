from fastapi import FastAPI, HTTPException
from connect import SurveyResult, MotivationQuote

app = FastAPI(title="Motivation API")

@app.get("/survey/")
def get_all_surveys():
    results = list(SurveyResult.select().dicts())
    return {"surveys": results}

@app.get("/quotes/{mood_tag}")
def get_quotes(mood_tag: str):
    quotes = [q.text for q in MotivationQuote.select().where(MotivationQuote.mood_tag == mood_tag)]
    if not quotes:
        raise HTTPException(status_code=404, detail="Quotes not found")
    return {"quotes": quotes}

@app.get("/state/{user_id}")
def get_user_state(user_id: int):
    surveys = list(SurveyResult.select().where(SurveyResult.user_id == user_id))

    if not surveys:
        raise HTTPException(status_code=404, detail="No surveys found for this user")

    avg_score = sum(s.score for s in surveys) / len(surveys)

    if avg_score >= 7:
        state = "positive"
    elif avg_score >= 4:
        state = "neutral"
    else:
        state = "negative"

    return {
        "user_id": user_id,
        "average_score": avg_score,
        "state": state
    }

@app.get("/motivation/{user_id}")
def get_motivation(user_id: int):
    surveys = list(SurveyResult.select().where(SurveyResult.user_id == user_id))
    if not surveys:
        raise HTTPException(status_code=404, detail="No surveys found for this user")

    avg_score = sum(s.score for s in surveys) / len(surveys)

    if avg_score >= 7:
        state = "positive"
        mood_tag = "happy"
    elif avg_score >= 4:
        state = "neutral"
        mood_tag = "neutral"
    else:
        state = "negative"
        mood_tag = "sad"

    quotes = [q.text for q in MotivationQuote.select().where(MotivationQuote.mood_tag == mood_tag)]

    return {
        "user_id": user_id,
        "average_score": avg_score,
        "state": state,
        "quotes": quotes if quotes else ["Нет цитат для этого состояния"]
    }

