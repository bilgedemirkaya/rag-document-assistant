from core.observer import Observable

class AppNotifier(Observable):
    def __init__(self):
        super().__init__()

    def notify_new_message(self, query, answer):
        self.notify("new_message", {"query": query, "answer": answer})

    def notify_summarization_complete(self, chunk_count, location_count, top_keywords):
        self.notify("summarization_complete", {
            "chunks": chunk_count,
            "locations": location_count,
            "keywords": len(top_keywords)
        })
