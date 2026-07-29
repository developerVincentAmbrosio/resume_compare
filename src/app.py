import streamlit as st
from engine import resume_analyzer

# Setup layout environment
st.set_page_config(layout="wide")

# Key configuration interface
with st.sidebar:
    st.header("Settings")
    api_key = st.secrets["OPENAI_API_KEY"]

# Dual column interface structure
col_input, col_output = st.columns(2, gap="large")

with col_input:
    st.subheader("Configuration Inputs")
    job_desc = st.text_area("Target Job Description", height=250, placeholder="Paste requirements here...")
    uploaded_files = st.file_uploader("Upload Resumes (PDF, DOCX or TXT file)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    analyze_btn = st.button("Run Evaluation", type="primary")

with col_output:
    st.subheader("Analysis Feedback")
    
    if analyze_btn:
        # Guard Clauses: Halt script early if fields are empty
        if "OPENAI_API_KEY" not in st.secrets:
            st.error("Please add your OpenAI API Key in the sidebar.")
            st.stop()
        if not job_desc.strip():
            st.warning("Please provide a Job Description.")
            st.stop()
        if not uploaded_files:
            st.warning("Please upload at least one resume file.")
            st.stop()

        # Execute data extraction pipeline
with col_output:
    st.subheader("Analysis Feedback")
    
    if analyze_btn:
        # Guard Clauses
        if "OPENAI_API_KEY" not in st.secrets:
            st.error("Please add your OpenAI API Key in the sidebar.")
            st.stop()
        if not job_desc.strip():
            st.warning("Please provide a Job Description.")
            st.stop()
        if not uploaded_files:
            st.warning("Please upload at least one resume file.")
            st.stop()

        with st.spinner("Processing Pipeline..."):
            # 1. Pack ALL files into the format your GraphState expects
            # This creates a dict: {"file1.pdf": b'...bytes...', "file2.docx": b'...bytes...'}
            file_payload = {}
            for file in uploaded_files:
                file.seek(0)
                file_payload[file.name] = file.read()
            
            # 2. Build the unified input dict for LangGraph
            graph_input = {
                "job_description": job_desc,
                "resume_files": file_payload,
                "parsed_resumes": {},      # Initialize empty dicts if required by your GraphState
                "analysis_results": {}     # Initialize empty dicts if required by your GraphState
            }
            
            # 3. Invoke the graph with exactly ONE parameter
            output = resume_analyzer.invoke(graph_input)
            
            # 4. Extract results returned by the final node
            results = output.get("analysis_results", {})
            
            if not results:
                st.info("No actionable text could be extracted or evaluated.")
                st.stop()
            
            # 5. Render results dynamically loop
            for filename, report in results.items():
                title = f"📋 {filename} — Match: {report['match_percentage']}%"
                with st.expander(title, expanded=True):
                    st.progress(report['match_percentage'] / 100)
                    
                    st.markdown("**Core Strengths:**")
                    for strength in report['strengths']:
                        st.write(f"✅ {strength}")
                        
                    st.markdown("**Matched Skills:**")
                    st.caption(", ".join(report['matched_skills']) or "None detected")
                    
                    st.markdown("**Missing Essential Skills:**")
                    st.caption(", ".join(report['missing_skills']) or "None detected")
                    
                    st.markdown("**Actionable Improvements:**")
                    for upgrade in report['improvements']:
                        st.write(f"💡 {upgrade}")
