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
        print(err)
        return None

