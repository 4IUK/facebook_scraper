import os
import face_recognition
from concurrent.futures import ProcessPoolExecutor
from PIL import Image

class FaceRecognitionActor:
    def __init__(self, known_faces_location, unknown_faces_location):
        self.known_faces_location = known_faces_location
        self.unknown_faces_location = unknown_faces_location

    def process_known_image(self, known_image_path):
        # Load a known image and extract face encodings
        known_image = face_recognition.load_image_file(known_image_path)
        face_encodings = face_recognition.face_encodings(known_image)
        
        if face_encodings:
            # If faces are detected, return the first face encoding
            encoding = face_encodings[0]
            return encoding
        else:
            # Handle the case when no face is detected in the image
            print(f"No face found in {known_image_path}")
            return None

    def compare_faces(self):
        # Load known faces using multiple processes
        with ProcessPoolExecutor() as executor:
            known_encodings = list(executor.map(self.process_known_image, [os.path.join(self.known_faces_location, filename) for filename in os.listdir(self.known_faces_location)]))
            known_names = [os.path.splitext(filename)[0] for filename in os.listdir(self.known_faces_location)]

        # Load unknown faces and compare with known faces
        for unknown_filename in os.listdir(self.unknown_faces_location):
            unknown_image_path = os.path.join(self.unknown_faces_location, unknown_filename)
            unknown_image = face_recognition.load_image_file(unknown_image_path)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            # Compare face encodings to find matches
            results = face_recognition.compare_faces(known_encodings, unknown_encoding)

            # Find the first matching face
            matched_index = next((i for i, result in enumerate(results) if result), None)

            if matched_index is not None:
                # If a match is found, print the matched name
                matched_name = known_names[matched_index]
                print(f"Found {matched_name} in {unknown_filename}")
            else:
                print(f"No match found in {unknown_filename}")

    def delete_unknown_images(self):
        # Delete all unknown images in the specified directory
        for filename in os.listdir(self.unknown_faces_location):
            file_path = os.path.join(self.unknown_faces_location, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f'Deleted {file_path}')
            except FileNotFoundError:
                print(f'File not found: {file_path}')
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')

    def extract_faces_from_directory(self, directory, scale_factor=1.5):
        # Create an "unknown" directory if it doesn't exist
        output_directory = "unknown"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Loop through each image in the directory
        for filename in os.listdir(directory):
            image_path = os.path.join(directory, filename)
            image = face_recognition.load_image_file(image_path)

            # Find all face locations in the image
            face_locations = face_recognition.face_locations(image)

            # Loop through each face and save it to the "unknown" directory
            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location

                # Enlarge the bounding box around the face
                face_width = right - left
                face_height = bottom - top
                left = max(0, left - int(face_width * (scale_factor - 1) / 2))
                top = max(0, top - int(face_height * (scale_factor - 1) / 2))
                right = min(image.shape[1], right + int(face_width * (scale_factor - 1) / 2))
                bottom = min(image.shape[0], bottom + int(face_height * (scale_factor - 1) / 2))

                # Crop the image to get the enlarged face
                face_image = image[top:bottom, left:right]

                # Convert the NumPy array to a PIL image
                pil_image = Image.fromarray(face_image)

                # Save the face to the "unknown" directory with a name like "face_1.png", "face_2.png", ...
                processed_filename = filename.split('.')[0]
                face_filename = os.path.join(output_directory, f"{processed_filename}_{i+1}.png")
                pil_image.save(face_filename)

                print(f"Face {i+1} from {filename} saved to {face_filename}.")

            # Delete the original image after extraction
            try:
                if os.path.isfile(image_path):
                    os.unlink(image_path)
                    print(f'Deleted original image: {image_path}')
            except Exception as e:
                print(f'Error deleting original image {image_path}: {e}')

# Example usage
known_faces_location = 'known/'
unknown_faces_location = 'unknown/'

# actor = FaceRecognitionActor(known_faces_location, unknown_faces_location)
# actor.extract_faces_from_directory(unknown_faces_location)
# actor.compare_faces()
# actor.delete_unknown_images()
