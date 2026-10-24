from src.db.config.config import supabase

def get_all_students() :
    try :
        response = supabase.table("students").select("*").execute()
        if response.data :
            return response.data
        else :
            print("No student found!")
            return None
    except Exception as err :
        print("Error in getting all students :", err)
        return None

def get_student(stud_id) :
    try :
        response = supabase.table("students").select("*").eq("student_id", stud_id).execute()
        if response.data :
            return response.data[0]
        else :
            print("No student found!")
            return None
    except Exception as err :
        print("Error in finding student :", err)
        return None

def register_student(name, face_embedding=None, voice_embedding=None) :
    try :
        data = {
            "name" : name,
            "face_embedding" : face_embedding,
            "voice_embedding" : voice_embedding
        }
        response = supabase.table("students").insert(data).execute()

        student = None
        if response.data :
            print("Student registered!")
            student = response.data[0]

        return student
    except Exception as err :
        print("Error in registering student :", err)
        return None

