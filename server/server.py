from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import random
import string
import asyncio
import time
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def generate_id():
    return "".join([random.choice(string.digits) for i in range(20)])

async def reset_game(timer=180):
    await asyncio.sleep(timer)
    app.state.players = []
    app.state.started = 0


@app.on_event("startup")
async def startup_event():
    app.state.players = []
    app.state.started = 0
    app.state.image_timestamp = time.time()

@app.get("/")
async def home():
    return FileResponse('static/game.html')

@app.post("/join")
async def join(name: str):
    if len(app.state.players) > 1:
        raise HTTPException(status_code=403, detail="Game already running")
    id = generate_id()
    app.state.players.append({"id": id, "name": name, "prompt": "", "player": len(app.state.players)})
    if len(app.state.players) > 1:
        app.state.started = time.time()
        asyncio.create_task(reset_game())
        return {"id": id, "detail": "ok", "player": 1}
    else:
        return {"id": id, "detail": "waiting for more players...", "player": 0}


@app.post("/update/{id}")
async def update(prompt: str, id: str):
    if len(app.state.players) < 2:
        raise HTTPException(status_code=403, detail="Game not running")
    for player in app.state.players:
        if player["id"] == id:
            player["prompt"] = prompt
            return
    else:
        raise HTTPException(status_code=403, detail="Player id invalid")


@app.post("/notify")
async def notify():
    app.state.image_timestamp = time.time()      

@app.get("/status")
async def status():
    return {"players": list(map(lambda x: dict(x, **{"id": None}), app.state.players)), "started": app.state.started, "now": time.time(), "images": app.state.image_timestamp}
