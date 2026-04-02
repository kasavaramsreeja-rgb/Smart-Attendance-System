import cv2
import time
from db import mark_attendance

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Start camera
cam = cv2.VideoCapture(0)

print("Starting attendance system...")

names = ["", "Sreeja"]

marked_ids = set()

capture_count = 0
max_captures = 1   # change if needed

while True:
    ret, img = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 100:
            name = names[id]

            if id not in marked_ids:
                mark_attendance(id)
                marked_ids.add(id)
                capture_count += 1

                print("⏳ Capturing... please wait")
                time.sleep(2)   # 🔥 slows down AFTER detection

        else:
            name = "Unknown"

        cv2.putText(img, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

        cv2.rectangle(img, (x, y), (x+w, y+h),
                      (255, 0, 0), 2)

    cv2.imshow('Attendance System', img)

    # 🔥 SLOW DOWN LOOP SPEED (optional)
    time.sleep(0.5)

    if capture_count >= max_captures:
        print("✅ Attendance captured. Closing camera...")
        time.sleep(2)
        break

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()