import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
import aiohttp
import re
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate,SystemMessagePromptTemplate
from langchain.chains import LLMChain
import getpass
from langchain_core.runnables import RunnableSequence
load_dotenv()

import os


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

Gemini_API=os.environ.get("Gemini_API")

# Load API keys from environment variables
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
genai.configure(api_key=Gemini_API)
OPENAI_API_KEY = None



def search_webpages(query, search_location="Delhi, Delhi, India", language="en", num_results=2):
    """
    Searches for webpages related to the query using the SerpAPI general Search API.
    Returns a list of dictionaries containing webpage URLs and titles.
    """
    # api_key = os.environ.get("YOUR_SERPAPI_API_KEY")  # Store your API key securely!
    # if not api_key:
    #     print("Error: Please set the YOUR_SERPAPI_API_KEY environment variable.")
    #     return None

    url = "https://serpapi.com/search"  # SerpAPI endpoint for general search
    params = {
        "engine": "google",  # Use the general Google search engine
        "q": query,
        "api_key": SERPER_API_KEY,
        "hl": language,
        "location": search_location,
        "num": num_results,
        "safe": "off"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        webpages = []
        if "organic_results" in data:
            for result in data["organic_results"]:
                webpage_info = {
                    "url": result.get("link"),
                    "title": result.get("title"),
                    "snippet": result.get("snippet")  # Optional: include the snippet
                }
                webpages.append(webpage_info)
            print(webpages)   
        else:
            print("No webpage results found in the API response.")
            return []

        return webpages

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing API response: Missing key - {e}")
        print(f"API Response: {data}")  # Print the raw response for debugging
        return None


def fetch_and_combine_url_content(webpages):
    """
    Takes a list of webpage dictionaries (from search_webpages).
    Fetches and combines the readable text content from each URL.
    Returns a combined string of all contents.
    """
    combined_content = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)

    for page in webpages:
        url = page.get("url")
        if not url:
            continue
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract visible text from the page
            paragraphs = soup.find_all("p")
            page_text = "\n".join(p.get_text() for p in paragraphs)
            combined_content += f"\n--- Content from {url} ---\n"
            combined_content += page_text.strip() + "\n"

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
        except Exception as e:
            print(f"Error parsing content from {url}: {e}")

    return combined_content.strip()


def concatenate_content(raw_text):
    """
    Takes the combined raw text from fetch_and_combine_url_content().
    Cleans and preprocesses the text for downstream use.
    """
    if not raw_text:
        return ""

    # Remove multiple empty lines
    cleaned_text = re.sub(r"\n\s*\n+", "\n\n", raw_text)

    # Strip leading/trailing whitespace
    cleaned_text = cleaned_text.strip()

    # Optional: Normalize any funky characters or encodings
    cleaned_text = cleaned_text.replace('\xa0', ' ')  # Replace non-breaking spaces

    return cleaned_text





# Initialize the memory object


def generate_answer(content, query): # 'content' is combined_content from web search, 'query' is user_query
    """
    Generates an answer from the concatenated content using Gemini with memory support and LCEL.
    """
    
    # 1. Define the prompt template.
    # This template now explicitly includes placeholders for chat history, web search context, and the user's query.
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template(
            "Based on the following web search context and our conversation history, please answer my query.\n\n"
            "Web Search Context:\n{context}\n\n"
            "My Query:\n{user_query}"
        )
    ])

    # 2. Initialize the Gemini model.
    # Using "gemini-2.0-flash-lite" as specified in your latest provided code context.
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", google_api_key=os.getenv("Gemini_API"))

    # 3. Load current memory variables.
    # `memory.load_memory_variables({})` returns a dictionary, typically like: {'chat_history': [message1, message2]}
    loaded_memory_vars = memory.load_memory_variables({})
    chat_history_messages = loaded_memory_vars.get("chat_history", []) # Get the list of messages, or an empty list if none.

    # 4. Construct the chain using LCEL's pipe operator.
    chain = prompt | llm 

    # 5. Prepare the input for the chain.
    # This dictionary must contain keys that match the input variables in your ChatPromptTemplate.
    chain_input = {
        "chat_history": chat_history_messages, # The loaded conversation history
        "context": content,                   # The web search content
        "user_query": query                   # The user's current query
    }

    # 6. Run the chain.
    response_obj = chain.invoke(chain_input) # This will likely return an AIMessage object
    
    # Extract the actual text content from the language model's response object.
    answer_text = ""
    if hasattr(response_obj, 'content'):
        answer_text = response_obj.content
    else:
        answer_text = str(response_obj) # Fallback if 'content' attribute is not present
    memory.save_context(
        {"input": query},      # The user's direct query for this turn
        {"output": answer_text} # The AI's textual response for this turn
    )

    return answer_text


