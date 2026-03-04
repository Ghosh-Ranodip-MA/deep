import streamlit as st
import requests
import time

def render_header():
    st.set_page_config(page_title="AI Research Synthesis", layout="wide")
    st.title("🔬 AI Research Synthesis and Gap Analysis Engine")

def poll_status(report_id: int, backend_url: str):
    status_placeholder = st.empty()
    while True:
        resp = requests.get(f"{backend_url}/api/status/{report_id}")
        if resp.status_code == 200:
            status_data = resp.json()
            current_status = status_data["status"]
            status_placeholder.info(f"Status: {current_status}")
            if current_status == "completed":
                return True
            elif current_status == "failed":
                status_placeholder.error("Analysis failed.")
                return False
            elif current_status == "pending":
                time.sleep(2)
                continue
        else:
            st.error("Failed to get status")
            return False
    return False