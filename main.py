from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import pyautogui
import threading
import cv2
from sqlmodel import create_engine, SQLModel, Field, Session
import asyncio

# Defined the model
class Coordinates(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    x: int
    y: int
    image: bytes


DATABASE_URL = "sqlite:///coordinates.db"
# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)
# Creates tables if they don't exist, in this case Coordinates
SQLModel.metadata.create_all(engine)

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Coordinates</title>
    </head>
    <body>
        <p id="coordinates">2</p>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");

            ws.onmessage = function(event) {
                var coordinate = document.getElementById('coordinates');
                coordinate.innerHTML = event.data;
            };

            function requestCoordinates() {
                ws.send("get_coordinates");
            }

            setInterval(requestCoordinates, 100);
            document.addEventListener('mousedown', function(event) {
                if (event.button === 0) {
                    ws.send("left_click");
                }
            });
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "get_coordinates":
            position = pyautogui.position()
            await websocket.send_text(f"X={position.x} Y={position.y}")
        elif data == "left_click":
            print("Left mouse button clicked")
            model = Coordinates(x=position.x, y=position.y)
            await left_button_click(model)
            data = "get_coordinates"


def capture_image():
    webcam = cv2.VideoCapture(0)
    ret, frame = webcam.read()
    webcam.release()
    if ret:
        cv2.imshow('frame', frame)
        _, image_buffer = cv2.imencode('.jpg', frame)
        image_data = image_buffer.tobytes()
        print("Image captured")
        return image_data
    else:
        print("Failed to capture image.")
        return False


def add_pic_to_db_async(coordinates: Coordinates, image_data):
    with Session(engine) as session:
        coordinate = Coordinates(x=coordinates.x, y=coordinates.y, image=image_data)
        session.add(coordinate)
        session.commit()
        print("Image uploaded to db")


def add_pic_to_db(coordinates: Coordinates, image_data):
    threading.Thread(target=add_pic_to_db_async, args=(coordinates, image_data)).start()


async def left_button_click(coordinates: Coordinates):
    image_data = capture_image()
    if image_data:
        add_pic_to_db(coordinates, image_data)


if __name__ == "__main__":
    asyncio.run(app.run())