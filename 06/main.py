from fastapi import FastAPI
from connect import SurveyResult, MotivationQuote

app = FastAPI(title="Motivation API")

@app.get('/MotivationQuote')
async def get_motiviation_quote():
    info = MotivationQuote.select()
    return [{
        "id": i.id,
        "text": i.text,
        "mood_tag": i.mood_tag,
        "author": i.author
    } for i in info]

@app.post('/MotivationQuote_post')
async def post_motivation_quite(text, mood_tag, author):
    info = MotivationQuote.create(
        text=text,
        mood_tag=mood_tag,
        author=author
    )
    return info

@app.put('/MotivationQuote_put/{item_id}')
async def put_motivation_quote(item_id, text, mood_tag, author):
    info = MotivationQuote.get(MotivationQuote.id == item_id)
    info.text = text
    info.mood_tag = mood_tag
    info.author = author
    info.save()
    return info

@app.delete('/MotivationQuote_delete/{item_id}')
async def delete_motivation_quote(item_id):
    deleted_rows = MotivationQuote.delete_by_id(item_id)
    return deleted_rows

@app.get('/SurveyResult')
async def get_survey_result():

    info = SurveyResult.select()
    return [{
        "id": i.id,
        "user_id": i.user_id, 
        "mood": i.mood,       
        "score": i.score   
    } for i in info]

@app.post('/SurveyResult_post')
async def post_survey_result_post(user_id, mood, score):
    
    info = SurveyResult.create(
        user_id=user_id, 
        mood=mood,       
        score=score  
    )
    return info

@app.put('/SurveyResult_put/{item_id}')
async def put_survey_result(item_id: int, user_id: int, mood: str, score: int):
    info = SurveyResult.get(SurveyResult.id == item_id)
    info.user_id = user_id 
    info.mood = mood       
    info.score = score     
    info.save()
    return info

@app.delete('/SurveyResult_delete/{item_id}')
async def delete_survey_result(item_id):
    deleted_rows = SurveyResult.delete_by_id(item_id)
    return deleted_rows