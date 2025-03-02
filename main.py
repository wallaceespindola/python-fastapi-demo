from datetime import datetime

import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False


def test_item_with_error_message():
    item = Item(name="test", price="hi")
    print(item)
    assert item.name == "test"
    assert item.price == 10.0
    assert item.is_offer is False


def test_item_with_no_error_message():
    item = Item(name="test", price=10)
    print(item)
    assert item.name == "test"
    assert item.price == 10.0
    assert item.is_offer is False


@app.get("/")
def read_root():
    return {"message": f"Hello World: {datetime.now()}"}
    # return {"message": "Hello World"}


app = FastAPI()


# Pydantic data model for item validation
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


# Basic GET endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.now()}


# GET endpoint with path parameter and optional query parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# POST endpoint that creates an item using the Item model for validation
@app.post("/items/")
async def create_item(item: Item):
    return {"item": item.dict()}


# Dependency Injection example: common parameters shared across endpoints
def common_parameters(q: str = None):
    return {"q": q}


@app.get("/dependency/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/dependency/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"users_query": commons}


# Background Tasks example: process tasks after response is sent
def write_log(message: str):
    with open("log.txt", "a") as log:
        log.write(message + "\n")


@app.post("/send-notification/")
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "Notification sent!")
    return {"message": "Notification will be sent in the background"}


# Run the application using uvicorn when executing this file directly.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
