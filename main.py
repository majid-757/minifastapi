from fastapi import FastAPI, Body, Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()    


app = FastAPI()


FakeDatabase = {
    1:{'task': 'Clean car'},
    2:{'task': 'write blog'},
    3:{'task': 'Start stream'},

}


@app.get('/')
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items



@app.get("/{id}")
def getItems(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item





# options 1
# @app.post("/")
# def addItem(item:str):
#     newId = len(FakeDatabase.keys()) + 1
#     FakeDatabase[newId] = {"task":task}
#     return FakeDatabase



#  options 2
@app.post("/")
def addItem(item:schemas.Item, session: Session= Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item



# options 3
# @app.post("/")
# def addItem(body = Body()):
#     newId = len(FakeDatabase.keys()) + 1
#     FakeDatabase[newId] = {"task":body['task']}
#     return FakeDatabase




@app.put('/{id}')
def updateItems(id:int, item:schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject = item.task
    session.commit()
    return itemObject


@app.delete('/{id}')
def updateItems(id:int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted....'



