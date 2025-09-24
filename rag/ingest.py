from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from app.config import INFINITEPAY_PAGES, RAG_DB
from rag.utils import fetch_text, chunk_text

def ingest():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    client = PersistentClient(path=str(RAG_DB))

    
    try:
        coll = client.get_collection('infinitepay')
    except:
        coll = client.create_collection('infinitepay')

    docs = []
    metas = []
    ids = []

    for url in INFINITEPAY_PAGES:
        try:
            text = fetch_text(url)
        except Exception as e:
            print('Failed to fetch', url, e)
            continue

        chunks = chunk_text(text, chunk_size=400, overlap=50)
        for i, c in enumerate(chunks):
            docs.append(c)
            metas.append({'source': url, 'chunk': i})
            ids.append(f"{url}__{i}")

    if not docs:
        print('No documents to ingest. Check network or URLs.')
        return

    embeddings = model.encode(docs, convert_to_numpy=True)
    coll.add(
        documents=docs,
        metadatas=metas,
        ids=ids,
        embeddings=embeddings.tolist()
    )

    print('Ingest complete. Documents:', len(docs))

if __name__ == '__main__':
    ingest()
