from core.observer import Observer
import streamlit as st

class UIObserver(Observer):
    def update(self, event_type: str, data: dict):
        if event_type == "new_message":
            st.toast(f"✅ New answer generated for: {data['query'][:50]}...")
        elif event_type == "summarization_complete":
            st.toast(f"✅ Summarization complete — {data['chunks']} chunks, {data['locations']} locations, {data['keywords']} keywords")
