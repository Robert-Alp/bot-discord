from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Annotated
from sqlmodel import select
from api.v1.models import TopicBan
from database import SessionDeps


apiv1 = APIRouter(prefix="/api/v1")

class AddTopic(BaseModel):
    topic: str

@apiv1.get("/bad-topics")
def get_bad_topic(session: SessionDeps):
    statement = select(TopicBan)
    result = session.exec(statement=statement)
    return result.all()

@apiv1.post("/bad-topics")
def addAuthor(topic: TopicBan, session: SessionDeps):
    
    try:
        topic.topic = topic.topic.lower()
        session.add(topic)
        session.commit()
        session.refresh(topic)
        return {
            "message": "Sujet ajouter avec succès",
        }
    except:
        return {
            "message": "Erreur lors de l'ajout"
        }


class DeleteTopicBody(BaseModel):
    topic: Annotated[str, Field(max_length=30)]

@apiv1.delete("/bad-topics")
def addAuthor(body: DeleteTopicBody, session: SessionDeps):
    try:
        statement = select(TopicBan).where(TopicBan.topic == body.topic)
        results = session.exec(statement)
        firstTopic = results.first()
        session.delete(firstTopic)
        session.commit()
        return {
            "message": "Suppression avec succès"
        }
    except:
        return {
            "message": "Erreur lors de la suppression"
        }
    


