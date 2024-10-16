import json
import pathlib

from langchain.schema import Document


def load_documents(json_path: pathlib.Path) -> list[Document]:
    with json_path.open("r") as f:
        data = json.load(f)

    docs = [
        Document(
            page_content=x["content"],
            metadata={
                "id": pid,
                "link": x["link"],
                "date": x["date"],
                "title": x["title"],
                "category": x["category"],
            },
        )
        for pid, x in data.items()
    ]
    return docs
