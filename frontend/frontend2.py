import os
from pathlib import Path
from uuid import uuid4

import requests
import streamlit as st
from PIL import Image


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
APPLICATION_FILE = DATA_DIR / "job_application.txt"
UPLOAD_DIR = DATA_DIR / "job_application_uploads"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8001")

st.set_page_config(page_title="Job Application", page_icon="📝")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


def save_upload(upload) -> str | None:
    if upload is None:
        return None

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    suffix = Path(upload.name).suffix.lower() or ".bin"
    saved_name = f"{uuid4().hex}{suffix}"
    (UPLOAD_DIR / saved_name).write_bytes(upload.getvalue())
    return saved_name


st.title("Welcome to Job Application")
st.caption(
    "Applications and uploaded files are stored on this computer only. "
    "This app does not automatically send them to a company or Google."
)

name = st.text_input("Enter Your Name")
prn = st.text_input("Enter Your PRN")
email = st.text_input("Enter Your Email")
passout_date = st.date_input("Enter your passout date")

gender = st.radio(
    "Select your Gender",
    ["Male", "Female", "Don't want to disclose"],
)

resume = st.file_uploader("Upload your resume", type=["pdf"])
if resume:
    st.success(f"Uploaded: {resume.name}")

agree = st.checkbox("I Agree that I have provided correct data")

photo = st.camera_input("Take a picture")
if photo:
    st.image(photo, caption="Camera Picture")

profile = st.file_uploader(
    "Upload your profile picture",
    type=["png", "jpeg", "jpg"],
)
if profile:
    try:
        image = Image.open(profile)
        st.image(
            image,
            caption="Uploaded Profile Picture",
            use_container_width=True,
        )
    except OSError as error:
        st.error(f"Could not read the uploaded profile picture: {error}")

video = st.file_uploader(
    "Upload a video",
    type=["mp4", "mov", "webm"],
)
if video:
    st.video(video)

if st.button("Submit", type="primary"):
    errors = []
    if not name.strip():
        errors.append("Enter your name.")
    if not prn.strip():
        errors.append("Enter your PRN.")
    if not email.strip() or "@" not in email:
        errors.append("Enter a valid email address.")
    if not agree:
        errors.append("Please confirm that your information is correct.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        try:
            saved_assets = {
                "Resume": save_upload(resume),
                "Live photo": save_upload(photo),
                "Profile picture": save_upload(profile),
                "Video": save_upload(video),
            }

            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with APPLICATION_FILE.open("a", encoding="utf-8") as file:
                file.write("\n========== JOB APPLICATION ==========\n")
                file.write(f"Name: {name.strip()}\n")
                file.write(f"PRN: {prn.strip()}\n")
                file.write(f"Email: {email.strip()}\n")
                file.write(f"Passout Date: {passout_date}\n")
                file.write(f"Gender: {gender}\n")
                file.write(f"Agreement: {agree}\n")
                for label, saved_name in saved_assets.items():
                    if saved_name:
                        file.write(f"{label}: {saved_name}\n")
                file.write("=====================================\n")
        except OSError as error:
            st.error(f"Could not save your application locally: {error}")
        else:
            st.success("Your application data has been saved successfully!")

if st.button("View Saved Applications"):
    try:
        data = APPLICATION_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        st.info("No applications have been saved yet.")
    except OSError as error:
        st.error(f"Could not read saved applications: {error}")
    else:
        st.text_area("Application Details", data, height=400)

st.divider()
st.subheader("Placement Assistant")
st.caption("Ask a question about placements or get help with this application.")
st.caption(
    "Chat messages are processed by the Gemini-backed assistant. "
    "Do not include sensitive personal details in chat."
)

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        if message.get("error"):
            st.error(message["content"])
        else:
            st.markdown(message["content"])

with st.form("placement_chat", clear_on_submit=True):
    prompt = st.text_input(
        "Your question",
        placeholder="Ask a question...",
        label_visibility="collapsed",
    )
    send = st.form_submit_button("Send")

if send:
    question = prompt.strip()
    if not question:
        st.warning("Enter a question before sending.")
    else:
        st.session_state.chat_messages.append(
            {"role": "user", "content": question}
        )
        try:
            with st.spinner("Getting a response..."):
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"prompt": question},
                    timeout=120,
                )
                response.raise_for_status()
                payload = response.json()

            if not isinstance(payload, dict) or not isinstance(
                payload.get("response"), str
            ):
                raise ValueError("The assistant returned an unexpected response.")

            assistant_message = {
                "role": "assistant",
                "content": payload["response"],
            }
        except requests.RequestException as error:
            assistant_message = {
                "role": "assistant",
                "content": f"Could not reach the assistant backend: {error}",
                "error": True,
            }
        except ValueError as error:
            assistant_message = {
                "role": "assistant",
                "content": str(error),
                "error": True,
            }

        st.session_state.chat_messages.append(assistant_message)
        st.rerun()
