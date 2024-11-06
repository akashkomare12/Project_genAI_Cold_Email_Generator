# Cold Email Generator

Cold email generator for services company using groq, langchain and streamlit. It allows users to input the URL of a company's careers page. The tool then extracts job listings from that page and generates personalized cold emails. These emails include relevant portfolio links sourced from a vector database, based on the specific job descriptions.

## Imagine a scenario:

- Nike needs a Principal Software Engineer and is spending time and resources in the hiring process, on boarding, training etc
- CodeSpyder is Software Development company can provide a dedicated software development engineer to Nike. So, the business development executive (Akash) from CodeSpyder is going to reach out to Nike via a cold email.

![image](https://github.com/user-attachments/assets/4737c2f0-9731-44fd-a0e8-7ba8aa139827)


## Set-up
To get started we first need to get an API_KEY from here: https://console.groq.com/keys. Inside app/.env update the value of GROQ_API_KEY with the API_KEY you created.

Run the streamlit app:

streamlit run app/main.py
