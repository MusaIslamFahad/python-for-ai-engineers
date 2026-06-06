# 🔴 Advanced Projects

| Project | Skills Used | Description |
|---------|------------|-------------|
| 01 — RAG Chatbot | Embeddings, ChromaDB, LLM API | Q&A bot over your own documents |
| 02 — LLM Eval Framework | async, pytest, Pandas, LLM API | Benchmark LLMs on custom tasks |
| 03 — Text Classification API | FastAPI, sklearn, Docker | Serve an ML model as a REST API |
| 04 — Multi-Tool Agent | Tool calling, asyncio, LLM API | Agent that searches and codes |
| 05 — Fine-tuning Pipeline | PyTorch, HuggingFace, LoRA | Fine-tune an LLM on custom data |

## Project 01 Starter: RAG Chatbot
```python
# rag_chatbot.py
# Skills: embeddings, vector DB, LLM API, streaming
# pip install anthropic chromadb sentence-transformers

import anthropic
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

class RAGChatbot:
    def __init__(self, docs_dir: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic()
        self.model = model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma = chromadb.Client()
        self.collection = self.chroma.create_collection("docs")
        self._index_documents(docs_dir)
    
    def _index_documents(self, docs_dir: str):
        for path in Path(docs_dir).rglob("*.txt"):
            text = path.read_text()
            chunks = self._chunk(text)
            embeddings = self.embedder.encode(chunks).tolist()
            ids = [f"{path.stem}_{i}" for i in range(len(chunks))]
            self.collection.add(documents=chunks, embeddings=embeddings, ids=ids)
        print(f"Indexed {self.collection.count()} chunks")
    
    def _chunk(self, text: str, size: int = 400, overlap: int = 50) -> list[str]:
        chunks, start = [], 0
        while start < len(text):
            chunks.append(text[start:start+size])
            start += size - overlap
        return chunks
    
    def ask(self, query: str) -> str:
        q_emb = self.embedder.encode([query]).tolist()
        results = self.collection.query(query_embeddings=q_emb, n_results=3)
        context = "\n\n".join(results["documents"][0])
        
        response = self.client.messages.create(
            model=self.model, max_tokens=1000,
            system="Answer using only the context. Cite sources when possible.",
            messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}]
        )
        return response.content[0].text

# Usage:
# bot = RAGChatbot("./docs")
# print(bot.ask("What is RAG?"))
```

## Resources
- [HuggingFace PEFT (LoRA)](https://huggingface.co/docs/peft)
- [LangChain Docs](https://docs.langchain.com)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Weights & Biases for experiment tracking](https://wandb.ai)
