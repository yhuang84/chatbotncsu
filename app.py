#!/usr/bin/env python3
"""
NCSU Research Assistant - Streamlit Community Entry Point
==========================================================
This file serves as the entry point for Streamlit Community Cloud.
For local development, you can also run: streamlit run user_interface.py
"""

import sys
import os
import traceback

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Add src to path
src_dir = os.path.join(current_dir, 'src')
if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)

# Import the main interface
# This will execute all the Streamlit code in user_interface.py
try:
    import user_interface
except Exception as e:
    # If import fails, show error in Streamlit
    import streamlit as st
    st.error("❌ Error loading application")
    st.exception(e)
    st.code(traceback.format_exc())
    st.info("📋 Please check the logs for more details.")
    raise
