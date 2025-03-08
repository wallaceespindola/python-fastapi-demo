from datetime import datetime

import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory storage for items and a simple auto-increment id mechanism
items_db = {}
current_id = 1


# Pydantic data model for item validation (used in POST, PUT endpoints)
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


# Basic GET endpoint for the root path
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


# Is the application running? Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.now()}


# GET endpoint with path parameter and a query parameter named 'search'
@app.get("/items/{item_id}")
async def read_item(item_id: int, search: str = None):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": items_db[item_id], "search": search}


# GET endpoint that lists all items
@app.get("/items/")
async def list_items():
    return {"items": items_db}


# POST endpoint that creates an item using the Item model for validation
@app.post("/items/")
async def create_item(item: Item):
    global current_id
    item_id = current_id
    items_db[item_id] = item
    current_id += 1
    return {"item_id": item_id, "item": item}


# PUT endpoint that updates an existing item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return {"item_id": item_id, "item": item}


# DELETE endpoint that removes an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully."}


# Dependency Injection example: common parameters shared across endpoints
def common_parameters(search: str = None):
    return {"search": search}


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
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
