import cv2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import sqlite3

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

webcam = cv2.VideoCapture(0)

def capture_image(coordinates: Coordinates):
    # Capture an image from the webcam
    webcam = cv2.VideoCapture(0)
    ret, frame = webcam.read()
    webcam.release()


    conn = sqlite3.connect('coordinates.db')
    cursor = conn.cursor()

    if ret:
        cv2.imshow('frame', frame)
        _, image_buffer = cv2.imencode('.jpg', frame)
        image_data = image_buffer.tobytes()
        cursor.execute("INSERT INTO coordinates (x, y, image) VALUES (?, ?, ?)",
                    (coordinates.x, coordinates.y, image_data))
        conn.commit()
        conn.close()
        print("New DB entry registered")
    else:
        print("Failed to capture image.")

def run_capture_thread(coordinates: Coordinates):
    capture_thread = threading.Thread(target=capture_image(coordinates))
    capture_thread.start()


@app.post('/coordinates')
async def receive_coordinates(data: Coordinates):
    print(f"Received coordinates: X={data.x}, Y={data.y}")
    run_capture_thread(data)
    return {'message': 'Coordinates received successfully'}