
"""
CLI chatbot with persistent conversation history and sentiment analysis.

Features:
- Stores conversation history (last 10 messages in memory)
- Saves history to a JSON file for persistence
- Loads previous conversations on startup
- Detects sentiment (positive, negative, neutral)
- Shows sentiment emoji in history
- Responds empathetically based on mood
- Allows you to view the chat history
- Supports basic keyword-based responses

Type 'exit', 'quit' or press Ctrl+C to end the session.
Type 'history' to see the conversation so far (with sentiment emojis).
Type 'clear' to start a fresh conversation.
"""

import sys
import json
import random
from typing import List, Tuple
from pathlib import Path

RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What would you like to talk about?",
    "help": "I can chat with you and remember our conversation. Type 'history' to see what we've talked about, or just keep chatting!",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome!",
    "thank you": "Happy to help!",
}

FALLBACKS = [
    "I'm not sure I understand. Can you rephrase?",
    "Interesting — tell me more.",
    "Hmm, I don't have a good answer for that yet.",
]

EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye"}


# ============================================================================
# Sentiment Analysis
# ============================================================================

POSITIVE_WORDS = {
    "good", "great", "awesome", "excellent", "love", "happy", "nice", "wonderful", 
    "fantastic", "amazing", "brilliant", "perfect", "beautiful", "wonderful", 
    "delighted", "thrilled", "excited", "pleased", "glad", "joy", "superb"
}

NEGATIVE_WORDS = {
    "bad", "terrible", "hate", "sad", "angry", "awful", "poor", "disappointed", 
    "frustrated", "upset", "annoyed", "miserable", "awful", "disgusting", "horrible",
    "dreadful", "dislike", "worse", "worst", "worst", "pathetic", "useless"
}


def analyze_sentiment(message: str) -> str:
    """
    Analyze sentiment of a message.
    Returns: 'positive', 'negative', or 'neutral'
    """
    words = message.lower().split()
    
    pos_count = sum(1 for word in words if word.strip(".,!?;:") in POSITIVE_WORDS)
    neg_count = sum(1 for word in words if word.strip(".,!?;:") in NEGATIVE_WORDS)
    
    if pos_count > neg_count and pos_count > 0:
        return "positive"
    elif neg_count > pos_count and neg_count > 0:
        return "negative"
    return "neutral"


def get_sentiment_emoji(sentiment: str) -> str:
    """Return emoji for sentiment."""
    return {"positive": "😊", "negative": "😞", "neutral": "😐"}.get(sentiment, "😐")


RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What would you like to talk about?",
    "help": "I can chat with you and remember our conversation. Type 'history' to see what we've talked about, or just keep chatting!",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome!",
    "thank you": "Happy to help!",
}

FALLBACKS = [
    "I'm not sure I understand. Can you rephrase?",
    "Interesting — tell me more.",
    "Hmm, I don't have a good answer for that yet.",
]

EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye"}


class ConversationHistory:
    """Store and retrieve conversation messages with file persistence and sentiment."""
    
    def __init__(self, max_size: int = 10, history_file: str = "chat_history.json"):
        self.messages: List[Tuple[str, str, str]] = []  # (speaker, text, sentiment)
        self.max_size = max_size
        self.history_file = Path(history_file)
        self.load_from_file()
    
    def load_from_file(self) -> None:
        """Load conversation history from JSON file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Convert to tuples and keep only the last max_size messages
                    self.messages = [tuple(msg) if len(msg) == 3 else (msg[0], msg[1], "neutral") 
                                    for msg in data[-self.max_size:]]
            except (json.JSONDecodeError, IOError):
                self.messages = []
    
    def save_to_file(self) -> None:
        """Save conversation history to JSON file."""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save history: {e}")
    
    def add(self, speaker: str, text: str, sentiment: str = "neutral") -> None:
        """Add a message to history with sentiment and save."""
        self.messages.append((speaker, text, sentiment))
        if len(self.messages) > self.max_size:
            self.messages.pop(0)
        self.save_to_file()
    
    def display(self) -> str:
        """Return formatted history for display with sentiment emojis."""
        if not self.messages:
            return "No conversation history yet."
        
        lines = ["📝 Conversation History:"]
        for speaker, text, sentiment in self.messages:
            emoji = get_sentiment_emoji(sentiment)
            prefix = "You" if speaker == "user" else "Bot"
            lines.append(f"  {emoji} {prefix}: {text}")
        return "\n".join(lines)
    
    def clear(self) -> None:
        """Clear all history."""
        self.messages = []
        self.save_to_file()


def get_response(message: str, sentiment: str) -> str:
    """Return a response based on keyword matching and sentiment."""
    if not message.strip():
        return "Say something so I can respond!"

    msg = message.lower()
    
    # Check for keyword matches
    for keyword, response in RESPONSES.items():
        if keyword in msg:
            return response
    
    # Sentiment-aware responses
    if sentiment == "positive":
        pos_responses = [
            "That's wonderful to hear!",
            "I'm glad you're excited!",
            "That sounds amazing!",
            "That's great! Tell me more.",
        ]
        return random.choice(pos_responses)
    
    if sentiment == "negative":
        neg_responses = [
            "I'm sorry to hear that. That sounds frustrating.",
            "I understand. That must be difficult.",
            "I feel for you. Is there anything I can help with?",
            "That's tough. I'm here to listen.",
        ]
        return random.choice(neg_responses)
    
    # Fallback for neutral
    return random.choice(FALLBACKS)


def main() -> None:
    print("Chatbot with Sentiment Analysis — type 'history' to see your chat, 'clear' to reset, or 'exit' to leave\n")
    
    history = ConversationHistory()
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                print("Bot: Say something — I'm listening.\n")
                continue
            
            # Check for exit
            if user_input.lower() in EXIT_KEYWORDS:
                print("Bot: Goodbye! (History saved to chat_history.json)\n")
                break
            
            # Check for history command
            if user_input.lower() == "history":
                print(f"Bot: {history.display()}\n")
                sentiment = analyze_sentiment(user_input)
                history.add("user", user_input, sentiment)
                continue
            
            # Check for clear command
            if user_input.lower() == "clear":
                history.clear()
                print("Bot: Conversation history cleared!\n")
                continue
            
            # Analyze sentiment
            sentiment = analyze_sentiment(user_input)
            emoji = get_sentiment_emoji(sentiment)
            
            # Record user message with sentiment
            history.add("user", user_input, sentiment)
            
            # Generate and display response
            response = get_response(user_input, sentiment)
            history.add("bot", response, "neutral")
            print(f"Bot: {response}\n")
    
    except (KeyboardInterrupt, EOFError):
        print("\nBot: Goodbye! (History saved to chat_history.json)\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
