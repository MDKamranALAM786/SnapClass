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

def is_student_enrolled(student_id, subject_id) :
    try :
        response = supabase.table("subject_students").select("*").eq("subject_id", subject_id).eq("student_id", student_id).execute()
        return True if response.data else False
    except Exception as err :
        print("Error in finding student enrolled :", err)
        return False

def enroll_student_into_subject(student_id, subject_id) :
    try :
        data = {"student_id" : student_id, "subject_id" : subject_id}
        response = supabase.table("subject_students").insert(data).execute()
        return response.data
    except Exception as err :
        print("Error in enrolling student into subject :", err)
        return None

def unenroll_student_from_subject(student_id, subject_id) :
    try :
        response = supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
        return response.data
    except Exception as err :
        print("Error in unenrolling student from subject :", err)
        return None

def get_student_subjects(student_id) :
    try :
        response = supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
        return response.data
    except Exception as err :
        print("Error in getting student subjects :", err)
        return None

def get_student_attendance(student_id) :
    try :
        response = supabase.table("attendance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
        return response.data
    except Exception as err :
        print("Error in getting student attendance :", err)
        return None

