# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from telos_core import telos_step

app = FastAPI(title="TelosCore (Competition Build)")

class Input(BaseModel):
    message: str

@app.post("/interact")
def interact(inp: Input):
    return telos_step(inp.message)

@app.get("/health")
def health():
    return {"status": "ok"}