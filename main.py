from fastapi import FastAPI, UploadFile, File
from embeddings import generate_embedding
from database import add_document, query_documents
from file_handler import extract_text
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import io

app = FastAPI()
executor = ThreadPoolExecutor()

@app.post("/ingest/")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text(content, file.filename)
    embedding = await app.loop.run_in_executor(executor, generate_embedding, text)
    add_document(file.filename, text, embedding)
    return {"status": "success", "file": file.filename}

@app.get("/query/")
async def query(query: str):
    query_embedding = await app.loop.run_in_executor(executor, generate_embedding, query)
    results = await app.loop.run_in_executor(executor, query_documents, query_embedding)
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
