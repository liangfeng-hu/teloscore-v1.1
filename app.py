```python
from fastapi import FastAPI
from pydantic import BaseModel
from telos_core import telos_step, TelosState

app = FastAPI(title="TelosCore Full-Memory Build")

class ChatRequest(BaseModel):
    message: str

global_state = TelosState()
global_history = []

@app.get("/")
def root():
    return {
        "name": "TelosCore Full-Memory Build",
        "status": "ok",
        "memory": "EverMemOS-powered",
    }

@app.post("/interact")
def interact(req: ChatRequest):
    result, history = telos_step(req.message, global_state, component_history_override=global_history)
    global global_history
    global_history = history
    return result
