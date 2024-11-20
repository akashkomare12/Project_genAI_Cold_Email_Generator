import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define a class for handling job extraction and email generation using the LangChain framework
class Chain:
    def __init__(self):
        # Initialize the language model with specific parameters
        self.llm = ChatGroq(
            temperature=0,  # Set deterministic behavior (no randomness in responses)
            groq_api_key=os.getenv("API_KEY"),  # Retrieve API key from environment variables
            model_name="llama-3.1-70b-versatile"  # Use the specified LLM model
        )

    # Method to extract job details from the scraped website text
    def extract_jobs(self, cleaned_text):
        # Define a prompt template for extracting job details
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        # Combine the prompt with the language model to create a chain
        chain_extract = prompt_extract | self.llm

        # Invoke the chain with the input text
        res = chain_extract.invoke(input={"page_data": cleaned_text})

        try:
            # Parse the output into JSON format
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            # Raise an exception if parsing fails, possibly due to large context or invalid JSON
            raise OutputParserException("Context too big. Unable to parse jobs.")
        
        # Ensure the result is always returned as a list of jobs
        return res if isinstance(res, list) else [res]

    # Method to write a cold email based on job details and portfolio links
    def write_mail(self, job, links):
        # Define a prompt template for email generation
        prompt_email = PromptTemplate.from_template(
            """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Akash, a business development executive at CodeSpyder Technologies. CodeSpyder Technologies is an AI & Software Consulting company dedicated to facilitating
        the seamless integration of business processes through automated tools. 
        Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
        process optimization, cost reduction, and heightened overall efficiency. 
        Your job is to write a cold email to the client regarding the job mentioned above describing the capability of  CodeSpyder Technologies 
        in fulfilling their needs.
        Also add the most relevant ones from the following links to showcase  CodeSpyder Technologies's portfolio: {link_list}
        Remember you are Akash, BDE at  CodeSpyder Technologies. 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        
        """
        )

        # Combine the prompt with the language model to create a chain
        chain_email = prompt_email | self.llm

        # Invoke the chain with job details and links as input
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        
        # Return the generated email content
        return res.content

# If the script is run as the main program, print the API key for debugging
if __name__ == '__main__':
    print(os.getenv('API_KEY'))  # Retrieve and print the API key from environment variables
