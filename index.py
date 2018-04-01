import os
from os import walk

from flask import Flask, request, jsonify
import face_recognition

app = Flask(__name__)
app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))

# unknown folder is the folder user need upload his/her face
app.config['UNKNOWN_PEOPLE'] = os.path.join(
    app.config['BASE_DIR'],
    'unknown_people'
)
app.config['KNOWN_PEOPLE'] = os.path.join(
    app.config['BASE_DIR'],
    'known_people'
)


def allowed_file(filename):
    """Check if a file is a picture by its name."""
    return filename.endswith(('.png', '.jpg', '.jpeg'))


def get_all_filesname(folder_name):
    """Get all the filenames in this folder"""
    filename_array = []
    for (dirpath, dirnames, filenames) in walk(folder_name):
        filename_array.extend(filenames)
        break
    return filename_array


def get_all_face_encodings(base_dir, filename_array):
    """Add all faces to numpy and get all faces encoding"""
    all_face_encodings = []
    for filename in filename_array:
        image_path = os.path.join(
            base_dir,
            filename
        )

        # Load image files into numpy arrays
        image_into_numpy = face_recognition.load_image_file(image_path)
        all_face_encodings.append(
            face_recognition.face_encodings(image_into_numpy)[0]
        )
    return all_face_encodings


@app.route('/judge', methods=['POST'])
def judge():
    # get the face files from request
    face_file = request.files['face']

    if allowed_file(face_file.filename):
        # if the image is valid, save at the unknonw_people folder
        face_filepath = os.path.join(
            app.config['UNKNOWN_PEOPLE'],
            face_file.filename
        )
        face_file.save(face_filepath)

        # Load image file into numpy array
        face_image = face_recognition.load_image_file(face_filepath)
        face_encoding = face_recognition.face_encodings(face_image)[0]

        # judge flag, if can_recognition = True, sign success
        can_recognition = False

        # known faces filename array
        known_faces_filenames = get_all_filesname(
            app.config['KNOWN_PEOPLE']
        )

        try:
            # read all known faces from known_people folder
            known_faces = get_all_face_encodings(
                app.config['KNOWN_PEOPLE'],
                known_faces_filenames
            )
        except IndexError:
            print("Cannot locate any faces in at least one of the images")
            return '<h1>Bad Request</h1>', 404

        # start face recogniton
        results = face_recognition.compare_faces(
            known_faces,
            face_encoding,
            tolerance=0.5
        )

        # judge whether have a face exist in known people
        if not True in results:
            can_recognition = False
        else:
            can_recognition = True

        return jsonify({"can_recognition": can_recognition})
