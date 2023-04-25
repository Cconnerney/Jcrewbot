# Index.py
# Store embeddings/ vectorstores

import os
import pickle
import faiss

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


os.environ['OPENAI_API_KEY'] = 'my_key'

input_path = "/Users/cristinconnerney/Desktop/Instalily/data/product1.csv"
output_path = '/Users/cristinconnerney/Desktop/Instalily/data/data2.pkl'


def main():

    # Open files with data loader
    loader = CSVLoader(file_path= input_path) 
    data = loader.load()

    embeddings = OpenAIEmbeddings()

    # Create a vector store from the documents and save it to disk.
    store = FAISS.from_documents(data, embeddings)

    with open(output_path, "wb") as f:
        pickle.dump(store, f)


if __name__ == '__main__':
    main()
