import streamlit as st
from parsers.parser_factory import get_parser
from utils.chunker import chunk_text
from embeddings.voyage_client import EmbeddingClient

from core.retriever import retrieve_top_k
from core.anthropic_client import AnthropicClient
import spacy
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from collections import Counter
from core.notifier import AppNotifier
from core.ui_observer import UIObserver
from textblob import TextBlob

notifier = AppNotifier()
notifier.register(UIObserver())

nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="rag_doc_map")
embedding_client = EmbeddingClient()
anthropic_client = AnthropicClient()

def main():
    st.set_page_config(page_title="🗃️ Document Assistant", layout="wide")

    # --- Initialize Session State ---
    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat 1": []}
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "Chat 1"
    if "chunks" not in st.session_state:
        st.session_state.chunks = []
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = []

    def create_new_chat():
        new_index = len(st.session_state.chats) + 1
        new_name = f"Chat {new_index}"
        st.session_state.chats[new_name] = []
        st.session_state.current_chat = new_name
        st.rerun() # update ui

    # --- Sidebar: Chat Sessions ---
    with st.sidebar:
        st.header("💬 Chat Sessions")
        mode = st.radio("Select Mode", ["Chat", "Insights"])
        st.markdown("### 🧾 Your Chats")

        chats_to_delete = None
        for chat_name in list(st.session_state.chats.keys()):
            cols = st.columns([0.8, 0.2])
            if cols[0].button(chat_name, key=f"select_{chat_name}", use_container_width=True):
                st.session_state.current_chat = chat_name
            if len(st.session_state.chats) > 1 and cols[1].button("❌", key=f"delete_{chat_name}"):
                chats_to_delete = chat_name

        if st.button("➕ New Chat"):
            create_new_chat()

        if chats_to_delete:
            del st.session_state.chats[chats_to_delete]
            if chats_to_delete == st.session_state.current_chat:
                if st.session_state.chats:
                    st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                else:
                    create_new_chat()
            st.rerun()

        st.markdown("### 🕘 Chat History")
        for i, (q, a) in enumerate(reversed(st.session_state.chats[st.session_state.current_chat])):
            with st.expander(f"Q{i+1}: {q}"):
                st.write(a)

    st.title(f"🗃️ Document Assistant — {st.session_state.current_chat}")

    if mode == "Chat":
        # --- Upload Document ---
        st.subheader("📂 Upload a Document")
        uploaded_file = st.file_uploader("Choose a document", type=["pdf", "txt", "docx"])
        if uploaded_file:
            filetype = uploaded_file.name.split(".")[-1]
            parser = get_parser(filetype)
            full_text = parser.parse(uploaded_file)
            st.success("File parsed successfully!")
            st.text_area("📄 Extracted Text", full_text[:1000], height=200)

            chunks = chunk_text(full_text)
            embeddings = embedding_client.embed_texts(chunks)

            st.session_state.chunks = chunks
            st.session_state.embeddings = embeddings

        # --- Question Input ---
        st.subheader("💬 Ask a Question About Your Document")
        query = st.text_input("Enter your question:")
        if query and st.button("Submit Query"):
            if not st.session_state.chunks:
                st.warning("Please upload and process a document first.")
            else:
                query_embedding = embedding_client.embed_texts([query])[0]
                top_chunks = retrieve_top_k(query_embedding, st.session_state.embeddings, st.session_state.chunks, k=3)
                top_chunk_texts = [chunk for chunk, sims in top_chunks]
                answer = anthropic_client.answer_query_base(query, top_chunk_texts)
                st.session_state.chats[st.session_state.current_chat].append((query, answer))
                notifier.notify_new_message(query, answer)
                st.write("### Answer")
                st.write(answer)

    elif mode == "Insights":
        st.subheader("📊 Insights — Visual Overview")

        if not st.session_state.chunks:
            st.info("Please upload and process a document in Chat Mode first.")
        else:
            full_text = " ".join(st.session_state.chunks)

            # Sentiment Analysis
            blob = TextBlob(full_text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            st.markdown("### 💬 Sentiment Analysis")
            st.metric("Polarity", f"{polarity:.2f}", help="Ranges from -1 (negative) to 1 (positive)")
            st.metric("Subjectivity", f"{subjectivity:.2f}", help="Ranges from 0 (objective) to 1 (subjective)")

            # Optional color-coded comment
            if polarity > 0.2:
                st.success("Overall sentiment is positive.")
            elif polarity < -0.2:
                st.error("Overall sentiment is negative.")
            else:
                st.info("Overall sentiment is neutral.")


            # Map
            doc = nlp(full_text)
            locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
            unique_locations = list(set(locations))[:20]

            geo_data = []
            for loc in unique_locations:
                try:
                    geo = geolocator.geocode(loc)
                    if geo:
                        geo_data.append({"lat": geo.latitude, "lon": geo.longitude})
                except Exception:
                    continue

            if geo_data:
                st.markdown("### 🗺️ Locations Mentioned in the Document")
                st.map(geo_data)
            else:
                st.info("No geographic locations detected in the document.")

            # Top keywords chart
            st.markdown("### 📊 Top Keywords")
            words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
            word_freq = Counter(words)
            top_keywords = word_freq.most_common(15)

            if top_keywords:
                keywords, counts = zip(*top_keywords)
                fig_bar, ax_bar = plt.subplots()
                ax_bar.barh(keywords[::-1], counts[::-1])
                ax_bar.set_xlabel("Frequency")
                ax_bar.set_title("Top 15 Keywords")
                st.pyplot(fig_bar)
                notifier.notify_summarization_complete(
                    chunk_count=len(st.session_state.chunks),
                    location_count=len(geo_data),
                    top_keywords=top_keywords
                )

            else:
                st.info("Not enough content to generate a keyword chart.")

if __name__ == "__main__":
    main()
