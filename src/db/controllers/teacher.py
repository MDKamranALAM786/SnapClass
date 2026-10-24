from src.db.config.config import supabase
import bcrypt

def hash_password(password) :
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def compare_password(password, hashed_password) :
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def teacher_exists(username) :
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data)

def register_teacher(name, username, password) :
    try :
        if teacher_exists(username) :
            return "User already exists!", None
        
        hashed_password = hash_password(password)
        data = {
            "name" : name,
            "username" : username,
            "password" : hashed_password
        }
        response = supabase.table("teachers").insert(data).execute()
        print("Response :", response)
        print("Data :", response.data)

        message = "User Created!"
        print(message)
        return message, response.data
    except Exception as err :
        print(err)
        return "Unexpeted Error!", None

def login_teacher(username, password) :
    try :
        response = supabase.table("teachers").select("*").eq("username", username).execute()
        print("Response :", response)
        print("Data :", response.data)
        if not response.data :
            message = "User not found!"
            print(message)
            return message, None
    
        teacher = response.data[0]
        if not compare_password(password, teacher["password"]) :
            message = "Incorrect Password!"
            print(message)
            return message, None
    
        message = "Login Successful!"
        print(message)
        return message, teacher
    except Exception as err :
        print(err)
        return "Unexpected Error", None

