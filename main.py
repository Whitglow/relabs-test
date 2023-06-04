from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

message_counter = 0
message_list = []

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global message_counter
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            message = json.loads(data)
            message_counter += 1
            message_with_number = f"{message_counter}. {message}"
            message_list.append(message_with_number)
            await websocket.send_text(json.dumps(message_list))
        except WebSocketDisconnect:
            break

@app.post('/clear_messages')
async def clear_messages():
    global message_list, message_counter
    message_list = []
    message_counter = 0
    return {'message': 'Messages cleared'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000)