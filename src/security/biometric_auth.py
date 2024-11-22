# src/security/biometric_auth.py

import cv2
import numpy as np
import os
from sklearn.metrics import pairwise

class BiometricAuth:
    def __init__(self, known_faces_dir='known_faces'):
        """Initialize the BiometricAuth class."""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = []  # List to store known face encodings
        self.known_names = []  # List to store names corresponding to known faces
        self.load_known_faces(known_faces_dir)

    def load_known_faces(self, directory):
        """Load known faces from a directory."""
        for filename in os.listdir(directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(directory, filename)
                face_image = cv2.imread(image_path)
                encoding = self.encode_face(face_image)
                if encoding is not None:
                    self.known_faces.append(encoding)
                    self.known_names.append(name)

    def capture_face(self):
        """Capture a face from the webcam."""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                return frame[y:y+h, x:x+w]
        return None

    def add_known_face(self, face_image, name):
        """Add a known face encoding to the list."""
        encoding = self.encode_face(face_image)
        if encoding is not None:
            self.known_faces.append(encoding)
            self.known_names.append(name)

    def authenticate(self, captured_face):
        """Authenticate the captured face against known faces."""
        if captured_face is None:
            return None
        captured_encoding = self.encode_face(captured_face)
        if captured_encoding is None:
            return None

        distances = pairwise.euclidean_distances([captured_encoding], self.known_faces)
        min_distance_index = np.argmin(distances)
        if distances[0][min_distance_index] < 0.6:  # Threshold for matching
            return self.known_names[min_distance_index]
        return None

    def encode_face(self, face_image):
        """Encode the face image using a dummy implementation (replace with actual encoding logic)."""
        # Here we use a simple method to flatten the image as a placeholder
        if face_image is not None:
            face_image = cv2.resize(face_image, (128, 128))  # Resize for consistency
            return face_image.flatten()  # Flatten the image to a 1D array
        return None

    def compare_faces(self, encoding1, encoding2):
        """Compare two face encodings."""
        return pairwise.euclidean_distances([encoding1], [encoding2])[0][0] < 0.6  # Threshold

# Example usage
if __name__ == "__main__":
    biometric_auth = BiometricAuth()

    # Capture a face for authentication
    captured_face = biometric_auth.capture_face()
    if captured_face is not None:
        identity = biometric_auth.authenticate(captured_face)
        if identity:
            print(f"Authenticated as: {identity}")
        else:
            print("Authentication failed.")
    else:
        print("No face captured.")
