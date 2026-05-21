import os
import tempfile
import streamlit as st
from summarizer import ResearchPaperSummarizer

st.set_page_config(
    page_title="AI Research Paper Summarizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more premium look
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .premium-title {
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        padding-bottom: 0.5rem;
    }
    .premium-subtitle {
        font-size: 1.15rem;
        color: #8892b0;
        font-weight: 400;
        margin-top: -1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "summarizer" not in st.session_state:
    st.session_state.summarizer = None

if "summary_result" not in st.session_state:
    st.session_state.summary_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.title("Settings")
    
    uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"])
    
    user_api_key = st.text_input(
        "Google Gemini API Key", 
        type="password", 
        help="Paste your API key here. It will be used for this session only."
    )
    
    detail_level = st.selectbox(
        "Summary Detail Level",
        options=["Brief", "Standard", "Detailed"],
        index=1,
        help="Choose how detailed the generated report should be."
    )
    
    if st.button("Generate Summary", type="primary", use_container_width=True):
        if not user_api_key:
            st.error("Please enter your Google Gemini API Key first.")
        elif uploaded_file is not None:
            # Initialize with user's key
            st.session_state.summarizer = ResearchPaperSummarizer(api_key=user_api_key)
            st.session_state.summary_result = None
            st.session_state.chat_history = []
            st.session_state.summarizer.extracted_text = ""
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name
            
            with st.status("Processing Paper...", expanded=True) as status:
                st.write("Initializing model and splitting text...")
                try:
                    result = st.session_state.summarizer.summarize(temp_path, detail_level=detail_level)
                    st.session_state.summary_result = result
                    status.update(label="Summary generated successfully!", state="complete", expanded=False)
                except Exception as e:
                    import traceback
                    st.error(traceback.format_exc())
                    status.update(label=f"Error: {e}", state="error")
            
            try:
                os.unlink(temp_path)
            except:
                pass
        else:
            st.warning("Please upload a PDF first.")

st.markdown('<h1 class="premium-title">📚 AI Research Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="premium-subtitle">Elevate your research workflow. Instantly generate comprehensive structured insights and interact dynamically with any academic paper.</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Summary Report", "Chat with Paper"])

with tab1:
    if st.session_state.summary_result:
        st.markdown(st.session_state.summary_result)
        
        st.download_button(
            label="Download Summary as Markdown",
            data=st.session_state.summary_result,
            file_name="research_paper_summary.md",
            mime="text/markdown",
        )
    else:
        st.info("Upload a PDF and click 'Generate Summary' in the sidebar to get started.")

with tab2:
    if not st.session_state.summary_result:
        st.info("Please generate a summary first to unlock chat functionality.")
    else:
        # Display chat messages from history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask a question about the paper..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Thinking..."):
                    response = st.session_state.summarizer.answer_question(prompt)
                    message_placeholder.markdown(response)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
