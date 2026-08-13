"""
SecPipe API — a minimal task/asset tracker.

This app exists to be carried through the SecPipe CI/CD pipeline: built, tested,
scanned, containerized, deployed to Kubernetes, and observed. Its own logic is
intentionally simple (in-memory storage, no database) so the project stays focused
on the pipeline and security tooling around it.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import itertools

app = FastAPI(
    title="SecPipe API",
    description="Minimal demo API used to exercise the SecPipe CI/CD pipeline.",
    version="0.1.0",
)

# In-memory "database" — resets every time the app restarts. Fine for this lab.
items_db: dict[int, dict] = {}
id_counter = itertools.count(1)


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class Item(ItemCreate):
    id: int


@app.get("/health", tags=["ops"])
def health_check():
    """Used later as a Kubernetes liveness/readiness probe target."""
    return {"status": "ok"}


@app.get("/items", response_model=list[Item], tags=["items"])
def list_items():
    return list(items_db.values())


@app.post("/items", response_model=Item, status_code=201, tags=["items"])
def create_item(item: ItemCreate):
    new_id = next(id_counter)
    stored_item = {"id": new_id, **item.model_dump()}
    items_db[new_id] = stored_item
    return stored_item


@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.delete("/items/{item_id}", status_code=204, tags=["items"])
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None
