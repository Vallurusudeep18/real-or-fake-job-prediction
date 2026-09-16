import streamlit as st
import joblib
import re
from fpdf import FPDF

# Load model and vectorizer
model = joblib.load("fake_job_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Page settings
st.set_page_config(
    page_title="AI Fake Job Detection System",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("📋 Project Details")

st.sidebar.markdown("""
### 🤖 Machine Learning Model
Logistic Regression

### 📄 Vectorizer
TF-IDF

### 📚 Dataset
Kaggle Fake Job Postings

### 🎯 Purpose
Detect Fake Job Advertisements
""")

st.sidebar.markdown("---")

st.sidebar.success("Version 2.1")

# Title
st.title("🕵️ AI Fake Job Posting Detection System")

st.markdown("""
### Detect whether a job advertisement is **REAL** or **FAKE**

Paste the complete job description below and click **Analyze Job Posting**.
""")

# Text input
job_text = st.text_area(
    "📄 Paste Job Description",
    height=300,
    placeholder="Paste the complete job description here..."
)
# Suspicious keywords
suspicious_words = [
    "registration fee",
    "pay fee",
    "bank details",
    "easy money",
    "guaranteed income",
    "no experience required",
    "instant joining",
    "earn money quickly",
    "whatsapp us",
    "security deposit"
]

# Predict button
predict = st.button(
    "🔍 Analyze Job Posting",
    use_container_width=True
)

if predict:

    if not job_text.strip():
        st.warning("Please enter a job description.")
    else:

        # ML Prediction

        X_input = vectorizer.transform([job_text])

        prediction = model.predict(X_input)[0]

        confidence = 0
        risk = 0

        if hasattr(model, "predict_proba"):

           proba = model.predict_proba(X_input)[0]

           if prediction == 0:
              confidence = proba[0] * 100
           else:
              confidence = proba[1] * 100

        # Base fraud risk comes from fake probability
           risk = proba[1] * 100

        # Check suspicious words
        found_words = []

        text_lower = job_text.lower()

        for word in suspicious_words:
            if word in text_lower:
                found_words.append(word)
        # Increase fraud risk based on suspicious keywords
        keyword_risk = {
            "registration fee": 30,
            "pay fee": 25,
            "security deposit": 25,
            "bank details": 20,
            "easy money": 20,
            "guaranteed income": 20,
            "earn money quickly": 20,
            "whatsapp us": 15,
            "no experience required": 10,
            "instant joining": 10
        }

        for word in found_words:
            risk += keyword_risk.get(word, 0)

        # Maximum fraud risk is 100%
        risk = min(risk, 100)
        

        # Results
        st.subheader("Prediction Result")

        if prediction == 0:
            
            if hasattr(model, "predict_proba"):
                st.success(
                    f"✅ REAL JOB\n\nConfidence: {confidence:.2f}%"
                )
            else:
                st.success("✅ REAL JOB")

        else:
            if hasattr(model, "predict_proba"):
                st.error(
                    f"⚠️ FAKE JOB\n\nConfidence: {confidence:.2f}%"
                )
            else:
                st.error("⚠️ FAKE JOB")
        st.subheader("📊 Prediction Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Confidence", f"{confidence:.2f}%")

        with col2:
            st.metric("Fraud Risk", f"{risk:.2f}%")

        st.subheader("🚨 Fraud Risk Meter")

        st.progress(min(risk / 100, 1.0))

        # Risk Level
        if risk < 30:
            st.success("🟢 Risk Level: LOW")
        elif risk < 70:
            st.warning("🟡 Risk Level: MEDIUM")
        else:
            st.error("🔴 Risk Level: HIGH")
        # Suspicious keyword section
        if found_words:
            st.warning("🚨 Suspicious phrases detected:")

            for word in found_words:
                st.write("•", word)

        st.subheader("📋 Job Information")
        # Extract Email
        email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', job_text)

        if email:
           st.write("📧 Email:", email[0])
        else:
           st.write("📧 Email: Not Found")
        # Email Verification
        if email:
           company_domains = [
           ".com", ".org", ".net", ".edu"
           ]

        public_domains = [
            "@gmail.com",
            "@yahoo.com",
            "@hotmail.com",
            "@outlook.com"
        ]

        email_address = email[0].lower()

        if any(domain in email_address for domain in public_domains):
           st.warning("⚠️ Public Email Address (Verify Carefully)")
        else:
           st.success("✅ Professional Company Email")
        # Extract Website
        website = re.findall(r'(https?://\S+|www\.\S+)', job_text)

        if website:
           st.write("🌐 Website:", website[0])
        else:
           st.write("🌐 Website: Not Found")
        # Extract Company Name
        company = re.search(r'Company\s*[:\-]\s*(.+)', job_text, re.IGNORECASE)

        if company:
           st.write("🏢 Company:", company.group(1))
        else:
           st.write("🏢 Company: Not Found")
        # Extract Location
        location = re.search(r'Location\s*[:\-]\s*(.+)', job_text, re.IGNORECASE)

        if location:
           st.write("📍 Location:", location.group(1))
        else:
           st.write("📍 Location: Not Found")
        # Extract Salary
        salary = re.search(r'Salary\s*[:\-]\s*(.+)', job_text, re.IGNORECASE)

        if salary:
           st.write("💰 Salary:", salary.group(1))
        else:
           st.write("💰 Salary: Not Found")
        # Salary Analysis
        if salary:

            salary_text = salary.group(1)

            numbers = re.findall(r'\d+', salary_text)

            if numbers:

                amount = int("".join(numbers))

                if amount >= 1000000:
                   st.error("⚠️ Very High Salary - Verify Carefully")

                elif amount >= 500000:
                   st.warning("🟡 High Salary")

                else:
                   st.success("✅ Salary Looks Reasonable")
        # Extract Experience
        experience = re.search(r'Experience\s*[:\-]\s*(.+)', job_text, re.IGNORECASE)

        if experience:
           st.write("👨‍💼 Experience:", experience.group(1))
        else:
           st.write("👨‍💼 Experience: Not Found")

        # Safety Tips
        st.subheader("Safety Tips")

        st.write("✔ Never pay registration fees.")
        st.write("✔ Verify company websites.")
        st.write("✔ Check recruiter email addresses.")
        st.write("✔ Be cautious of guaranteed income promises.")
        # ==========================
        # CREATE PDF REPORT
        # ==========================
        def clean_text(text):
            if text is None:
               return "Not Found"

            text = str(text)

            text = text.replace("₹", "Rs.")
            text = text.replace("–", "-")
            text = text.replace("—", "-")

            return text.encode("latin-1", "replace").decode("latin-1")
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "AI Fake Job Detection Report", ln=True, align="C")

        pdf.ln(10)

        pdf.set_font("Arial", size=12)

        result = "REAL JOB" if prediction == 0 else "FAKE JOB"

        pdf.cell(190, 10, f"Prediction : {result}", ln=True)
        pdf.cell(190, 10, f"Confidence : {confidence:.2f}%", ln=True)
        pdf.cell(190, 10, f"Fraud Risk : {risk:.2f}%", ln=True)
        company_text = company.group(1) if company else "Not Found"

        pdf.cell(
            190,
            10,
            clean_text(f"Company : {company_text}"),
            ln=True
        )
        pdf.cell(190, 10, f"Location : {location.group(1) if location else 'Not Found'}", ln=True)

        salary_text = salary.group(1) if salary else "Not Found"

        pdf.cell(
            190,
            10,
            clean_text(f"Salary : {salary_text}"),
            ln=True
        )
        pdf.cell(190, 10, f"Experience : {experience.group(1) if experience else 'Not Found'}", ln=True)


        pdf.cell(190, 10, f"Email : {email[0] if email else 'Not Found'}", ln=True)

        pdf.cell(190, 10, f"Website : {website[0] if website else 'Not Found'}", ln=True)
        pdf_output = bytes(pdf.output(dest="S"))

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_output,
            file_name="JobShield_AI_Report.pdf",
            mime="application/pdf"
        )