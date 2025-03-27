import cv2
import face_recognition
import numpy as np
import os
import time
import platform
import threading
from time import sleep


class FaceLock:
    def __init__(self, known_face_path, lock_threshold=5, frame_skip=20):
        if not os.path.exists(known_face_path):
            raise FileNotFoundError(f"please capture and save {known_face_path} first!")

        self.known_encoding = face_recognition.face_encodings(face_recognition.load_image_file(known_face_path))[0]
        self.cap = cv2.VideoCapture(0)
        self.lock_threshold = lock_threshold
        self.frame_skip = frame_skip
        self.last_detected = time.time()
        self.frame_count = 0
        self.face_recognized = False
        self.face_locations = []
        self.face_lock = threading.Lock()

    def lock_screen(self):
        os_type = platform.system()
        if os_type == "Windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif os_type == "Linux":
            os.system("xdg-screensaver lock")
        elif os_type == "Darwin":
            os.system("pmset displaysleepnow")

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        detected_faces = face_recognition.face_locations(rgb_small_frame, model="hog")

        with self.face_lock:
            if detected_faces:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, detected_faces)
                for face_encoding in face_encodings:
                    match = face_recognition.compare_faces([self.known_encoding], face_encoding, tolerance=0.5)
                    if match[0]:
                        self.face_recognized = True
                        self.last_detected = time.time()
                        self.face_locations = [(top * 2, right * 2, bottom * 2, left * 2)
                                               for (top, right, bottom, left) in detected_faces]
                        return
            self.face_recognized = False
            self.face_locations = []

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame_count += 1
            if self.frame_count % self.frame_skip == 0:
                self.process_frame(frame)

            with self.face_lock:
                color = (0, 255, 0) if self.face_recognized else (0, 0, 255)
                status_text = "Authorized" if self.face_recognized else "Unauthorized"
                for (top, right, bottom, left) in self.face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            cv2.rectangle(frame, (10, 10), (260, 60), (0, 0, 0), -1)
            cv2.putText(frame, status_text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Face Recognition", frame)
            print(f"[INFO] {status_text} - {time.strftime('%H:%M:%S')}")

            if not self.face_recognized and time.time() - self.last_detected > self.lock_threshold:
                print("Unauthorized face or no face detected! Locking PC...")
                self.lock_screen()
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    face_lock = FaceLock(known_face_path='known_face.jpg')
    face_lock.run()