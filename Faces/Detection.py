import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from numpy import asarray
from PIL import Image
from mtcnn import MTCNN
import numpy as np
import os

from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine


def get_detector():
    return MTCNN()


def extract_face_from_image(image, detector, required_size=(224, 224)):
    # load image and detect faces
    faces = detector.detect_faces(image)
    face_images = []

    for face in faces:
        # extract the bounding box from the requested face
        x1, y1, width, height = face['box']
        x2, y2 = x1 + width, y1 + height

        # extract the face
        face_boundary = np.asarray(image)[y1:y2, x1:x2]

        # resize pixels to the model size
        face_image = Image.fromarray(face_boundary)
        face_image = face_image.resize(required_size)
        face_array = asarray(face_image)
        face_images.append(face_array)

    return face_images


def get_petes(detector):

    petes = [plt.imread(os.path.join('reference_images', 'allpete.jpg'))]

    face_images = []
    for pete in petes:
        faces = extract_face_from_image(pete, detector)
        for face in faces:
            face_image = Image.fromarray(face)
            face_image = face_image.resize((224, 224))
            face_array = asarray(face_image)
            face_images.append(face_array)
    return face_images


def highlight_faces(image, detector):
    # display image
    plt.imshow(image)

    ax = plt.gca()

    faces = detector.detect_faces(image)

    # for each face, draw a rectangle based on coordinates
    for face in faces:
        x, y, width, height = face['box']
        face_border = Rectangle((x, y), width, height,
                                fill=False, color='red')
        ax.add_patch(face_border)
    plt.show()


def highlight_faces_bool(image, detector, boolean):
    # display image
    plt.imshow(image)

    ax = plt.gca()

    faces = detector.detect_faces(image)

    # for each face, draw a rectangle based on coordinates
    for face, pete in zip(faces, boolean):
        x, y, width, height = face['box']
        face_border = Rectangle((x, y), width, height,
                                fill=False, color='red' if pete is False else 'green')
        ax.add_patch(face_border)
    plt.axis('off')
    #plt.show()
    return plt


def get_model_scores(faces):
    samples = asarray(faces, 'float32')

    # prepare the data for the model
    samples = preprocess_input(samples, version=2)

    # create a vggface model object
    model = VGGFace(model='resnet50',
                    include_top=False,
                    input_shape=(224, 224, 3),
                    pooling='avg')

    # perform prediction
    return model.predict(samples)


def find_pete(petes, img, detector):
    faces = extract_face_from_image(img, detector)

    model_scores_pete = get_model_scores(petes)
    model_scores_image = get_model_scores(faces)

    pete_bool = []

    for idx, face_score_1 in enumerate(model_scores_image):
        foundpete = False
        for idy, face_score_2 in enumerate(model_scores_pete):
            score = cosine(face_score_1, face_score_2)
            if score <= 0.4:
                foundpete = True
        pete_bool.append(foundpete)

    return pete_bool
