import cv2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import os

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

def capture_image():
    # Capture an image from the webcam
    webcam = cv2.VideoCapture(0)
    ret, frame = webcam.read()
    webcam.release()

    if ret:
        # Save the captured frame as an image
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, 'new.jpg')
        cv2.imwrite(image_path, frame)
        print(f"Image saved: {image_path}")
    else:
        print("Failed to capture image.")
def run_capture_thread():
    capture_thread = threading.Thread(target=capture_image)
    capture_thread.start()


@app.post('/coordinates')
async def receive_coordinates(data: Coordinates):
    print(f"Received coordinates: X={data.x}, Y={data.y}")
    run_capture_thread()
    return {'message': 'Coordinates received successfully'}