import os
from langchain_community.document_loaders import PyPDFLoader
from pinecone import Pinecone
from dotenv import load_dotenv

from src.services.index import get_base_directory, list_board_game_indices, get_pinecone_config, get_text_splitter

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)


def index():
    base_directory = get_base_directory()
    if not os.path.exists(base_directory):
        print(f"Directory does not exist: {base_directory}")
        return

    # Initialize embeddings and text splitter
    text_splitter = get_text_splitter()

    # Get list of game folders using list_board_game_indices
    game_folders = list_board_game_indices()
    if not game_folders:
        print(f"No game folders found in {base_directory}")
        return

    for game_folder in game_folders:
        game_path = os.path.join(base_directory, game_folder)
        index_name = game_folder
        documents = []

        # Process each PDF in the game folder
        for filename in os.listdir(game_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(game_path, filename)
                print(f"Processing {file_path}")

                try:
                    # Load PDF with PyPDFLoader
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()

                    # Split documents into chunks
                    split_docs = text_splitter.split_documents(docs)
                    documents.extend(split_docs)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

        if documents:
            try:
                pinecone_config = get_pinecone_config()

                # Create Pinecone index
                if index_name not in pc.list_indexes().names():
                    pc.create_index(
                        name=index_name,
                        **pinecone_config
                    )

                print(f"Successfully processed {index_name}")
            except Exception as e:
                print(f"Error creating vector store for {index_name}: {e}")


# if __name__ == "__main__":
#     index()