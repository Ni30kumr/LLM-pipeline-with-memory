# LLM-Based RAG System

## Overview

This project is designed to create a Retrieval-Augmented Generation (RAG) system using a Large Language Model (LLM). The system integrates with an API to scrape content from the internet and uses an API to serve the LLM-generated answers. A simple front-end interface is provided to interact with the system.  
**Note**: ONLY use the packages provided in the `requirements.txt` file (similar/alternative packages are okay only if they perform the same task/function).



## Process Overview

1. **User Input via Streamlit Interface**:  
   - The user interacts with a Streamlit-based front-end where they can input their query.

2. **Query Sent to Flask Backend**:  
   - The query entered by the user is sent from the Streamlit interface to a Flask backend via an API call.

3. **Internet Search and Article Scraping**:  
   - The Flask backend searches the internet for the query using SerpAPI. It retrieves the top relevant articles and scrapes their content, extracting only the useful text (headings and paragraphs).

4. **Content Processing**:  
   - The scraped content is processed and combined with the user's query to create an input for the LLM.

5. **LLM Response Generation**:  
   - The processed content and the user's query are used to generate a contextual answer using the Gemini LLM. The LLM is accessed via API, and the generated response is returned to the Flask backend.

6. **Response Sent Back to Streamlit Interface**:  
   - The Flask backend sends the generated answer back to the Streamlit interface, where it is displayed to the user.

7. **Memory (Optional)**:  
   - Langchain memory is used to maintain conversational context, enabling multi-turn dialogue.

## What we expect?

We expect you to explore, understand the components and functionality, and demonstrate your ability to work with the provided tools and deliver a solution that meets the requirements.  
**Bonus points:** If you use Langchain (or similar tools to add memory to the system) to make the chatbot conversational.

## Prerequisites

- Python 3.12 or above

## Setup Instructions

### Step 1: Clone or download the Repository

```bash
git clone https://github.com/Ni30kumr/LLM-pipeline-with-memory.git
cd LLM-pipeline-with-memory
```

Or download the ZIP and extract it.

### Step 2: Set Up a Virtual Environment

You can use `venv` or `conda` to create an isolated environment for this project.

#### Using venv

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using conda

```bash
conda create --name project_env python=3.12
conda activate project_env
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory and add your API keys:
 🔎 Web Search: [SerpAPI Dashboard](https://serpapi.com/dashboard)  
- 🧠 LLM Prompt Testing: [Gemini Prompt Studio](https://aistudio.google.com/app/prompts/new_chat)

```env
SERPAPI_API_KEY=your_serpapi_key_here
GEMINI_API_KEY=your_gemini_key_here
```


### Step 5: Run the Flask Backend

```bash
cd flask_app
python app.py
```

### Step 6: Run the Streamlit Frontend

Open a new terminal window:

```bash
cd streamlit_app
streamlit run app.py
```

### Step 7: Open the Application

Go to your browser and open:

```
http://localhost:8501
```

Now you're ready to interact with the system.

## Project Structure

- **flask_app/**: Contains the backend Flask API and utility functions.
- **streamlit_app/**: Contains the Streamlit front-end code.
- **.env**: Stores API keys (do not commit this file).
- **requirements.txt**: Lists the project dependencies.






