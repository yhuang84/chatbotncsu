#!/usr/bin/env python3
"""
NCSU Research Assistant - Web Interface
========================================
A beautiful web interface for the NCSU Research Assistant with NC State branding.
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 🔑 Load API key - Priority: Environment Variables > Streamlit Secrets > .env file
api_key_loaded = False

# Try environment variables first (for Streamlit Community and other cloud deployments)
if os.getenv('OPENAI_API_KEY'):
    api_key_loaded = True

# Try Streamlit secrets (for Streamlit Community)
if not api_key_loaded:
    try:
        if hasattr(st, 'secrets') and st.secrets is not None:
            os.environ['OPENAI_API_KEY'] = st.secrets["openai"]["api_key"]
            api_key_loaded = True
    except (KeyError, AttributeError, TypeError, FileNotFoundError):
        pass

# Try .env file as fallback
if not api_key_loaded:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv('OPENAI_API_KEY'):
            api_key_loaded = True
    except ImportError:
        pass

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="NCSU Search Assistant",
    page_icon="🐺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the researcher (after page config)
from ncsu_advanced_config_base import NCSUAdvancedResearcher

# Custom CSS for NC State red theme
st.markdown("""
<style>
    /* NC State Red Theme */
    :root {
        --ncsu-red: #CC0000;
        --ncsu-dark-red: #990000;
        --ncsu-light-red: #FF4444;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #CC0000 !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #CC0000 0%, #990000 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #CC0000;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #990000;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(204, 0, 0, 0.3);
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input {
        border: 2px solid #CC0000;
        border-radius: 8px;
    }
    
    /* Cards/Containers */
    .stExpander {
        border: 2px solid #CC0000;
        border-radius: 8px;
        background-color: white;
    }
    
    /* Success/Info boxes */
    .stSuccess {
        background-color: rgba(204, 0, 0, 0.1);
        border-left: 4px solid #CC0000;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    /* Result container */
    .result-box {
        background: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #CC0000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Source card */
    .source-card {
        background: #f8f8f8;
        padding: 15px;
        border-radius: 8px;
        border-left: 3px solid #CC0000;
        margin: 10px 0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #CC0000 !important;
        font-weight: bold !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #CC0000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'running' not in st.session_state:
    st.session_state.running = False

# Header with logos
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "NC_State_Wolfpack_logo.svg.png")
        st.image(logo_path, width=150)
    except:
        st.write("🐺")

with col2:
    st.markdown("<h1 style='text-align: center;'>🎯 NCSU Research Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>AI-Powered Research Tool for NC State University</p>", unsafe_allow_html=True)

with col3:
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "NC-State-University-Logo.png")
        st.image(logo_path, width=150)
    except:
        st.write("🏛️")

st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Key check
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        st.success("✅ API Key Loaded")
    else:
        st.error("❌ No API Key Found")
        st.info("Add OPENAI_API_KEY to your .env file or Streamlit secrets")
    
    st.markdown("---")
    
    # LLM Settings
    st.markdown("### 🤖 LLM Settings")
    llm_provider = st.selectbox(
        "Provider",
        ["openai", "anthropic", "mock"],
        index=0
    )
    
    llm_model = st.text_input(
        "Model",
        value="gpt-4.1-mini" if llm_provider == "openai" else "claude-3-sonnet-20240229"
    )
    
    llm_temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Lower values = more deterministic, Higher values = more creative"
    )

    llm_max_tokens = st.number_input(
        "Max Tokens",
        min_value=1000,
        max_value=8000,
        value=4000,
        step=500,
        help="Maximum length of the generated answer"
    )
    
    st.markdown("---")
    
    # Search Settings
    st.markdown("### 🔍 Search Settings")
    top_k = st.slider(
        "Top-K Results",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="Number of initial search results to retrieve"
    )

    max_pages = st.slider(
        "Max Pages to Extract",
        min_value=5,
        max_value=30,
        value=20,
        step=5,
        help="Maximum number of pages to extract content from"
    )

    relevance_threshold = st.slider(
        "Relevance Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1,
        help="Minimum relevance score for content to be included"
    )
    
    st.markdown("---")
    
    # Advanced Settings
    with st.expander("⚙️ Advanced Settings"):
        enable_grading = st.checkbox("Enable Content Grading", value=True, help="Use LLM to grade content relevance")
        selenium_enabled = st.checkbox("Enable Selenium", value=True, help="For JavaScript-heavy pages")
        enhanced_extraction = st.checkbox("Enhanced Extraction", value=True, help="More comprehensive content extraction")
        
        st.markdown("---")
        st.markdown("**📊 Additional Options:**")
        
        min_content_length = st.number_input(
            "Min Content Length (chars)",
            min_value=0,
            max_value=1000,
            value=100,
            step=50
        )
        max_content_length = st.number_input(
            "Max Content Length (chars)",
            min_value=1000,
            max_value=100000,
            value=50000,
            step=5000
        )
        timeout = st.number_input(
            "Timeout (seconds)",
            min_value=10,
            max_value=120,
            value=30,
            step=10
        )

# Main content area
st.markdown("### 📝 Enter Your Research Query")

query = st.text_area(
    "What would you like to research about NC State?",
    height=100,
    placeholder="Example: How can I get reimbursement for my travel expenses as a student?"
)

# Example queries
st.markdown("**💡 Example Queries:**")
examples_col1, examples_col2, examples_col3 = st.columns(3)

with examples_col1:
    if st.button("🎓 Graduate Programs"):
        query = "What are the computer science graduate programs at NCSU?"
        st.rerun()

with examples_col2:
    if st.button("💰 Financial Aid"):
        query = "What kinds of scholarships are available for students?"
        st.rerun()

with examples_col3:
    if st.button("✈️ Travel Reimbursement"):
        query = "How can I get reimbursement for my travel expenses?"
        st.rerun()

st.markdown("---")

# Research button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔍 Start Research", use_container_width=True, type="primary")

# Perform research
if search_button and query:
    st.session_state.running = True
    
    # Create config
    config = {
        'query': query,
        'llm_provider': llm_provider,
        'llm_model': llm_model,
        'llm_temperature': llm_temperature,
        'llm_max_tokens': llm_max_tokens,
        'top_k': top_k,
        'max_pages': max_pages,
        'relevance_threshold': relevance_threshold,
        'enable_grading': enable_grading,
        'selenium_enabled': selenium_enabled,
        'enhanced_extraction': enhanced_extraction,
        'min_content_length': min_content_length,
        'max_content_length': max_content_length,
        'output_dir': 'results',
        'timeout': timeout
    }
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize researcher
        status_text.markdown("🔧 **Initializing researcher...**")
        progress_bar.progress(10)
        researcher = NCSUAdvancedResearcher(config)
        
        # Conduct research
        status_text.markdown("🔍 **Searching NCSU website...**")
        progress_bar.progress(30)
        
        with st.spinner("Conducting research... This may take a few minutes."):
            results = researcher.research(query)
        
        status_text.markdown("✅ **Research complete!**")
        progress_bar.progress(100)
        
        # Save results
        saved_files = researcher.save_results(results)
        
        # Store in session state
        st.session_state.results = results
        st.session_state.saved_files = saved_files
        st.session_state.running = False
        
        st.success("🎉 Research completed successfully!")
        
    except Exception as e:
        st.error(f"❌ Error during research: {str(e)}")
        st.session_state.running = False
        import traceback
        with st.expander("Error Details"):
            st.code(traceback.format_exc())

# Display results
if st.session_state.results:
    results = st.session_state.results
    
    st.markdown("---")
    st.markdown("## 📊 Research Results")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔍 Search Results",
            len(results.get('search_results', []))
        )
    
    with col2:
        st.metric(
            "📄 Pages Extracted",
            len(results.get('extracted_pages', []))
        )
    
    with col3:
        st.metric(
            "✅ Pages Filtered",
            len(results.get('filtered_pages', []))
        )
    
    with col4:
        total_words = sum(p.get('word_count', 0) for p in results.get('filtered_pages', []))
        st.metric(
            "📝 Total Words",
            f"{total_words:,}"
        )
    
    # Answer
    st.markdown("### 🤖 AI-Generated Answer")

    # Get answer text
    answer_text = results.get('final_answer', 'No answer generated')

    # Add custom CSS for link styling
    st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] a {
        color: #CC0000 !important;
        text-decoration: none;
        font-weight: 500;
        border-bottom: 1px solid #CC0000;
    }
    div[data-testid="stMarkdownContainer"] a:hover {
        color: #990000 !important;
        border-bottom: 2px solid #990000;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display answer (Markdown format will auto-render links)
    st.markdown(answer_text)

    # Download answer
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if 'saved_files' in st.session_state:
            answer_file = st.session_state.saved_files.get('answer')
            if answer_file and os.path.exists(answer_file):
                with open(answer_file, 'r', encoding='utf-8') as f:
                    answer_content = f.read()
                st.download_button(
                    label="📥 Download Answer",
                    data=answer_content,
                    file_name=f"ncsu_research_answer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    # Sources
    st.markdown("### 📚 Sources")
    
    sources = results.get('sources', [])
    for i, source in enumerate(sources, 1):
        with st.expander(f"📄 Source {i}: {source['title']} (Relevance: {source['relevance_score']:.2f})"):
            st.markdown(f"""
            **URL:** [{source['url']}]({source['url']})
            
            **Relevance Score:** {source['relevance_score']:.3f}
            
            **Word Count:** {source['word_count']:,} words
            """)
    
    # Detailed data
    with st.expander("📊 View Detailed Research Data"):
        st.json(results)
    
    # Save info
    if 'saved_files' in st.session_state:
        st.markdown("### 💾 Saved Files")
        for file_type, file_path in st.session_state.saved_files.items():
            st.code(f"{file_type.upper()}: {file_path}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>🐺 NC State University Research Assistant</strong></p>
    <p>Powered by AI | Built with ❤️ for the Wolfpack</p>
    <p style='font-size: 0.9em;'>© 2025 NC State University | Enhanced UI Version</p>
</div>
""", unsafe_allow_html=True)

