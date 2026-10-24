import streamlit as st
import numpy as np
import dlib
import face_recognition_models
from sklearn.svm import SVC

from src.db.controllers.student import get_all_students

@st.cache_resource
def load_dlib_models() :
    face_detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    face_recognizer = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return [face_detector, shape_predictor, face_recognizer]

def get_face_embeddings(face_np) :
    dlib_models = load_dlib_models()
    faces = dlib_models[0](face_np, 1)

    encodings = []
    for face in faces :
        shape = dlib_models[1](face_np, face)
        face_encoding = dlib_models[2].compute_face_descriptor(face_np, shape, 1)
        encodings.append(np.array(face_encoding))

    return encodings

@st.cache_resource
def get_trained_model() :
    X = []
    Y = []

    students = get_all_students()
    if not students :
        return None

    for student in students :
        embeddings = student["face_embeddings"]
        id = student["student_id"]
        if embeddings :
            X.append(embeddings)
            Y.append(id)

    if len(X) == 0 :
        print("No studnets to train face recognition model")
        return None

    model = SVC(kernel="linear", probability=True, class_weight="balanced")
    try :
        model.fit(X, Y)
    except ValueError as err :
        print(err)

    model_data = {
        "model" : model,
        "X" : X,
        "Y" : Y
    }
    return model_data

def train_model() :
    st.session_state.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np, threshold=0.6) :
    embeddings = get_face_embeddings(class_image_np)
    model_data = get_trained_model()
    if not model_data :
        return None, None, len(embeddings)

    model = model_data["model"]
    X = model_data["X"]
    Y = model_data["Y"]
    student_ids = sorted(list(set(Y)))

    present_student = set()
    for embedding in embeddings :
        predicted_id = model.predict(embedding)
        student_embedding = X[Y.index(predicted_id)]

        loss = np.linalg.norm(student_embedding - embedding)
        if loss <= threshold :
            present_student.add(predicted_id)

    return present_student, student_ids, len(embeddings)

