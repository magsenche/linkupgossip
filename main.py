import logging
import os
import pathlib

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from linkup import dataset, utils

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

if __name__ == "__main__":
    # TODO: use all posts?
    dataset.retrieve_posts("vsd", 200)
    dataset.retrieve_posts("public", 200)

    output_folder = pathlib.Path(os.getenv("OUTPUT_FOLDER", "outputs"))
    documents = []
    for site_name in ["vsd", "public"]:
        for json_file in (output_folder / site_name).glob("*.json"):
            documents += utils.load_documents(json_file)
    logging.info(f"{len(documents)} articles ready to be embeded")

    # TODO: some data cleaning (duplicates)
    # TODO: request HF api key if too slow

    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)

    vs_folder_path = output_folder / "vectorstore"
    vectorstore.save_local(vs_folder_path)
    logging.info(f"Saved vectorstore at {vs_folder_path}")
