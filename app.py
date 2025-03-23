import os
import time
import tempfile
import logging
import requests
from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# Load Azure credentials from environment variables
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
DOCUMENT_INTELLIGENCE_KEY = os.getenv("DOCUMENT_INTELLIGENCE_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

API_KEY = "6k6JjMIXFU4mkspzu19LZY3iruhcixrjHGWAvsyfWc4OSRpu2tpuJQQJ99BCACHYHv6XJ3w3AAAAACOGvkWS"
API_VERSION = "2024-05-01-preview"
AZURE_ENDPOINT = "https://cben-m8j7ldga-eastus2.openai.azure.com/"
AZURE_DEPLOYMENT = "gpt-4"

if not all([AZURE_STORAGE_CONNECTION_STRING, DOCUMENT_INTELLIGENCE_ENDPOINT, DOCUMENT_INTELLIGENCE_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY]):
    logging.error("One or more Azure credentials are missing. Please set environment variables.")
    raise ValueError("Missing Azure credentials.")

# Upload file to Azure Blob Storage
def upload_file_to_blob(file_path, container_name="uploads"):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        logging.info(f"File uploaded successfully: {blob_client.url}")
        return blob_client.url
    except Exception as e:
        logging.error(f"Failed to upload file to Blob Storage: {e}")
        raise

# Extract text using Azure Document Intelligence
def extract_text(file_url):
    try:
        client = DocumentIntelligenceClient(DOCUMENT_INTELLIGENCE_ENDPOINT, AzureKeyCredential(DOCUMENT_INTELLIGENCE_KEY))
        poller = client.begin_analyze_document("prebuilt-read", {"urlSource": file_url})
        result = poller.result()

        text_content = "\n".join([line.content for page in result.pages for line in page.lines])
        return text_content
    except Exception as e:
        logging.error(f"Error extracting text from document: {e}")
        raise

# Ask GPT-4 a question
def ask_gpt(prompt, max_retries=5):
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are an AI assistant. Answer the following query."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200
    }

    url = f"{AZURE_ENDPOINT}openai/deployments/{AZURE_DEPLOYMENT}/chat/completions?api-version={API_VERSION}"

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 429:  # Too many requests
                wait_time = (attempt + 1) * 2  # Exponential backoff
                logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue  # Retry request
            response.raise_for_status()  # Raise other errors
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during GPT request: {e}")
            if attempt == max_retries - 1:
                raise  # Give up after max retries

    return "Error: Too many requests. Please try again later."

# Flask Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        logging.info(f"File saved at: {file_path}")

        file_url = upload_file_to_blob(file_path)
        extracted_text = extract_text(file_url)
        summary = ask_gpt(f"Summarize this document: {extracted_text}")

        return jsonify({"filename": file.filename, "summary": summary})
    except Exception as e:
        logging.error(f"Internal Server Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    if not data or "query" not in data:
        return jsonify({"error": "No query provided"}), 400

    query = data["query"]
    try:
        response = ask_gpt(query)
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
