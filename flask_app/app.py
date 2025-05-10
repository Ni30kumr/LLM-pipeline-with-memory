
from flask import Flask, request,jsonify
import os
from utils import search_webpages, concatenate_content,fetch_and_combine_url_content,generate_answer

# Load environment variables from .env file

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, content fetching, and answer generation functions,
    and returns the generated answer.
    """
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data['query']
    print("Received query:", user_query)

    # Step 1: Search for relevant webpages
    print("Step 1: Searching for articles...")
    webpages = search_webpages(user_query, num_results=2)
    if not webpages:
        return jsonify({"error": "No relevant webpages found."}), 404

    # Step 2: Fetch and combine content from the scraped articles
    print("Step 2: Fetching and combining content...")
    combined_content_list = fetch_and_combine_url_content(webpages)
    if not combined_content_list:
        return jsonify({"error": "Failed to retrieve content from the webpages."}), 500

# Concatenate the list of content into a single string
    combined_content = concatenate_content(combined_content_list)

    # Step 3: Generate an answer using the LLM with memory
    print("Step 3: Generating answer...")
    answer = generate_answer(combined_content, user_query)
    if not answer:
        return jsonify({"error": "Failed to generate an answer."}), 500

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='localhost', port=5001)