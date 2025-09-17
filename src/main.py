import os
from dotenv import load_dotenv

from classes.anthropic_connector import AnthropicConnector
from classes.gemini_connector import GeminiConnector
from classes.ollama_connector import OllamaConnector
from classes.openai_connector import OpenAIConnector

load_dotenv(override=True)
API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ANTHROFIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

messages = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Berlin is the capital of Germany."},
    {"role": "user", "content": "Okay... but why do I need Berlin?"},
]

# OllamaConnector examples
ollama_bot = OllamaConnector()
response_ollama_ask = ollama_bot.ask("What is the capital of France?").run().get_result()
response_ollama_conversation = ollama_bot.conversation(messages).run().get_result()
response_ollama_ask_stream = ollama_bot.ask("What is the capital of France?").stream().enable_print_result().run()
response_ollama_conversation_stream = ollama_bot.conversation(messages).stream().enable_print_result().run()

# OpenAIConnector examples
openai_bot = OpenAIConnector(api_key=API_KEY)
response_openai_ask = openai_bot.ask("What is the capital of France?").run().get_result()
response_openai_conversation = openai_bot.conversation(messages).run().get_result()
response_openai_ask_stream = openai_bot.ask("What is the capital of France?").stream().enable_print_result().run()
response_openai_conversation_stream = openai_bot.conversation(messages).stream().enable_print_result().run()

# GeminiConnector examples
gemini_bot = GeminiConnector(api_key=GEMINI_API_KEY)
response_gemini_ask = gemini_bot.ask("What is the capital of France?").run().get_result()
response_gemini_conversation = gemini_bot.conversation(messages).run().get_result()
response_gemini_ask_stream = gemini_bot.ask("What is the capital of France?").stream().enable_print_result().run()
response_gemini_conversation_stream = gemini_bot.conversation(messages).stream().enable_print_result().run()

# AnthropicConnector examples
anthropic_bot = AnthropicConnector(api_key=ANTHROFIC_API_KEY)
response_anthropic_ask = anthropic_bot.ask("What is the capital of France?").run().get_result()
response_anthropic_conversation = anthropic_bot.conversation(messages).run().get_result()
response_anthropic_ask_stream = anthropic_bot.ask("What is the capital of France?").stream().enable_print_result().run()
response_anthropic_conversation_stream = anthropic_bot.conversation(messages).stream().enable_print_result().run()

print("Ollama ask:", response_ollama_ask)
print("Ollama conversation:", response_ollama_conversation)
print("Ollama ask stream:", response_ollama_ask_stream)
print("Ollama conversation stream:", response_ollama_conversation_stream)

print("OpenAI ask:", response_openai_ask)
print("OpenAI conversation:", response_openai_conversation)
print("OpenAI ask stream:", response_openai_ask_stream)
print("OpenAI conversation stream:", response_openai_conversation_stream)

print("Gemini ask:", response_gemini_ask)
print("Gemini conversation:", response_gemini_conversation)
print("Gemini ask stream:", response_gemini_ask_stream)
print("Gemini conversation stream:", response_gemini_conversation_stream)

print("Anthropic ask:", response_anthropic_ask)
print("Anthropic conversation:", response_anthropic_conversation)
print("Anthropic ask stream:", response_anthropic_ask_stream)
print("Anthropic conversation stream:", response_anthropic_conversation_stream)
