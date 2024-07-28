import os
import logging
from flask import Flask, request, jsonify
import openai
import chromadb
from datetime import datetime

# Set up OpenAI API key
openai.api_key = 'sk-proj-ygt2j1lcN0pCvqP8cMpbT3BlbkFJQE8wVwwRjJWddaY0uDjxaG'

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Read documents from markdown files in the 'docs' directory
documents = []
docs_dir = './docs'

for filename in os.listdir(docs_dir):
    if filename.endswith('.md'):
        with open(os.path.join(docs_dir, filename), 'r', encoding='utf-8') as file:
            documents.append(file.read())

client = chromadb.Client()
collection = client.create_collection(name="docs_model1")

# Store each document in a vector embedding database
for i, d in enumerate(documents):
    response = openai.Embedding.create(input=[d], model="text-embedding-ada-002")
    embedding = response['data'][0]['embedding']
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[d]
    )

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

        # Retrieve the most relevant document
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        retrieved_document = results['documents'][0]

        # Add the retrieved document as context to the messages
        messages.append({"role": "system", "content": f"Relevant document: {retrieved_document}"})

        # Generate chat completion using the messages
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=150
        )

        created_at = datetime.utcnow().isoformat() + 'Z'
        response_data = {
            "id": "chatcmpl-123",  # Example id, replace with actual id if available
            "object": "chat.completion",
            "created": created_at,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": completion['choices'][0]['message']['content']
                    },
                    "finish_reason": "stop"
                }
            ]
        }

        logger.info(f"Chat response: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"Error generating chat completion: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11434)
