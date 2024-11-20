import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chain import Chain  # Importing the Chain class for job extraction and email generation
from portfolio import Portfolio  # Importing the Portfolio class for querying relevant portfolio links
from utils import clean_text  # Importing a utility function for cleaning text

# Function to create the Streamlit app
def create_streamlit_app(llm, portfolio, clean_text):
    # Set the title of the Streamlit web app
    st.title("📧 Cold Mail Generator")

    # Input field for the user to provide a URL (default value provided for testing)
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-41251?from=job%20search%20funnel")
    
    # Button to trigger processing of the input URL
    submit_button = st.button("Submit")

    if submit_button:  # Executes when the "Submit" button is clicked
        try:
            # Load the content of the given URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)  # Clean the scraped text content
            
            # Load the portfolio links (relevant portfolio projects or examples)
            portfolio.load_portfolio()
            
            # Extract job details from the cleaned text using the Chain class
            jobs = llm.extract_jobs(data)
            
            # Iterate through the extracted jobs
            for job in jobs:
                # Extract required skills from the job details
                skills = job.get('skills', [])
                
                # Query portfolio links relevant to the extracted skills
                links = portfolio.query_links(skills)
                
                # Generate a cold email for the job using the Chain class
                email = llm.write_mail(job, links)
                
                # Display the generated email in the app as Markdown code
                st.code(email, language='markdown')
        except Exception as e:
            # Display an error message if an exception occurs
            st.error(f"An Error Occurred: {e}")


# Main entry point of the program
if __name__ == "__main__":
    # Initialize the Chain class for job extraction and email writing
    chain = Chain()
    
    # Initialize the Portfolio class for querying relevant portfolio links
    portfolio = Portfolio()
    
    # Set the configuration for the Streamlit app (layout, title, and icon)
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    # Run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)
