import os
import pickle

import faiss
import numpy as np


class VectorDatabase:

    def __init__(self):

        self.index = None

        self.metadata = []

    def build_index(self, embeddings, metadata):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            np.array(embeddings).astype("float32")
        )

        self.metadata = metadata

        print(f"Indexed {len(metadata)} chunks.")

    def save(
        self,
        index_path="vectorstore/faiss.index",
        metadata_path="vectorstore/metadata.pkl"
    ):

        os.makedirs("vectorstore", exist_ok=True)

        faiss.write_index(
            self.index,
            index_path
        )

        with open(metadata_path, "wb") as f:

            pickle.dump(
                self.metadata,
                f
            )

        print("Vector database saved.")

    def load(
        self,
        index_path="vectorstore/faiss.index",
        metadata_path="vectorstore/metadata.pkl"
    ):

        self.index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as f:

            self.metadata = pickle.load(f)

        print("Vector database loaded.")

    def search(self, query_embedding, top_k=4):

        distances, indices = self.index.search(

            np.array([query_embedding]).astype("float32"),

            top_k
        )

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            results.append(
                self.metadata[idx]
            )

        return results