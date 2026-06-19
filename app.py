import streamlit as st
from pipeline import run_research_pipeline
from docx import Document
from io import BytesIO
import json
import os

def create_word_file(topic, report, feedback):

    doc = Document()

    doc.add_heading("InfoBot Research Report", level=1)

    doc.add_heading("Research Report", level=2)
    doc.add_paragraph(report)

    doc.add_page_break()

    doc.add_heading("Critic Review", level=2)
    doc.add_paragraph(feedback)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="InfoBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------
# LOAD HISTORY
# ----------------------------------------

if "history" not in st.session_state:

    if os.path.exists("data/history.json"):

        with open(
            "data/history.json",
            "r",
            encoding="utf-8"
        ) as f:

            st.session_state.history = json.load(f)

    else:

        st.session_state.history = []

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0F172A, #111827);
}

/* Remove Streamlit Branding Space */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hero Title */
.hero-title {
    font-size: 4rem;
    font-weight: 800;
    text-align: center;
    color: white;
    margin-bottom: 0;
}

.hero-subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(12px);
}

/* Section Headings */
.section-title {
    color: white;
    font-size: 1.3rem;
    font-weight: 700;
}

/* Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

.metric-title {
    color: #94A3B8;
    font-size: 0.9rem;
}

.metric-value {
    color: white;
    font-size: 1.4rem;
    font-weight: 700;
}

/* Report Box */
.report-box {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Footer */
.footer {
    text-align:center;
    color:#64748B;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# SIDEBAR
# ----------------------------------------

with st.sidebar:

    st.title("🤖 InfoBot")

    st.divider()

    if st.button(
        "➕ New Research",
        use_container_width=True
    ):

        st.session_state.selected_chat = None
        st.rerun()

    st.divider()

    st.subheader("History")

    if not st.session_state.history:

        st.caption("No research history yet")

    else:

        for idx, item in enumerate(
            reversed(st.session_state.history)
        ):

            if st.button(
                f"📄 {item['topic'][:30]}",
                key=f"history_{idx}",
                use_container_width=True
            ):

                st.session_state.selected_chat = item
                st.rerun()

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    """
    <div class="hero-title">
        🤖 InfoBot
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        AI-Powered Multi-Agent Research Assistant
        <br>
        Tavily • Hyperbrowser • Mistral AI
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Search Engine</div>
        <div class="metric-value">🔎 Tavily</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Web Intelligence</div>
        <div class="metric-value">🌐 Hyperbrowser</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Reasoning Model</div>
        <div class="metric-value">🧠 Mistral AI</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown(
    """
    <div class="section-title">
        Research Topic
    </div>
    """,
    unsafe_allow_html=True
)

topic = st.text_input(
    "",
    placeholder="e.g. Future of Agentic AI, Quantum Computing, Electric Vehicles..."
)

generate = st.button(
    "🚀 Generate Research Report",
    use_container_width=True
)

# --------------------------------------------------
# PIPELINE EXECUTION
# --------------------------------------------------

if generate:

    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    progress = st.progress(0)

    status = st.empty()

    status.info("🔎 Searching trusted sources...")
    progress.progress(20)

    result = run_research_pipeline(topic)

    progress.progress(50)
    status.info("🌐 Extracting information...")

    progress.progress(75)
    status.info("🧠 Generating report...")

    progress.progress(100)
    status.success("✅ Research completed successfully!")

    report = result.get("report", "")
    feedback = result.get("feedback", "")

    new_entry = {
    "topic": topic,
    "report": report,
    "feedback": feedback
}

    if not any(
        item["topic"] == topic
        for item in st.session_state.history
    ):

        st.session_state.history.append(
            new_entry
    )

    with open(
        "data/history.json",
        "w",
         encoding="utf-8"
    ) as f:

        json.dump(
            st.session_state.history,
            f,
            indent=4
    )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(
        [
            "📄 Research Report",
            "🧠 Critic Review"
        ]
    )

    with tab1:

        st.markdown(
            """
            <div class="section-title">
                Research Report
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(report)

        word_file = create_word_file(
            topic,
            report,
            feedback
)

        st.download_button(
            label="📄 Download Word Report",
            data=word_file,
            file_name="InfoBot_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

    with tab2:

        st.markdown(
            """
            <div class="section-title">
                Critic Review
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(feedback)

# ----------------------------------------
# VIEW PREVIOUS CHAT
# ----------------------------------------

if st.session_state.selected_chat:

    old = st.session_state.selected_chat

    st.divider()

    st.markdown(
        f"## 📂 {old['topic']}"
    )

    tab1, tab2 = st.tabs(
        [
            "📄 Research Report",
            "🧠 Critic Review"
        ]
    )

    with tab1:

        st.markdown(
            old["report"]
        )

    with tab2:

        st.markdown(
            old["feedback"]
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Built with ❤️ using Tavily, Hyperbrowser and Mistral AI
    </div>
    """,
    unsafe_allow_html=True
)