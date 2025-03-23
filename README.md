# AI Virtual Legal Assistant

## Overview
AI Virtual Legal Assistant is a cloud-based application that allows users to upload legal documents, extract text, generate summaries in both text and audio formats, and interact with an AI assistant powered by GPT-4. The project leverages Azure services for text extraction, AI processing, and speech synthesis while being deployed on an AWS EC2 instance.

## Features
- **File Upload & Storage**: Documents are uploaded and stored securely in Azure Blob Storage.
- **Text Extraction**: Utilizes Azure Document Intelligence to extract text from uploaded documents.
- **AI-Powered Summarization**: Uses Azure OpenAI (GPT-4) to generate concise summaries.
- **Text-to-Speech**: Converts summaries to speech using Azure Speech Services, allowing users to download the audio.
- **AI Chat Assistant**: A GPT-4 powered chatbot to answer legal-related queries.
- **Summary Download**: Users can download the document summary as a PDF.
- **Audio Download**: Users can download the audio version of the summary.
- **Deployment on AWS**: Hosted on an AWS EC2 instance for scalability and availability.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask/FastAPI)
- **Cloud Services**:
  - **Azure Blob Storage**: For document and audio storage
  - **Azure Document Intelligence**: For text extraction from documents
  - **Azure OpenAI (GPT-4)**: For generating document summaries and AI chat responses
  - **Azure Speech Services**: For generating audio summaries
- **Deployment**:
  - **AWS EC2**: For hosting the application

## Setup & Installation
### Prerequisites
- AWS EC2 instance with Python installed
- Azure account with access to Blob Storage, Document Intelligence, OpenAI, and Speech Services
- API keys for Azure services
- Flask or FastAPI for backend

### Installation Steps
1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/ai-legal-assistant.git
   cd ai-legal-assistant
   ```

2. **Create a virtual environment and activate it**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory and add:
   ```env
   AZURE_BLOB_STORAGE_CONNECTION_STRING=your_connection_string
   AZURE_DOCUMENT_INTELLIGENCE_KEY=your_document_intelligence_key
   AZURE_OPENAI_API_KEY=your_openai_api_key
   AZURE_SPEECH_API_KEY=your_speech_api_key
   ```

5. **Run the application**
   ```sh
   python app.py
   ```

6. **Access the application**
   - If running locally: `http://127.0.0.1:5000`
   - If deployed on AWS: `http://your-aws-ec2-ip:5000`

## AWS Deployment
1. **Launch an EC2 instance** (Ubuntu recommended)
2. **Connect to the instance**
   ```sh
   ssh -i your-key.pem ubuntu@your-ec2-instance-ip
   ```
3. **Install dependencies**
   ```sh
   sudo apt update && sudo apt install python3-pip python3-venv -y
   ```
4. **Clone the repository and follow setup steps above**
5. **Run the application**
   ```sh
   nohup python app.py &
   ```
6. **Access the application using the public IP of the EC2 instance**

## Usage
1. Upload a document.
2. View the extracted text and AI-generated summary.
3. Download the summary as a PDF or audio file.
4. Chat with the AI legal assistant for legal queries.


