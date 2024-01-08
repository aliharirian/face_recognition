import face_recognition
import cv2
import numpy as np
import pymongo
from dotenv import load_dotenv
import os


class FaceRecognition:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Load MongoDB configuration from environment variables
        self.username = os.getenv('MONGO_USERNAME', '')
        self.password = os.getenv('MONGO_PASSWORD', '')
        self.hostname = os.getenv('MONGO_HOSTNAME', 'localhost')
        self.port = int(os.getenv('MONGO_PORT', 27017))
        self.database_env = os.getenv('MONGO_DATABASE', 'face_recognition')
        self.collection_env = os.getenv('MONGO_COLLECTION', 'faces')

        # Connect to MongoDB
        if self.username and self.password:
            uri = f"mongodb://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database_env}"
        else:
            uri = f"mongodb://{self.hostname}:{self.port}/{self.database_env}"
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[self.database_env]
        self.collection = self.database[self.collection_env]

        # Fetch known face encodings and names from MongoDB
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

        # Initialize video capture
        self.video_capture = cv2.VideoCapture(0)

        # Initialize variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def load_known_faces(self):
        for known_face_data in self.collection.find():
            name = known_face_data['name']
            image_binary = known_face_data['image_binary']

            # Decode binary data to numpy array
            image_array = np.frombuffer(image_binary, dtype=np.uint8)

            # Decode the image array
            face_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Find face encodings
            face_encoding = face_recognition.face_encodings(face_img)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)

    def process_frame(self, frame):
        if self.process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color to RGB color
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

    def display_results(self, frame):
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            self.process_frame(frame)
            self.display_results(frame)
            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        self.video_capture.release()
        cv2.destroyAllWindows()


# Create an instance of the FaceRecognition class and run the application
face_recognition_app = FaceRecognition()
face_recognition_app.run()
