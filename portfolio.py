import pandas as pd  # For handling CSV file data
import chromadb  # For managing a vector database
import uuid  # For generating unique IDs

# Define a class to manage a portfolio of projects and related links
class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        """
        Initializes the Portfolio class with:
        - `file_path`: The CSV file containing portfolio data (default is "my_portfolio.csv").
        - `self.data`: A DataFrame loaded from the CSV file.
        - `self.chroma_client`: A persistent ChromaDB client to manage vector database.
        - `self.collection`: A collection in the ChromaDB database for storing portfolio data.
        """
        self.file_path = file_path
        self.data = pd.read_csv(file_path)  # Read portfolio data from the specified CSV file
        self.chroma_client = chromadb.PersistentClient('vectorstore')  # Initialize ChromaDB persistent client
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")  # Create or get a collection named "portfolio"

    def load_portfolio(self):
        """
        Loads portfolio data into the vector database.
        - Adds each row of the portfolio CSV to the ChromaDB collection if it's empty.
        - Stores `Techstack` as the document and `Links` as metadata.
        """
        if not self.collection.count():  # Check if the collection is empty
            for _, row in self.data.iterrows():  # Iterate through rows in the DataFrame
                self.collection.add(
                    documents=row["Techstack"],  # Add the technical stack as the searchable document
                    metadatas={"links": row["Links"]},  # Add the project link as metadata
                    ids=[str(uuid.uuid4())]  # Assign a unique ID to each entry
                )

    def query_links(self, skills):
        """
        Queries the vector database to find portfolio links based on the required skills.
        - `skills`: A list of skills to search for in the database.
        - Returns the metadata (links) for the top 2 results.
        """
        return self.collection.query(
            query_texts=skills,  # Use the skills as the query text
            n_results=2  # Retrieve the top 2 most relevant results
        ).get('metadatas', [])  # Extract and return only the metadata (links)

