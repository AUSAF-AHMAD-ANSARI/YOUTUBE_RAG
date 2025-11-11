"""
Streamlit UI for AI YouTube Summarizer - Professional Edition
==============================================================
Enterprise-grade interface with modern design patterns

SETUP INSTRUCTIONS:
1. Make sure youtube_processor.py is in the same folder
2. Install: pip install -r requirements.txt
3. Create .env with: GOOGLE_API_KEY=your_key_here
4. Run: streamlit run app.py
"""

import streamlit as st
import time
from youtube_processor import process_video, extract_video_id_from_url

# ============================================================================
# CONFIGURATION
# ============================================================================

DEVELOPER_NAME = "Ausaf Ahmad Ansari"
DEVELOPER_TITLE = "Computer Science Graduate"
GITHUB_URL = "https://github.com/AUSAF-AHMAD-ANSARI"
LINKEDIN_URL = "https://www.linkedin.com/in/ausafahmadansari/"

# ============================================================================
# PAGE SETUP
# ============================================================================

st.set_page_config(
    page_title="AI YouTube Summarizer | RAG Technology",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ADVANCED STYLING
# ============================================================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    
    /* Animated background pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(168, 85, 247, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main Card Container */
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent,
            rgba(99, 102, 241, 0.8),
            rgba(168, 85, 247, 0.8),
            transparent
        );
    }
    
    .main-card:hover {
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }
    
    /* Header Styling */
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
    }
    
    .header-text {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        line-height: 1.2;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
    }
    
    .subtitle-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.3rem;
        font-weight: 400;
        margin-top: 1rem;
        letter-spacing: 0.5px;
    }
    
    .accent-line {
        width: 120px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        margin: 1.5rem auto;
        border-radius: 2px;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.9rem 2.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        box-shadow: 
            0 4px 20px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 8px 30px rgba(102, 126, 234, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.4);
    }
    
    /* Stat Cards */
    .stat-card {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.15) 0%, 
            rgba(118, 75, 162, 0.15) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.1) 0%, 
            transparent 100%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 0.75rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .chat-message:hover {
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateX(4px);
    }
    
    .user-message {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.1) 0%, 
            rgba(102, 126, 234, 0.05) 100%);
        border-left: 4px solid #667eea;
    }
    
    .ai-message {
        background: linear-gradient(135deg, 
            rgba(168, 85, 247, 0.1) 0%, 
            rgba(168, 85, 247, 0.05) 100%);
        border-left: 4px solid #a855f7;
    }
    
    .chat-message strong {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(15, 12, 41, 0.95) 0%, 
            rgba(48, 43, 99, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] h3 {
        color: white;
        font-weight: 700;
        font-size: 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stInfo {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem 1.5rem;
    }
    
    /* Video Container */
    .video-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Footer */
    .footer-container {
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .footer-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 0.5rem;
    }
    
    .footer-credits {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 1.5rem;
    }
    
    /* Badge Styling */
    .tech-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Form Styling */
    .stForm {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    /* Slider Styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-header::before {
        content: '';
        width: 4px;
        height: 28px;
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        margin: 2.5rem 0;
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .stSpinner > div {
        border-color: #667eea !important;
        border-right-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'main_chain' not in st.session_state:
    st.session_state.main_chain = None
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'video_info' not in st.session_state:
    st.session_state.video_info = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def reset_app():
    """Reset application state"""
    st.session_state.main_chain = None
    st.session_state.processed = False
    st.session_state.video_info = {}
    st.session_state.chat_history = []

# ============================================================================
# HEADER
# ============================================================================

st.markdown('''
    <div class="header-container">
        <h1 class="header-text">🎥 AI YouTube Summarizer</h1>
        <div class="accent-line"></div>
        <p class="subtitle-text">Enterprise-grade RAG technology for intelligent video analysis</p>
    </div>
''', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🎯 Technology Stack")
    st.markdown("""
    <div style='margin: 1rem 0;'>
        <span class='tech-badge'>🧠 LangChain</span>
        <span class='tech-badge'>🗄️ FAISS</span>
        <span class='tech-badge'>🤖 Gemini 2.0</span>
        <span class='tech-badge'>🔥 HuggingFace</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Core Features:**
    - ✨ Advanced semantic analysis
    - 💬 Context-aware conversations
    - 🎯 Multi-chunk retrieval (10x)
    - ⚡ Real-time processing
    - 🔍 Deep content understanding
    """)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Quick Start Guide")
    st.markdown("""
    **Step 1:** Paste YouTube URL or Video ID  
    **Step 2:** Click "Process Video" button  
    **Step 3:** Explore quick actions or ask custom questions  
    **Step 4:** Review detailed analytics  
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Advanced Configuration")
    with st.expander("🔧 Model Settings", expanded=False):
        chunk_size = st.slider("Chunk Size", 400, 1200, 800, 50, 
                               help="Size of text chunks for processing")
        chunk_overlap = st.slider("Chunk Overlap", 50, 200, 100, 10,
                                  help="Overlap between consecutive chunks")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1,
                               help="Controls response creativity")
        
        model_options = {
            "Gemini 2.0 Flash ⚡ (Recommended)": "gemini-2.5-flash-lite",
            "Gemini 2.5 Pro 💎": "gemini-2.5-pro",
            "Gemini 2.5 Flash ⚡": "gemini-2.5-flash"
        }
        selected_model_name = st.selectbox("LLM Model", list(model_options.keys()))
        model_name = model_options[selected_model_name]
    
    st.markdown("---")
    
    st.markdown("### 👨‍💻 Developer Info")
    st.markdown(f"""
    <div style='padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);'>
        <p style='font-size: 1.1rem; font-weight: 700; color: white; margin-bottom: 0.5rem;'>{DEVELOPER_NAME}</p>
        <p style='color: rgba(255, 255, 255, 0.7); margin-bottom: 1rem;'>{DEVELOPER_TITLE}</p>
        <a href='{GITHUB_URL}' target='_blank' style='color: #667eea; text-decoration: none; margin-right: 1rem;'>🔗 GitHub</a>
        <a href='{LINKEDIN_URL}' target='_blank' style='color: #667eea; text-decoration: none;'>💼 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown('<p class="section-header">🔗 Video Input</p>', unsafe_allow_html=True)
    video_input = st.text_input(
        "Enter YouTube URL or Video ID",
        placeholder="https://www.youtube.com/watch?v=... or video ID",
        label_visibility="collapsed",
        key="video_input"
    )
    
    with st.expander("💡 Example Videos & Tips"):
        st.markdown("""
        **Try these sample videos:**
        - `Gfr50f6ZBvo` - Technology & AI content
        - `dQw4w9WgXcQ` - Music video example
        
        **Important Notes:**
        - Video must have closed captions/subtitles enabled
        - Processing time varies with video length
        - Optimal for videos under 60 minutes
        """)
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    
    with col_btn1:
        process_btn = st.button("🚀 Process Video", use_container_width=True, type="primary")
    
    with col_btn2:
        if st.session_state.processed:
            if st.button("🔄 New Video", use_container_width=True):
                reset_app()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.processed:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">🎬 Preview</p>', unsafe_allow_html=True)
        
        video_id = st.session_state.video_info.get('video_id', '')
        if video_id:
            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">📋 Instructions</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style='color: rgba(255, 255, 255, 0.7); line-height: 1.8;'>
            <p><strong>1.</strong> Paste a YouTube URL or video ID in the input field</p>
            <p><strong>2.</strong> Click "Process Video" to start analysis</p>
            <p><strong>3.</strong> Wait for the AI to process the transcript</p>
            <p><strong>4.</strong> Ask questions or use quick actions</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PROCESS VIDEO
# ============================================================================

if process_btn and video_input:
    video_id = extract_video_id_from_url(video_input)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.markdown("**🎬 Initializing video processor...**")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        status_text.markdown("**📝 Extracting transcript and generating embeddings...**")
        progress_bar.progress(40)
        
        status_text.markdown("**🧠 Building vector database with FAISS...**")
        progress_bar.progress(60)
        
        success, main_chain, metadata, error = process_video(
            video_id=video_id,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            model_name=model_name,
            temperature=temperature
        )
        
        progress_bar.progress(80)
        status_text.markdown("**✅ Finalizing RAG pipeline...**")
        time.sleep(0.3)
        
        progress_bar.progress(100)
        
        if success:
            status_text.markdown("**🎉 Processing complete!**")
            time.sleep(0.8)
            
            st.session_state.main_chain = main_chain
            st.session_state.processed = True
            st.session_state.video_info = {
                'video_id': video_id,
                'segments': metadata.get('segments', 0),
                'words': metadata.get('total_words', 0),
                'chunks': metadata.get('chunks', 0),
                'duration': metadata.get('duration', 0)
            }
            
            progress_bar.empty()
            status_text.empty()
            
            st.success("🎉 Video successfully processed and ready for analysis!")
            st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ Processing Error: {error}")
            st.info("💡 **Troubleshooting:** Ensure the video has captions enabled and your API key is correctly configured.")
            
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")
        st.info("💡 Please check your internet connection and try again.")
    
    finally:
        progress_bar.empty()
        status_text.empty()

# ============================================================================
# STATISTICS DASHBOARD
# ============================================================================

if st.session_state.processed and st.session_state.video_info:
    st.markdown("---")
    st.markdown('<p class="section-header">📊 Video Analytics Dashboard</p>', unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown(f"""
            <div class="stat-card">
                <p class="stat-number">{st.session_state.video_info.get('segments', 0)}</p>
                <p class="stat-label">Segments</p>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
            <div class="stat-card">
                <p class="stat-number">{st.session_state.video_info.get('words', 0):,}</p>
                <p class="stat-label">Total Words</p>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown(f"""
            <div class="stat-card">
                <p class="stat-number">{st.session_state.video_info.get('chunks', 0)}</p>
                <p class="stat-label">Data Chunks</p>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        duration_min = st.session_state.video_info.get('duration', 0) / 60
        st.markdown(f"""
            <div class="stat-card">
                <p class="stat-number">{duration_min:.1f}</p>
                <p class="stat-label">Duration (min)</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# QUICK ACTIONS
# ============================================================================

if st.session_state.processed:
    st.markdown("---")
    st.markdown('<p class="section-header">🎯 Quick Action Prompts</p>', unsafe_allow_html=True)
    
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    
    with quick_col1:
        if st.button("📝 Complete Summary", use_container_width=True):
            st.session_state.chat_history.append({
                'question': "Provide a comprehensive and detailed summary of this video, covering all major points",
                'answer': None
            })
            st.rerun()
    
    with quick_col2:
        if st.button("🔑 Key Insights", use_container_width=True):
            st.session_state.chat_history.append({
                'question': "What are the most important key takeaways and insights from this video?",
                'answer': None
            })
            st.rerun()
    
    with quick_col3:
        if st.button("👤 Speaker Analysis", use_container_width=True):
            st.session_state.chat_history.append({
                'question': "Who is the speaker and what are the main topics they discuss in this video?",
                'answer': None
            })
            st.rerun()
    
    with quick_col4:
        if st.button("💡 Core Concepts", use_container_width=True):
            st.session_state.chat_history.append({
                'question': "What are the fundamental concepts and main ideas presented in this video?",
                'answer': None
            })
            st.rerun()

# ============================================================================
# CHAT INTERFACE
# ============================================================================

if st.session_state.processed:
    st.markdown("---")
    st.markdown('<p class="section-header">💬 Intelligent Q&A Interface</p>', unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        for idx, chat in enumerate(st.session_state.chat_history):
            # Question
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🙋 Question {idx + 1}:</strong><br>
                    <span style='color: rgba(255, 255, 255, 0.85); font-size: 1rem; line-height: 1.6;'>{chat['question']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Answer
            if chat['answer'] is None:
                with st.spinner("🤔 Analyzing content with RAG pipeline..."):
                    try:
                        answer = st.session_state.main_chain.invoke(chat['question'])
                        st.session_state.chat_history[idx]['answer'] = answer
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                        st.session_state.chat_history[idx]['answer'] = f"Error: {str(e)}"
            else:
                st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>🤖 AI Response:</strong><br>
                        <span style='color: rgba(255, 255, 255, 0.85); font-size: 1rem; line-height: 1.7;'>{chat['answer']}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # New question input
    st.markdown('<div class="main-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
    st.markdown("#### ✍️ Ask Your Custom Question")
    
    with st.form(key="question_form", clear_on_submit=True):
        user_question = st.text_area(
            "Your question about the video",
            placeholder="e.g., What are the main arguments? Can you explain the concept discussed at 5:30? What examples are provided?",
            height=120,
            label_visibility="collapsed"
        )
        
        col_submit1, col_submit2 = st.columns([3, 1])
        
        with col_submit1:
            submit_question = st.form_submit_button("🚀 Submit Question", use_container_width=True, type="primary")
        
        with col_submit2:
            if st.form_submit_button("🗑️ Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        if submit_question and user_question.strip():
            st.session_state.chat_history.append({
                'question': user_question,
                'answer': None
            })
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(f"""
    <div class="footer-container">
        <p class="footer-title">🚀 Powered by Advanced RAG Technology</p>
        <p class="footer-subtitle">LangChain · FAISS Vector DB · Google Gemini 2.0 · Streamlit</p>
        <p style='color: rgba(255, 255, 255, 0.6); margin: 1rem 0;'>
            Perfect for analyzing educational content, technical tutorials, lectures, and presentations
        </p>
        <div class="accent-line" style="width: 80px; margin: 1.5rem auto;"></div>
        <p class="footer-credits">
            Engineered by <strong style='color: white;'>{DEVELOPER_NAME}</strong> · {DEVELOPER_TITLE}<br>
            <span style='font-size: 0.85rem; opacity: 0.7;'>© 2025 All Rights Reserved</span>
        </p>
    </div>
""", unsafe_allow_html=True)