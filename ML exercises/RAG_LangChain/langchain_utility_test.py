import os
from langchain_openai import ChatOpenAI

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "utility_rag_test"
os.environ["OPENAI_API_KEY"] = "sk-proj-ygt2j1lcN0pCvqP8cMpbT3BlbkFJQE8wVwwRjJWdY0uDjxdaaG"

llm = ChatOpenAI()
msg = llm.invoke("Hello, Universe! testing.. What is the name of our galaxy and where are we located in the Universe?")

print(msg)
