# Chainlit AI Assistant with Gemini

This is a simple Chainlit application that provides a generic AI assistant using LangChain and Google's Gemini model. The application stores chat history in a `chat_history.json` file.

## Features

-   **AI Assistant:** A conversational AI assistant powered by Gemini.
-   **Chat History:** Conversations are saved and loaded from a local JSON file (`chat_history.json`), allowing you to continue previous conversations.
-   **Powered by LangChain:** Leverages the LangChain library for building the application logic.
-   **Built with Chainlit:** A modern and easy-to-use UI for chat applications.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Google API Key:**
    -   Create a `.env` file in the root of the project.
    -   Add your Google API key to the `.env` file as follows:
        ```
        GOOGLE_API_KEY="your-google-api-key"
        ```
    -   You can obtain a Google API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).

## How to Run

Once you have completed the setup, you can run the application using the following command:

```bash
chainlit run app.py -w
```

This will start the Chainlit server. You can then access the application in your browser at `http://localhost:8000`. The `-w` flag enables auto-reloading, which is useful for development.

## How it Works

-   **`app.py`:** This is the main application file containing the Chainlit app logic.
-   **`requirements.txt`:** This file lists the Python libraries required to run the application.
-   **`chat_history.json`:** This file is created automatically to store your conversation history.
-   **`.env`:** This file is used to store your `GOOGLE_API_KEY` securely.

When you start a chat, the application:
1.  Loads the previous chat history from `chat_history.json`.
2.  Initializes the Gemini model and a conversation memory.
3.  Displays the past conversation.

As you send messages, the application:
1.  Sends your message to the Gemini model to get a response.
2.  Displays the AI's response.
3.  Saves the new message and response to the `chat_history.json` file.
