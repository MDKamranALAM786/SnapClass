# AI Attendance System

A Streamlit-based attendance management app for students and teachers. The project combines face recognition, voice-based attendance, and a Supabase-backed database to simplify classroom attendance tracking.

## Project Overview

This application is designed for a classroom environment where:

- Teachers can create subjects, share join codes, manage students, and review attendance history.
- Students can log in using face recognition and enroll in subjects.
- Attendance can be taken by uploading class photos or using voice recognition.
- Data is stored in Supabase for persistence and reporting.

The app is named Snap Class in the UI and is built around a student/teacher flow managed by Streamlit session state.

## Features

- Student login with face-based authentication
- Teacher login and registration
- Subject creation and sharing
- Join-code enrollment flow
- Photo-based attendance analysis
- Optional voice attendance
- Attendance records and summaries
- Student subject dashboard with enrollment and attendance history

## Tech Stack

- Python
- Streamlit
- NumPy
- Pandas
- OpenCV-compatible image processing
- Face recognition models
- Voice recognition using audio embeddings
- Supabase database

## Project Structure

```text
AI Attendance System/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── secrets.toml
├── src/
│   ├── components/
│   ├── db/
│   ├── pages/
│   ├── pipelines/
│   └── ui/
└── venv/
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- pip
- Git
- A Supabase project with valid credentials
- Windows users may need Visual Studio C++ Build Tools if `dlib` fails to compile

## Configuration

The app reads Supabase credentials from `.streamlit/secrets.toml`.

Example:

```toml
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_key"
```

If you are using a different Supabase project, replace the values in the existing file or create your own local `secrets.toml` file in the `.streamlit` folder.

## Installation

1. Clone the repo:

```bash
git clone <repository-url>
cd "AI Attendance System"
```

2. Create and activate a virtual environment:

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Run the App

From the project root:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Usage

### Teacher Flow

- Open the app and choose Teacher.
- Register or log in.
- Create a subject and share its code.
- Add photos or use voice attendance to mark presence.
- View attendance summaries.

### Student Flow

- Open the app and choose Student.
- Log in using face recognition.
- Register a profile if needed.
- Enroll in subjects and view your attendance records.

## Notes

- This project relies on AI pipelines for real-time face recognition and voice embedding creation.
- For production deployment, consider securing the Supabase keys and adding environment-specific configuration.
- Attendance accuracy depends on good lighting, camera quality, and clean subject enrollment data.

## License

This project is provided for educational and demonstration purposes.
