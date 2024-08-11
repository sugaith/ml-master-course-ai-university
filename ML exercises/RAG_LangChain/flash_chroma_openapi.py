import os
import logging
from flask import Flask, request, jsonify, Response
import openai
import chromadb
from datetime import datetime
import json

# Set up OpenAI API key
openai.api_key = 'sk-proj---'

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Helper function to split text into chunks
def split_text_into_chunks(text, max_tokens=256):
    sentences = text.split('.')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_tokens:
            current_chunk += sentence + '.'
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + '.'

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Read documents from markdown files in the 'docs' directory
documents = []
docs_dir = './docs'

for filename in os.listdir(docs_dir):
    if filename.endswith('.md'):
        with open(os.path.join(docs_dir, filename), 'r', encoding='utf-8') as file:
            documents.append(file.read())

client = chromadb.Client()
collection = client.create_collection(name="docs_model1")

# Store each document in a vector embedding database in batches
batch_size = 1
for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    for j, d in enumerate(batch):
        logger.info(f"Processing document {i + j + 1}/{len(documents)}")
        chunks = split_text_into_chunks(d)
        for k, chunk in enumerate(chunks):
            try:
                response = openai.Embedding.create(input=[chunk], model="text-embedding-ada-002")
                embedding = response['data'][0]['embedding']
                collection.add(
                    ids=[f"{i + j}_{k}"],
                    embeddings=[embedding],
                    documents=[chunk]
                )
                logger.info(f"Processed chunk {k + 1}/{len(chunks)} of document {i + j + 1}")
            except Exception as e:
                logger.error(f"Error embedding chunk {k + 1} of document {i + j + 1}: {e}")

@app.route('/')
def home():
    logger.info("Accessed home route")
    return jsonify({"message": "Welcome to the API"})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model')
    messages = data.get('messages')

    logger.info(f"Chat request received: model={model}, messages={messages}")

    if not model or not messages:
        logger.error("Model and messages are required")
        return jsonify({"error": "Model and messages are required"}), 400

    try:
        # Generate embedding for the latest user message
        latest_user_message = next((msg['content'] for msg in messages if msg['role'] == 'user'), None)
        if not latest_user_message:
            logger.error("No user message found")
            return jsonify({"error": "No user message found"}), 400

        response = openai.Embedding.create(input=[latest_user_message], model="text-embedding-ada-002")
        query_embedding = response['data'][0]['embedding']

        # Retrieve the most relevant document chunk
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=9
        )
        retrieved_documents = results['documents'][0]

        logger.info(f"Retrieved documents=====> {retrieved_documents}")

        # Add the retrieved document chunk as context to the messages
        messages.append({"role": "system", "content": f"Utility-NYC Documents: {retrieved_documents}"})

        # Generate chat completion using the messages
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=150,
            stream=True  # Enable streaming
        )

        def generate():
            for chunk in completion:
                content = chunk['choices'][0]['delta'].get('content', '')
                if content:
                    yield json.dumps({"message": {"role": "assistant", "content": content}}) + "\n"

        return Response(generate(), content_type='application/json')

    except Exception as e:
        logger.error(f"Error generating chat completion: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11434)
