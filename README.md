# Simple QnA Chatbot

A simple question-and-answer chatbot built using Chainlit and OpenAI Agent SDK with a Custom Model Provider(Google Gemini). This chatbot provides an interactive interface for users to ask questions and receive responses in real-time.

## Features

- OpenAI Agent SDK With Custom Model (Gemini)
- Interactive chat interface using Chainlit
- Powered by Gemini API for intelligent responses
- Real-time message streaming
- Chat history management
- Error handling and user feedback

## Prerequisites

- Python 3.12 or higher
- Gemini API key
- Uv (Python Package Managet)

## Installation

1. Clone the repository:
```bash
git clone 
cd simple-qna-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv add openai-agents==0.04 python-dotenv chainlit
```

4. Create a `.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Start the chatbot:
```bash
uv run chainlit run chatbot.py -w
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8000)

3. Start chatting with the bot!

## Project Structure

```
simple-qna-chatbot/
├── src/
│   └── simple_qna_chatbot/
│       ├── chatbot.py      # Main chatbot implementation
│       ├── streaming.py    # Streaming functionality
│       └── __init__.py     # Package initialization
├── .env                    # Environment variables
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Development

This project uses:
- Chainlit for the web interface
- Gemini API for language model capabilities
- Python 3.12+ for the backend



## Author

- Qureshihasaan (hasaanqureshi150@gmail.com)
