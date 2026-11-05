import streamlit as st
import numpy as np
import librosa
import io
from resemblyzer import VoiceEncoder, preprocess_wav

@st.cache_resource
def load_VoiceEncoder() :
    return VoiceEncoder()

def get_voice_embeddings(audio_bytes) :
    try :
        # load encoder
        encoder = load_VoiceEncoder()

        # process audio
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()
    except Exception as err :
        print("Error in getting voice embeddings :", err)
        return None

def identify_speaker(embedding, student_dict, threshold=0.65) :
    try :
        if embedding is None or not student_dict :
            return None, -1

        best_id = None
        best_score = -1

        embedding = np.asarray(embedding)

        # evaluate over every stud (id, embedding)
        for stud_id, stud_embedding in student_dict.items() :
            if stud_embedding is None :
                continue

            stud_embedding = np.asarray(stud_embedding)
            if stud_embedding.size == 0 :
                continue

            # evaluate curr student embedding with given embedding
            similarity_score = np.dot(embedding, stud_embedding)
            if similarity_score > best_score :
                best_score = similarity_score
                best_id = stud_id

        # no student embedding matched
        if not best_id or best_score < threshold :
            return None, -1

        return best_id, best_score
    except Exception as err :
        print("Error in identfying speaker :", err)
        return None, -1

def process_bulk_audio(audio_bytes, student_dict, threshold=0.65) :
    try :
        # load encoder
        encoder = load_VoiceEncoder()

        # get audio and split into segments ---> (non silent parts)
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_students = {}
        # process over every audio segment
        for start, end in segments :
            # very low voice --> skip
            if (end-start) < sr * 0.5 :
                continue

            # get the curr audio segment --> preprocess --> embeddings
            audio_segment = audio[start:end]
            wav = preprocess_wav(audio_segment)
            embedding = encoder.embed_utterance(wav)

            # find student with matching embedding and evaluate
            stud_id, score = identify_speaker(embedding, student_dict, threshold)
            if stud_id :
                if stud_id not in identified_students or identified_students[stud_id] < score :
                    identified_students[stud_id] = score

        return identified_students
    except Exception as err :
        print("Error in processing bulk audio :", err)
        return None

