

from fastapi import FastAPI, HTTPException

# pydantic forces python type hints to be strict and enforcable while your program runs, throwing errors if data does not match expected structure
# also automatically converts incoming data to the correct type whenever possible
from pydantic import BaseModel 

# access {BASE_URL}/docs or {BASE_URL}/redoc to view API tester
app = FastAPI()

# item in a todo list
class Item(BaseModel):
    text: str # deleting default value makes it required
    is_done: bool = False

items = []

@app.get("/")
def root():
    return {"Hello": "World"}

# will pass in item as a query parameter if item type is string
# but if a modeled object like item, requires item as a request body parameter
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

# the limit type hint converts the string into an integer
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

# item_id is index
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
