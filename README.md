# Face Recognition Project

This Python project serves as a fundamental university assignment that leverages the face_recognition library in conjunction with OpenCV to execute real-time face recognition via a webcam. It is designed as an introductory project to demonstrate basic face recognition capabilities. Specifically, it identifies a predefined face (Ali Haririan) and showcases the recognition process by displaying a bounding box around the identified face along with the person's name.
## Getting Started

### Prerequisites
- Python 3.x
- Install required packages by running: `pip install -r requirements.txt`

### Installation And Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/aliharirian/face_recognition.git
   cd face_recognition
   ```

2. Configure the face image:
   - Add a face image file (`face_image.jpg`) to the root directory. This image will be used for learning and recognizing faces.

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. `manage.py`

   This script allows you to manage a MongoDB database containing information about individuals, including their names, family names, ages, and associated images.
   
   #### Setup
   If the `.env` file does not exist, create one and the same directory as `manage.py`. Define the following environment variables in the `.env` file:
   
   ```
   MONGO_USERNAME=<your_username>
   MONGO_PASSWORD=<your_password>
   MONGO_HOSTNAME=<localhost>
   MONGO_PORT=<mongodb_port>
   MONGO_DATABASE=<face_recognition>
   MONGO_COLLECTION=<faces>
   ```
   
   #### Running
   Execute the script using:
   
   ```bash
   python manage.py
   ```
   
   This will open a GUI where you can insert, delete, and view data.

5. `face_recognition_script.py`
   
   This script performs real-time face recognition using a webcam. It loads known faces from the MongoDB database and identifies individuals in the video feed.
   
   #### Running
   Execute the script using:
   
   ```bash
   python face_recognition_script.py
   ```
   
   This will open a window displaying the webcam feed with real-time face recognition.

## File Structure

The project is organized with the following file structure:

```
face_recognition/
│
├── face_recognition_script.py  # Script for real-time face recognition using a webcam.
├── manager.py                  # Script for managing data in a MongoDB database through a GUI.
├── face_image.jpg              # Example face image.
├── LICENSE                     # Project license information. 
├── README.md                   # Project documentation.
└── requirements.txt            # List of project dependencies.  
```

## Dependencies

- [face_recognition](https://github.com/ageitgey/face_recognition): Library for face recognition.
- [OpenCV](https://github.com/opencv/opencv): Computer vision library for image and video processing.
- [NumPy](https://github.com/numpy/numpy): Fundamental package for scientific computing with Python.
- And Include other tools that I used in the `requirements.txt` file.

## Acknowledgments

- The face recognition script is based on the `face_recognition` library by [ageitgey](https://github.com/ageitgey/face_recognition).
- Developed by Ali Haririan.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
