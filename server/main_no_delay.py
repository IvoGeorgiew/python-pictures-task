import cv2
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading


class Coordinates(BaseModel):
    x: int
    y: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

coordinates = dict()
previous_coordinates = dict()
capture_thread = None
webcam = cv2.VideoCapture(0)

def capture_image():
    global coordinates
    global previous_coordinates

    conn = sqlite3.connect('coordinates.db')
    cursor = conn.cursor()

    while True:
        ret, frame = webcam.read()
        cv2.imshow('frame', frame)

        if coordinates != previous_coordinates:
            _, image_buffer = cv2.imencode('.jpg', frame)
            image_data = image_buffer.tobytes()

            cursor.execute("INSERT INTO coordinates (x, y, image) VALUES (?, ?, ?)",
                      (coordinates["x"], coordinates["y"], image_data))
            conn.commit()
            print("Image saved and coordinates added to the database")
            previous_coordinates = coordinates

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    webcam.release()

    # Close the SQLite connection
    conn.close()

def start_capture_thread():
    global capture_thread
    if capture_thread is None or not capture_thread.is_alive():
        capture_thread = threading.Thread(target=capture_image)
        capture_thread.start()

@app.post('/coordinates')
async def receive_coordinates(data: Coordinates):
    global coordinates
    print(f"Received coordinates: x={data.x}, y={data.y}")
    coordinates = {
        "x": data.x,
        "y": data.y
    }
    start_capture_thread()

    return {'message': 'Coordinates received successfully'}