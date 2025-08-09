import chainlit as cl
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

# File to store chat history
HISTORY_FILE = "chat_history.json"

# Load chat history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save chat history to file
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

@cl.on_chat_start
async def on_chat_start():
    if not os.environ.get("GOOGLE_API_KEY"):
        await cl.Message(content="Please configure your GOOGLE_API_KEY in a .env file.").send()
        return

    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # Load history
    history = load_history()
    memory = ConversationBufferMemory(return_messages=True)
    for message in history:
        if message["type"] == "user":
            memory.chat_memory.add_user_message(message["content"])
        elif message["type"] == "ai":
            memory.chat_memory.add_ai_message(message["content"])

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    # Create the runnable
    runnable = (
        RunnablePassthrough.assign(
            history=lambda x: memory.load_memory_variables(x).get("history", [])
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    cl.user_session.set("runnable", runnable)
    cl.user_session.set("memory", memory)
    cl.user_session.set("history", history)

    if history:
        for message in history:
            if message["type"] == "user":
                await cl.Message(author="User", content=message["content"]).send()
            elif message["type"] == "ai":
                await cl.Message(author="Assistant", content=message["content"]).send()
    else:
        await cl.Message(content="Starting a new chat. How can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")
    memory = cl.user_session.get("memory")
    history = cl.user_session.get("history")

    # Get response from the model
    response = await runnable.ainvoke({"input": message.content})

    # Save user message and AI response to memory
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(response)

    # Update and save history file
    history.append({"type": "user", "content": message.content})
    history.append({"type": "ai", "content": response})
    save_history(history)
    cl.user_session.set("history", history)

    await cl.Message(content=response).send()
