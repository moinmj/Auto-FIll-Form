# 🤖 Smart Form AI

An **AI-powered universal form automation system** that can analyze, understand, and automatically fill web forms using **Selenium, OCR, and LLMs**.

---

## 🚀 Overview

Smart Form AI is designed to automate the entire form-filling process:

* 🔍 Extracts form fields dynamically from any website
* 🧠 Understands field meaning using AI (LLM + rules)
* 📄 Extracts user data from documents (OCR + LLM)
* 💬 Interacts with users to collect missing information
* ⚡ Automatically fills forms in a real browser

---

## 🧠 How It Works

```
Form URL
   ↓
Selenium → Extract fields
   ↓
LLM + Rules → Map labels (name, email, phone…)
   ↓
OCR + LLM → Extract document data
   ↓
Decision Engine → Decide actions
   ↓
Chatbot Flow → Ask missing info
   ↓
Final Payload
   ↓
Selenium → Auto-fill form
```

---

## ✨ Features

* ✅ Works on **any form (dynamic or static)**
* 🤖 AI-powered **field understanding**
* 📄 Document parsing using **OCR (Tesseract)**
* 💬 Smart chatbot interaction for missing fields
* ⚡ Real-time **browser automation (Selenium)**
* 🔁 Hybrid system (Rules + LLM for accuracy)

---

## 🛠️ Tech Stack

| Category   | Technology    |
| ---------- | ------------- |
| Backend    | FastAPI       |
| Frontend   | Streamlit     |
| Automation | Selenium      |
| OCR        | Tesseract     |
| AI/LLM     | Groq (LLaMA3) |
| Parsing    | BeautifulSoup |

---

## 📂 Project Structure

```
Smart-Form-AI/
│
├── app/
│   ├── routes/
│   │   └── form_routes.py
│   ├── services/
│   │   ├── form_analyzer.py
│   │   ├── form_filler.py
│   │   ├── decision_engine.py
│   │   └── chatbot_engine.py
│   ├── ml/
│   │   ├── document_parser.py
│   │   └── field_mapper.py
│   └── main.py
│
├── frontend/
│   └── streamlit_app.py
│
├── tests/
│   ├── test_ocr.py
│   └── test_llm.py
│
├── run.py
└── requirements.txt
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/smart-form-ai.git
cd smart-form-ai
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 5️⃣ Install Tesseract OCR

Download and install from:
https://github.com/tesseract-ocr/tesseract

Then update path in code:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

### 6️⃣ Run Backend

```bash
python run.py
```

Open:

```
http://127.0.0.1:8000/docs
```

---

### 7️⃣ Run Frontend (Optional)

```bash
streamlit run frontend/streamlit_app.py
```

---

## 🧪 Usage

### 🔹 Analyze Form

```
GET /analyze-form
```

---

### 🔹 Smart Autofill (AI Flow)

```
POST /smart-autofill
```

---

### 🔹 Upload Document

```
POST /upload-document
```

---

### 🔹 Autofill Browser

```
POST /auto-fill-browser
```

Example request:

```json
{
  "url": "https://httpbin.org/forms/post",
  "payload": {
    "custname": "Moin Jan Rashid",
    "custtel": "9876543210",
    "custemail": "moin@example.com",
    "delivery": "18:30",
    "size": "Medium",
    "topping": "Bacon"
  }
}
```

---

## 📸 Demo

* Form extraction ✔️
* AI field mapping ✔️
* Chat-based interaction ✔️
* Auto-filled browser ✔️

---

## 🔥 Future Enhancements

* ✅ Auto-submit forms
* 📊 Confidence scoring for extracted data
* 🧠 User profile memory
* 📄 Multi-page form support
* 🌐 Chrome extension integration

---

## 🎯 Key Highlights

* Works without predefined templates
* Combines **AI + automation**
* Handles real-world noisy data (OCR)
* Fully dynamic system

---

## 👨‍💻 Author

**Moin Jan Rashid**

---

## ⭐ Contribute

Contributions are welcome! Feel free to fork and improve.

---

## 📜 License

This project is licensed under the MIT License.
