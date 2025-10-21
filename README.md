# Orkun GPT
RAG based application on question and answer about myself

**Overview**

The app is built with Streamlit, and uses an LLM to answer questions about Orkun Sefik. The tehcnologies used in the app are: 

- As the framework: Langchain is used,
- For embedding generation: GPT4All is used (all-MiniLM-L6-v2-f16), 
- As the LLM: Gemini 2.0 Flash-Lite is used, 
- For the UI: Streamlit for the user interface,
- For the Vector Database: Chroma DB is used. 

**Instructions**

1. run pip install -r requirements.txt
2. create a .env file within the root directory if it is not there. 
3. generate your own GEMINI API KEY from https://aistudio.google.com/ and put it in .env file as GEMINI_API_KEY = "YOUR_KEY"
4. (OPTIONAL): you can change the data just by replacing the current pdf's found in data folder with your own pdf's. 
5. run `python create_db.py` in the terminal to create the vector database from the documents.
6. run `streamlit run app.py` to launch streamlit UI in the browser
