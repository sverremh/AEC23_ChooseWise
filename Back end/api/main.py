from typing import Dict, Any
from fastapi import FastAPI

app = FastAPI()

@app.get("/", status_code=200)
def handle_get():
    return {"message": "hello"}

@app.post("/", status_code=201)
def handle_webhook(resp: Dict[Any, Any]):
    print(resp)
    return {"message": resp}