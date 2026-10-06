import ollama
import streamlit as st
import pandas as pd

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Complaint Categorizer",
    page_icon="🤖"
)


# ---------------- SESSION STATE ----------------

if "complaints" not in st.session_state:
    st.session_state.complaints = []


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ Complaint Settings")

    uploaded_file = st.file_uploader(
        "📎 Upload Complaint File",
        type=["txt"]
    )

    if uploaded_file:

        st.success("File uploaded successfully! ✅")

        if st.button("Read File"):

            try:

                context = uploaded_file.read().decode("utf-8")

                st.subheader("📄 File Content")

                st.text(context)

            except:

                st.error("Error reading file")


    st.markdown("---")

    if st.button("🗑️ Clear All Complaints"):

        st.session_state.complaints = []

        st.success("All complaints cleared! ✅")


# ---------------- TITLE ----------------

st.title("🤖 AI Complaint Categorizer")

st.write(
    "Submit your college complaint and AI will "
    "categorize it and provide useful suggestions."
)


# ---------------- TABS ----------------

tab1, tab2 = st.tabs(
    ["📝 Submit Complaint", "📊 Complaint Dashboard"]
)


# ==================================================
# TAB 1 - SUBMIT COMPLAINT
# ==================================================

with tab1:

    st.subheader("📝 Submit Your Complaint")

    complaint = st.chat_input(
        "What is your complaint?"
    )


    if complaint:

        # Display user's complaint

        with st.chat_message("user"):

            st.write(complaint)


        # AI instructions

        system_prompt = """
You are an AI College Complaint Categorizer.

Analyze the student's complaint.

Choose ONE category from:

Library
Technical
Infrastructure
Lost and Found
Academic
Transport
Hostel
Security
Canteen
Fees
Other

Also identify:

Priority: Low, Medium, or High
Department
Summary
Suggested Action

Give the answer exactly in this format:

Category: 
Priority:
Department:
Summary:
Suggested Action:

Keep the answer simple.
"""


        # Ask Ollama

        with st.spinner("🤖 Analyzing complaint..."):

            response = ollama.chat(

                model="llama3.2:3b",

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt
                    },

                    {
                        "role": "user",
                        "content": complaint
                    }

                ]
            )


        # Get AI response

        answer = response["message"]["content"]


        # Display AI response

        with st.chat_message("assistant"):

            st.write(answer)


        # ---------------- GET CATEGORY ----------------

        category = "Other"

        for line in answer.split("\n"):

            if line.lower().startswith("category:"):

                category = line.split(":", 1)[1].strip()


        # ---------------- GET PRIORITY ----------------

        priority = "Medium"

        for line in answer.split("\n"):

            if line.lower().startswith("priority:"):

                priority = line.split(":", 1)[1].strip()


        # ---------------- GET DEPARTMENT ----------------

        department = "General Administration"

        for line in answer.split("\n"):

            if line.lower().startswith("department:"):

                department = line.split(":", 1)[1].strip()


        # ---------------- SAVE COMPLAINT ----------------

        st.session_state.complaints.append(

            {
                "Complaint": complaint,
                "Category": category,
                "Priority": priority,
                "Department": department,
                "AI Response": answer
            }

        )


        st.success("✅ Complaint added to dashboard!")


# ==================================================
# TAB 2 - DASHBOARD
# ==================================================

with tab2:

    st.subheader("📊 Complaint Dashboard")


    # ---------------- TOTAL COMPLAINTS ----------------

    total = len(st.session_state.complaints)


    st.metric(
        "Total Complaints",
        total
    )


    # ---------------- CATEGORY COUNT ----------------

    if total > 0:

        data = pd.DataFrame(
            st.session_state.complaints
        )


        st.subheader("📂 Complaints by Category")


        category_count = (
            data["Category"]
            .value_counts()
        )


        # Display category numbers

        for category, count in category_count.items():

            st.write(
                f"### 📌 {category}: {count}"
            )


        # ---------------- CHART ----------------

        st.bar_chart(category_count)


        # ---------------- ALL COMPLAINTS ----------------

        st.subheader("📋 All Complaints")


        st.dataframe(

            data[
                [
                    "Complaint",
                    "Category",
                    "Priority",
                    "Department"
                ]
            ],

            use_container_width=True

        )


    else:

        st.info(
            "No complaints submitted yet."
        )