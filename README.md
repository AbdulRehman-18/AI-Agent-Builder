# Ai Agent Builder

### Personal AI Academics Assignment

### Uploading on git just for version control

A small demo project to build, run and experiment with agentic AI. Designed for personal academic assignment and version control.

## Advanced Chatbot

A command-line chatbot with **persistent history**, **sentiment analysis**, and **intent classification** is included in `chatbot.py`.

### Current Features

**Featur 1: Conversaton History** ✅
- Stores the last 10 messages in memory during the session.
- Type `history` to view the full coversation.

**Fature 2: Persistet File Storage** ✅
- Saves all messages to `chat_history.json` automatically.
- Loads previous conversations when you start the chatbot.
- History persists across essions!
- Type `clear` to start a fresh conversation.

**Feature : NEW! Sentiment Analysis** ✅ NEW!
- Automatically detects sentiment: **positive** 😊, **negative** 😞, or **neutral** 😐
- Shows sentiment emoji next to each message in history
- Responds empathetically based on your mood

**Feature 4: Intent Classification** ✅
- Classifies messages as: **question** ❓, **greeting** 👋, **command** ⚙️, or **statement** 💬
- Tailors responses based on intent
- Examples:
  - "What is Python?" → ❓ question → "That's a great question!"
  - "Hi!" → 👋 greeting → "Hello! Great to see you!"
  - "I love coding" → 💬 statement → "That's wonderful to hear!"

**Feature 5: Typing Effect** ⌨️ NEW!
- Bot responses appear character-by-character with realistic delays
- Simulates human-like typing animation
- Creates a more engaging, natural conversation feel
- Speed: ~0.03 seconds per character (customizable in code)

### Quick Start

Run it with Python (PowerShell on Windows):

```powershell
python chatbot.py
```

Watch as the bot "types" its responses in real-time for a more natural conversation! ⌨️

### Commands

- **Regular chat** — Type any message and the bot responds contextually
- **`history`** — Display all messages with sentiment emojis
- **`clear`** — Clear the chat history and start fresh
- **`help`** — Get quick help
- **`exit`, `quit`, `bye`** — End the session

### How Intent Classification Works

The bot recognizes:
- **Questions** — "What...", "How...", "Can you...?" → thoughtful responses
- **Greetings** — "Hello", "Hi", "Hey" → warm responses
- **Commands** — "history", "clear", "help" → executes commands
- **Statements** — Everything else → asks for elaboration

Combined with sentiment analysis for contextual, empathetic responses!

### How History is Persisted

- **In-memory buffer** — Last 10 messages with sentiment metadata.
- **JSON file** — Auto-saved to `chat_history.json` with sentiment tags.
- **Auto-load** — Previous conversations load on startup.
- **Rolling window** — Only the last 10 messages are kept (oldest removed first).


