from typing import Dict, Any
from speckle import get_data_from_speckle
from fastapi import FastAPI
from specklepy.api.wrapper import StreamWrapper
from specklepy.api import operations

app = FastAPI()

@app.get("/", status_code=200)
def handle_get():
    return {"message": "hello"}

@app.post("/", status_code=201)
def handle_webhook(resp: Dict[Any, Any]):
    print(resp)
    STREAM_ID = resp["payload"]["streamId"]
    OBJECT_ID = resp["payload"]["data"]["commit"]["objectId"]

    get_data_from_speckle(STREAM_ID, OBJECT_ID)

    return {"message": resp}