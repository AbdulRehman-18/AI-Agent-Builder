# Ai Agent Builder

#Abdul Rehman 🔥

### Personal AI Academics Assignment

### Uploading on git just for version control

A small demo project to build, run and experiment with agentic AI. Designed for personal academic assignment and version control.

## Advanced Chatbot

A command-line chatbot with **persistent conversation history** and **sentiment analysis** is included in `chatbot.py`.

### Current Features

**Feature 1: Conversation History** ✅
- Stores the last 10 messages in memory during the session.
- Type `history` to view the full conversation.

**Feature 2: Persistent File Storage** ✅
- Saves all messages to `chat_history.json` automatically.
- Loads previous conversations when you start the chatbot.
- History persists across sessions!
- Type `clear` to start a fresh conversation.

**Feature 3: Sentiment Analysis** ✅ NEW!
- Automatically detects sentiment: **positive** 😊, **negative** 😞, or **neutral** 😐
- Shows sentiment emoji next to each message in history
- Responds empathetically based on your mood
- Example: "I love this!" → 😊 positive → "That's wonderful to hear!"
- Example: "I hate it" → 😞 negative → "I'm sorry to hear that."

### Quick Start

Run it with Python (PowerShell on Windows):

```powershell
python chatbot.py
```




### How History is Persisted

- **In-memory buffer** — Last 10 messages with sentiment metadata.
- **JSON file** — Auto-saved to `chat_history.json` with sentiment tags.
- **Auto-load** — Previous conversations load on startup.
- **Rolling window** — Only the last 10 messages are kept (oldest removed first).


