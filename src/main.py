import os
from dotenv import load_dotenv

from classes.anthropic_connector import AnthropicConnector
from classes.conversation import Conversation
from classes.conversation_participant import ConversationParticipant
from classes.gemini_connector import GeminiConnector
from classes.ollama_connector import OllamaConnector
from classes.openai_connector import OpenAIConnector
from constants.default import USER_RESERVED_NAME
from models.conversation_message import ConversationMessage

load_dotenv(override=True)
API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ANTHROFIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# ConversationParticipant examples

jack_prompt = (
    "You are Jack, a far-left communist. You always argue for radical equality and "
    "collective ownership. You dislike Lucy, who you see as a capitalist enemy. "
    "Respond only as yourself, in the first person, without adding names, tags, or brackets. "
    "Never write '[Jack]' or other speaker labels. "
    "Keep your answers short and to the point."
)


lucy_prompt = (
    "You are Lucy, a centrist capitalist. You believe in free markets and moderate reforms. "
    "You often clash with Jack, whose communist views you find extreme. "
    "Respond only as yourself, in the first person, without adding names, tags, or brackets. "
    "Never write '[Lucy]' or other speaker labels. "
    "Keep your answers short and to the point."
)


mike_prompt = (
    "You are Mike, a libertarian anarchist. You distrust both communism and capitalism. "
    "You mock Jack for wanting too much control and Lucy for defending the system. "
    "Respond only as yourself, in the first person, without adding names, tags, or brackets. "
    "Never write '[Mike]' or other speaker labels. "
    "Keep your answers short and to the point."
)


jack_bot = OllamaConnector(system_prompt=jack_prompt)
lucy_bot = OllamaConnector(system_prompt=lucy_prompt)
mike_bot = OllamaConnector(system_prompt=mike_prompt)

jack_participant = ConversationParticipant(participant_id="1", name="Jack", llm_instance=jack_bot)
lucy_participant = ConversationParticipant(participant_id="2", name="Lucy", llm_instance=lucy_bot)
mike_participant = ConversationParticipant(participant_id="3", name="Mike", llm_instance=mike_bot)

participants = [jack_participant, lucy_participant, mike_participant]


conversation = Conversation(participants=participants, messages=[
    ConversationMessage(author=USER_RESERVED_NAME, content="Hey, Jack, Lucy, and Mike! I want to create new country, any ideas how to build it?"),
])

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
CYAN = "\033[36m"

for i in range(10):
    print(f"{BOLD}{CYAN}--- Round {i+1} ---{RESET}")
    output = conversation.process_conversation_round().get_last_round_messages()
    for message in output:
        print(f"{BOLD}{GREEN}{message.author}{RESET}: {message.content}\n")

# messages = [
#     {"role": "user", "content": "What is the capital of France?"},
#     {"role": "assistant", "content": "Berlin is the capital of Germany."},
#     {"role": "user", "content": "Okay... but why do I need Berlin?"},
# ]

# messagesWithAuthors = [
#     ConversationMessage(author="David", content="I think the capital of France is London."),
#     ConversationMessage(author="John", content="I don't know... I think it's Berlin."),
#     ConversationMessage(author="user", content="What about you Amanda, what do you think?"),
# ]

# participant_ollama = ConversationParticipant(participant_id="1", name="Amanda", llm_instance=ollama_bot)
# response = participant_ollama.conversation(messagesWithAuthors).run().get_result()

# print("OllamaBot response:", response)

# # OllamaConnector examples
# ollama_bot = OllamaConnector()
# response_ollama_ask = ollama_bot.ask("What is the capital of France?").run().get_result()
# response_ollama_conversation = ollama_bot.conversation(messages).run().get_result()
# response_ollama_ask_stream = ollama_bot.ask("What is the capital of France?").stream().enable_print_result().run()
# response_ollama_conversation_stream = ollama_bot.conversation(messages).stream().enable_print_result().run()




# # OllamaConnector examples
# ollama_bot = OllamaConnector()
# response_ollama_ask = ollama_bot.ask("What is the capital of France?").run().get_result()
# response_ollama_conversation = ollama_bot.conversation(messages).run().get_result()
# response_ollama_ask_stream = ollama_bot.ask("What is the capital of France?").stream().enable_print_result().run()
# response_ollama_conversation_stream = ollama_bot.conversation(messages).stream().enable_print_result().run()

# # OpenAIConnector examples
# openai_bot = OpenAIConnector(api_key=API_KEY)
# response_openai_ask = openai_bot.ask("What is the capital of France?").run().get_result()
# response_openai_conversation = openai_bot.conversation(messages).run().get_result()
# response_openai_ask_stream = openai_bot.ask("What is the capital of France?").stream().enable_print_result().run()
# response_openai_conversation_stream = openai_bot.conversation(messages).stream().enable_print_result().run()

# # GeminiConnector examples
# gemini_bot = GeminiConnector(api_key=GEMINI_API_KEY)
# response_gemini_ask = gemini_bot.ask("What is the capital of France?").run().get_result()
# response_gemini_conversation = gemini_bot.conversation(messages).run().get_result()
# response_gemini_ask_stream = gemini_bot.ask("What is the capital of France?").stream().enable_print_result().run()
# response_gemini_conversation_stream = gemini_bot.conversation(messages).stream().enable_print_result().run()

# # AnthropicConnector examples
# anthropic_bot = AnthropicConnector(api_key=ANTHROFIC_API_KEY)
# response_anthropic_ask = anthropic_bot.ask("What is the capital of France?").run().get_result()
# response_anthropic_conversation = anthropic_bot.conversation(messages).run().get_result()
# response_anthropic_ask_stream = anthropic_bot.ask("What is the capital of France?").stream().enable_print_result().run()
# response_anthropic_conversation_stream = anthropic_bot.conversation(messages).stream().enable_print_result().run()

# print("Ollama ask:", response_ollama_ask)
# print("Ollama conversation:", response_ollama_conversation)
# print("Ollama ask stream:", response_ollama_ask_stream)
# print("Ollama conversation stream:", response_ollama_conversation_stream)

# print("OpenAI ask:", response_openai_ask)
# print("OpenAI conversation:", response_openai_conversation)
# print("OpenAI ask stream:", response_openai_ask_stream)
# print("OpenAI conversation stream:", response_openai_conversation_stream)

# print("Gemini ask:", response_gemini_ask)
# print("Gemini conversation:", response_gemini_conversation)
# print("Gemini ask stream:", response_gemini_ask_stream)
# print("Gemini conversation stream:", response_gemini_conversation_stream)

# print("Anthropic ask:", response_anthropic_ask)
# print("Anthropic conversation:", response_anthropic_conversation)
# print("Anthropic ask stream:", response_anthropic_ask_stream)
# print("Anthropic conversation stream:", response_anthropic_conversation_stream)
