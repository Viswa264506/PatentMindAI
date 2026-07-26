import json
from pathlib import Path

from backend.tools.embedding_tool import EmbeddingTool
from backend.tools.vector_search_tool import VectorSearchTool
from backend.schemas.state import Patent

INPUT_FILE = Path("backend/data/lens-sample-patent-bulk.json")

embedding_tool = EmbeddingTool()
vector_tool = VectorSearchTool()

with INPUT_FILE.open("r", encoding="utf-8") as f:
    patents_json = json.load(f)

print(f"Loaded {len(patents_json)} patents")

patents = []
embeddings = []

for index, item in enumerate(patents_json, start=1):

    patent = Patent(
        patent_number=item["patent_number"],
        title=item["title"],
        abstract=item["abstract"],
        provider="Lens Sample Dataset"
    )

    embedding = embedding_tool.get_embedding(
        patent.title + "\n" + patent.abstract
    )

    patents.append(patent)
    embeddings.append(embedding)

    if index % 100 == 0:
        print(f"Processed {index}/{len(patents_json)} patents")

print("Saving vectors to ChromaDB...")

try:
    vector_tool.store_patents(
        patents=patents,
        embeddings=embeddings
    )

    print("=" * 60)
    print("✅ Vector Database Built Successfully!")
    print(f"Stored {len(patents)} patents")
    print("=" * 60)

except Exception as e:
    print("\n❌ ERROR OCCURRED")
    print(type(e).__name__)
    print(e)
print(f"Stored {len(patents)} patents")
print("=" * 60)