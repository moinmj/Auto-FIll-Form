import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Smart Form AI", layout="centered")

st.title("🤖 Smart Form AI")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "chatbot_flow" not in st.session_state:
    st.session_state.chatbot_flow = []

if "decisions" not in st.session_state:
    st.session_state.decisions = []

if "url" not in st.session_state:
    st.session_state.url = ""

if "processed" not in st.session_state:   # 🔥 THIS WAS MISSING
    st.session_state.processed = False

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader("🔗 Enter Form URL")
url = st.text_input("Form URL", value=st.session_state.url)

st.subheader("📄 Upload Document (Optional)")
uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

# -----------------------------
# START PROCESSING
# -----------------------------
if st.button("🚀 Start Processing"):

    if not url:
        st.warning("Please enter a valid URL")
    else:
        with st.spinner("Analyzing form..."):

            st.session_state.url = url

            files = None
            data = {"url": url}

            if uploaded_file:
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue())
                }

            files = []

            # Add URL as form field
            files.append(("url", (None, url)))

            # Add file if exists
            if uploaded_file:
                files.append(
                    ("file", (uploaded_file.name, uploaded_file.getvalue(), "image/png"))
                )

            response = requests.post(
                "http://127.0.0.1:8000/smart-autofill",
                files=files
            )

            print("STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)

            if response.status_code == 200:
                result = response.json()
            else:
                st.error(f"Backend Error: {response.text}")
                st.stop()

            # 🔥 STORE EVERYTHING
            st.session_state.chatbot_flow = result.get("chatbot_flow", [])
            st.session_state.decisions = result.get("decisions", [])
            st.session_state.processed = True   # 🔥 IMPORTANT

            st.success("✅ Processing Complete!")

# -----------------------------
# DISPLAY CHATBOT FLOW
# -----------------------------
if st.session_state.processed and st.session_state.chatbot_flow:

    st.subheader("💬 Questions")

    user_responses = {}

    for item in st.session_state.chatbot_flow:

        if item["type"] == "document_prompt":
            st.info(item["message"])

        elif item["type"] == "input":
            user_responses[item["field"]] = st.text_input(
                item["message"],
                key=item["field"]
            )

        elif item["type"] == "choice":
            user_responses[item["field"]] = st.selectbox(
                item["message"],
                item["options"],
                key=item["field"]
            )

        elif item["type"] == "file_upload":
            st.warning(item["message"])
            st.file_uploader(
                f"Upload for {item['field']}",
                key=f"file_{item['field']}"
            )

    # -----------------------------
    # SUBMIT RESPONSES
    # -----------------------------
    if st.button("✅ Submit Answers"):

        with st.spinner("Filling form..."):

            try:
                submit_response = requests.post(
                    "http://127.0.0.1:8000/submit-responses",
                    json={
                        "url": st.session_state.url,
                        "decisions": st.session_state.decisions,
                        "user_responses": user_responses
                    }
                )

                submit_result = submit_response.json()

                st.success("🎉 Form Autofilled Successfully!")

                st.subheader("📦 Final Payload")
                st.json(submit_result.get("final_payload", {}))

            except Exception as e:
                st.error(f"Submission Error: {e}")