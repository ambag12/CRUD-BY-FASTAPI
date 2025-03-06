from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import User
from database import engine, SessionLocal, Base
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

Base.metadata.create_all(bind=engine)

app = FastAPI()

class UserSerializer(BaseModel):
    name:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/post/")
def create_user(create:UserSerializer, db: Session=Depends(get_db)):
    
    return User.create(db, name=create.name)


@app.get("/users/{user_id}")
def get_user(user_id:int, db: Session = Depends(get_db)):
    return User.get(db, id=user_id)

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.delete("/del_users/{user_id}")
def delete_user(user_id:int, db: Session = Depends(get_db)):
    user = User.get(db, id=user_id)
    if user:
        user.delete(db)
        return {"message": "User deleted"}
    return {"error": "User not found"}

@app.put("/update_users/{user_id}")
async def update_record(user_id: int,payload:UserSerializer, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return User.update_records(user, payload, db)
    
    return {"error": "User not found"}