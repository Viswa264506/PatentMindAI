import json
from pathlib import Path

INPUT_FILE = Path("backend/data/lens-sample-patent-bulk.jsonl")
OUTPUT_FILE = Path("backend/data/lens-sample-patent-bulk.json")

patents = []


with INPUT_FILE.open("r", encoding="utf-8") as file:

    for line in file:

        patent = json.loads(line)

        # ------------------------
        # Patent Number
        # ------------------------
        patent_number = patent.get("doc_number", "")

        # ------------------------
        # Title
        # ------------------------
        titles = patent.get("biblio", {}).get("invention_title", [])

        title = None

        for t in titles:
            if t.get("lang") == "en":
                title = t.get("text")
                break

        if title is None and titles:
            title = titles[0].get("text")

        # ------------------------
        # Abstract
        # ------------------------
        abstracts = patent.get("abstract", [])

        abstract = None

        for a in abstracts:
            if a.get("lang") == "en":
                abstract = a.get("text")
                break

        if abstract is None and abstracts:
            abstract = abstracts[0].get("text")

        if not title or not abstract:
            continue

        patents.append(
            {
                "patent_number": patent_number,
                "title": title,
                "abstract": abstract,
                "jurisdiction": patent.get("jurisdiction"),
                "publication_type": patent.get("publication_type"),
            }
        )

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(patents, f, indent=2, ensure_ascii=False)

print("=" * 60)
print(f"Saved {len(patents)} patents")
print(f"Output : {OUTPUT_FILE}")
print("=" * 60)