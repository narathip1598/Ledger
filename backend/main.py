from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Hello"}

models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
    
class Answer(BaseModel):
    question_id: int
    choice_id: int
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()
    
@app.get("/questions")
def read_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Questions).all()
    results = []
    for question in questions:
        choices = db.query(models.Choices).filter(models.Choices.question_id == question.id).all()
        results.append({
            "id": question.id,
            "question_text": question.question_text,
            "choices": [{"id": c.id, "choice_text": c.choice_text, "is_correct": c.is_correct} for c in choices]
        })
    return results

@app.get("/choices/{question_id}")
async def read_choices(question_id:int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Choices is not found')
    return result

@app.post("/submit-answers")
async def submit_answers(answers: List[Answer], db: db_dependency):
    for answer in answers:
        db_answer = models.Answers(
            question_id=answer.question_id,
            choice_id=answer.choice_id
        )
        db.add(db_answer)
    db.commit()
    return {"message": "Answers saved successfully"}

@app.post("/check-answers")
async def check_answers(answers: List[Answer], db: db_dependency):
    results = []
    
    for answer in answers:
        # Check if the selected choice is correct
        choice = db.query(models.Choices).filter(models.Choices.id == answer.choice_id).first()
        if choice is None:
            raise HTTPException(status_code=404, detail=f"Choice {answer.choice_id} not found.")
        
        # Get the correct answer for the question
        correct_choice = db.query(models.Choices).filter(
            models.Choices.question_id == answer.question_id, 
            models.Choices.is_correct == True
        ).first()
        
        if correct_choice is None:
            raise HTTPException(status_code=404, detail=f"No correct choice found for question {answer.question_id}.")
        
        # Compare the selected choice with the correct answer
        is_correct = choice.id == correct_choice.id
        
        # Store the result for the user
        results.append({
            "question_id": answer.question_id,
            "selected_choice": choice.choice_text,
            "correct_choice": correct_choice.choice_text,
            "is_correct": is_correct
        })
    
    return {"results": results}
