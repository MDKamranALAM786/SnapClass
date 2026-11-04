from src.db.config.config import supabase

def create_new_subject(sub_code, sub_name, sub_section, teacher_id) :
    try :
        data = {"name" : sub_name, "subject_code" : sub_code, "section" : sub_section, "teacher_id" : teacher_id}
        response = supabase.table("subjects").insert(data).execute()
        print(f"Created Subject : {response.data}")
        return response.data
    except Exception as err :
        print(f"Error in creating subject : {err}")
        return None

def get_all_subjects(teacher_id) :
    try :
        response = supabase.table("subjects").select("*, subject_students(count), attendance_logs(time)").eq("teacher_id", teacher_id).execute()
        subjects = response.data

        print(subjects)

        for subject in subjects :
            subject["total_students"] = subject.get("subjects_students", [{}])[0].get("count", 0) if subject.get("subject_students") else 0

            attendance = subject.get("attendance_logs", [])
            subject["total_classes"] = len(set(log["time"] for log in attendance))

            subject.pop("subject_students", None)
            subject.pop("attendance_logs", None)

        return subjects
    except Exception as err :
        print(f"Error in getting all subjects : {err}")
        return None

def get_subject(subject_code) :
    try :
        response = supabase.table("subjects").select("subject_id, name, subject_code").eq("subject_code", subject_code).execute()
        return response.data[0] if response.data else None
    except Exception as err :
        print("Error in getting subject :", err)
        return None

