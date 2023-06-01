import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import cv2

conn = sqlite3.connect('coordinates.db')
cursor = conn.cursor()

cursor.execute("SELECT x, y, image FROM coordinates")
rows = cursor.fetchall()

for row in rows:
    x, y, image_data = row
    image_buffer = bytearray(image_data)
    nparr = np.frombuffer(image_buffer, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f"Coordinates: X={x}, Y={y}")
    plt.show()

conn.close()