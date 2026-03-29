import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="AI Data Intelligence Hub", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Premium CSS Styling
st.markdown("""
<style>
    /* Global Font and Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }

    /* Custom Header Banner */
    .premium-header {
        background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%);
        padding: 40px 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    
    .premium-header h1 {
        font-weight: 800;
        margin-bottom: 0;
        font-size: 3.5rem;
        color: #ffffff;
    }
    
    .premium-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 600;
        margin-top: 10px;
    }

    /* Card Styling */
    div.stExpander {
        background: #161b22;
        border: 1px solid #30363d !important;
        border-radius: 10px;
        overflow: hidden;
    }
    div.stExpander > div:first-child p {
        font-size: 1.1rem;
        font-weight: 600;
        color: #58a6ff;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
        transition: transform 0.2s;
        font-weight: 600;
        border-radius: 8px;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        background: linear-gradient(90deg, #2ea043, #3fb950);
        color: white;
    }

    /* Input Fields */
    .stTextInput input, .stFileUploader {
        background-color: #0d1117 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 8px;
    }
    
    [data-testid="stHeader"] {
        background: rgba(13, 17, 23, 0); 
    }
</style>
""", unsafe_allow_html=True)

# 3. Dynamic Header
st.markdown("""
<div class="premium-header">
    <h1>⚡ AI Pipeline & Career Hub</h1>
    <p>Live Kafka Streaming • Vector Context • LLM Multi-Agent System</p>
</div>
""", unsafe_allow_html=True)

api_url = "http://localhost:8001"

# 4. Content Tabs
tab1, tab2 = st.tabs(["🌎 Market Intelligence", "🎯 Smart Resume Matcher"])

# -----------------
# TAB 1: Market
# -----------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🤖 Ask the Autonomous Agents")
    st.caption("Ask questions about real-time job market trends. The query routes through specialized Retrieval, Analysis, and Formatting agents.")
    
    user_question = st.text_input("Enter your research query:", placeholder="e.g. What are the best skills to learn for a Data Engineer today?")
    
    if st.button("Generate Executive Insights", use_container_width=True):
        if user_question.strip():
            with st.spinner("🤖 Agents are securely retrieving & analyzing Kafka stream data..."):
                try:
                    res = requests.post(f"{api_url}/analyze", json={"question": user_question}, timeout=45)
                    if res.status_code == 200:
                        st.success("✅ Multi-Agent Consensus Reached")
                        with st.container(border=True):
                            st.markdown(res.json()["report"])
                    else:
                        st.error("Server synchronization error.")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")

# -----------------
# TAB 2: Resume Match
# -----------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏹 Unlock Hidden Opportunities")
    st.caption("Upload your resume. The AI will chunk it, embed it, and find the perfect match in the live datastream before generating specific ATS tweaks.")
    
    st.markdown("---")
    
    col_left, col_right = st.columns([1, 1.8], gap="large")
    
    with col_left:
        st.subheader("1. Your Profile")
        location = st.text_input("📍 Preferred Location Filter", placeholder="e.g., San Francisco, Noida, Remote")
        
        st.markdown("<br>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("📄 Upload PDF Resume", type="pdf", help="Your data remains strictly localized.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if uploaded_file and st.button("🚀 Analyze & Find Matches", use_container_width=True):
            with st.spinner("Chunking Document & Generating Embeddings..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                res_upload = requests.post(f"{api_url}/upload_resume", files=files)
                
                if res_upload.status_code == 200:
                    resume_text = res_upload.json()["resume_text"]
                    st.session_state["resume_text"] = resume_text
                    
                    match_payload = {
                        "resume_text": resume_text,
                        "location_filter": location.strip() if location else None,
                        "k": 5
                    }
                    res_match = requests.post(f"{api_url}/match_jobs", json=match_payload)
                    if res_match.status_code == 200:
                        st.session_state["matches"] = res_match.json()["matches"]
                        st.success("Resume vectorization complete!")
                    else:
                        st.error("Error matching jobs.")
                else:
                    st.error("Error breaking down PDF.")

    with col_right:
        st.subheader("2. AI Copilot Recommendations")
        if "matches" in st.session_state and st.session_state["matches"]:
            for idx, job in enumerate(st.session_state["matches"]):
                meta = job.get('metadata', {})
                title = meta.get('title', 'Position')
                company = meta.get('company', 'Company')
                loc = meta.get('location', 'Location')
                
                with st.expander(f"💼 {title} at {company} 📍 {loc}", expanded=(idx==0)):
                    st.markdown("**Original Description Extract:**")
                    st.info(f'"{job.get("page_content", "")}"')
                    
                    if st.button(f"✨ Generate Targeted Tweaks", key=f"opt_btn_{idx}", help="Run the LLM optimization pipeline on this specific role"):
                        with st.spinner("🤖 Computing gap analysis..."):
                            payload = {
                                "resume_text": st.session_state["resume_text"],
                                "job_description": job['page_content']
                            }
                            res_opt = requests.post(f"{api_url}/optimize_resume", json=payload)
                            
                            if res_opt.status_code == 200:
                                st.markdown("---")
                                st.markdown("### 🏆 Expert Optimization Report")
                                st.markdown(res_opt.json()["suggestions"])
                            else:
                                st.error("Failed to generate optimization report.")
        elif "matches" not in st.session_state:
            st.info("👈 Upload your resume and start the analysis.")
        else:
            st.warning("No active jobs found matching those exact conditions.")
