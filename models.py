from typing import Annotated
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True) 
    name= Column(String(50))

    @classmethod
    def get(cls, db:Session, id: int):
        return db.query(cls).filter(cls.id == id).first()
    @classmethod
    def create(cls,db:Session, name:str):
        user_create=cls(name=name)
        db.add(user_create)
        db.commit()
        db.refresh(user_create)
        return user_create
    def delete(self,db:Session):
        db.delete(self)
        db.commit()
    @classmethod
    def update_records(cls, user, payload, db: Session):
        user.name = payload.name
        db.commit()
        db.refresh(user)
        return {"message": "User updated", "user": user}