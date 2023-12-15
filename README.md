# Face Recognition Project

This Python project is a simple university assignment that utilizes the face_recognition library along with OpenCV to perform real-time face recognition through a webcam. It has been designed as an introductory project to showcase basic face recognition capabilities, and in this case, it recognizes a predefined face (Ali Haririan) and displays a bounding box around the recognized face along with the person's name.
## Getting Started

### Prerequisites
- Python 3.x
- Install required packages by running: `pip install -r requirements.txt`

### Installation
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

4. Run the script:
   ```bash
   python face_recognition_script.py
   ```

## Usage

- The script captures video from the default webcam (`video_capture = cv2.VideoCapture(0)`). Adjust the index if using a different camera.

- Replace the sample face image (`face_image.jpg`) in the root directory with the desired image for recognition.

- Modify the `known_face_encodings` and `known_face_names` arrays in the script to include the faces you want to recognize.

- Press 'q' on the keyboard to exit the application.

## File Structure

- `face_recognition_script.py`: Main Python script for face recognition.
- `requirements.txt`: List of required Python packages.
- `face_image.jpg`: Sample face image for learning and recognition.

## Dependencies

- [face_recognition](https://github.com/ageitgey/face_recognition): Library for face recognition.
- [OpenCV](https://github.com/opencv/opencv): Computer vision library for image and video processing.
- [NumPy](https://github.com/numpy/numpy): Fundamental package for scientific computing with Python.

## Acknowledgments

- The face recognition script is based on the `face_recognition` library by [ageitgey](https://github.com/ageitgey/face_recognition).
- Developed by Ali Haririan.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
