from fastapi import FastAPI, HTTPException, Request
from connect import SurveyResult, MotivationQuote

app = FastAPI(title="Motivation API")



@app.get("/survey/")
def get_all_surveys():
    results = list(SurveyResult.select().dicts())
    return {"surveys": results}


@app.get("/survey/{survey_id}")
def get_survey(survey_id: int):
    survey = SurveyResult.get_or_none(SurveyResult.id == survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey.__data__


@app.post("/survey/")
async def create_survey(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    question = data.get("question")
    score = data.get("score")

    if user_id is None or question is None or score is None:
        raise HTTPException(status_code=400, detail="Missing required fields")

    survey = SurveyResult.create(user_id=user_id, question=question, score=score)
    return {"message": "Survey created", "survey_id": survey.id}


@app.put("/survey/{survey_id}")
async def update_survey(survey_id: int, request: Request):
    data = await request.json()
    survey = SurveyResult.get_or_none(SurveyResult.id == survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    if "question" in data:
        survey.question = data["question"]
    if "score" in data:
        survey.score = data["score"]

    survey.save()
    return {"message": "Survey updated successfully"}


@app.delete("/survey/{survey_id}")
def delete_survey(survey_id: int):
    deleted = SurveyResult.delete().where(SurveyResult.id == survey_id).execute()
    if not deleted:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Survey deleted successfully"}



@app.get("/quotes/")
def get_all_quotes():
    quotes = list(MotivationQuote.select().dicts())
    return {"quotes": quotes}


@app.get("/quotes/{mood_tag}")
def get_quotes(mood_tag: str):
    quotes = [q.text for q in MotivationQuote.select().where(MotivationQuote.mood_tag == mood_tag)]
    if not quotes:
        raise HTTPException(status_code=404, detail="Quotes not found")
    return {"quotes": quotes}


@app.post("/quotes/")
async def create_quote(request: Request):
    data = await request.json()
    text = data.get("text")
    mood_tag = data.get("mood_tag")

    if text is None or mood_tag is None:
        raise HTTPException(status_code=400, detail="Missing required fields")

    quote = MotivationQuote.create(text=text, mood_tag=mood_tag)
    return {"message": "Quote created", "quote_id": quote.id}


@app.put("/quotes/{quote_id}")
async def update_quote(quote_id: int, request: Request):
    data = await request.json()
    quote = MotivationQuote.get_or_none(MotivationQuote.id == quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    if "text" in data:
        quote.text = data["text"]
    if "mood_tag" in data:
        quote.mood_tag = data["mood_tag"]

    quote.save()
    return {"message": "Quote updated successfully"}


@app.delete("/quotes/{quote_id}")
def delete_quote(quote_id: int):
    deleted = MotivationQuote.delete().where(MotivationQuote.id == quote_id).execute()
    if not deleted:
        raise HTTPException(status_code=404, detail="Quote not found")
    return {"message": "Quote deleted successfully"}


# ---------------------- #
#  Дополнительные GET API #
# ---------------------- #

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
