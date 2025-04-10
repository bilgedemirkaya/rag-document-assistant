# 🗃️ Document Assistant — Retrieval-Augmented Generation with Streamlit + Claude

This project is a Streamlit-based application that allows users to upload documents, ask questions about their content, and receive intelligent answers powered by **Anthropic Claude** and **VoyageAI embeddings**.

It supports:
- Chat mode with Claude-powered question answering
- Insight mode including sentiment, location map, and keyword insights
- Multi-chat management system
- Real-time feedback with toast notifications

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/document-assistant.git
cd document-assistant
```

```
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## Add your API keys
Create a .env file in the root directory:

ANTHROPIC_API_KEY=your_anthropic_key
VOYAGE_API_KEY=your_voyage_key

## Run the App
```streamlit run main.py```

## Requirements
- Python 3.8+
- Streamlit
- Anthropic SDK
- VoyageAI
- spaCy
- geopy
- matplotlib and pandas


### Key Features
- Claude-3 integration via AnthropicClient
- Smart chunking of uploaded documents
- Top-k semantic search with VoyageAI
- Dynamic multi-chat UI (ChatGPT-style)
- Visual summarization (sentiment, maps, keywords)
- Observer pattern for real-time toast updates