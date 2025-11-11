
"""
CLI chatbot with persistent conversation history, sentiment analysis, intent classification, and typing effect.

Features:
- Stores conversation history (last 10 messages in memory)
- Saves history to a JSON file for persistence
- Loads previous conversations on startup
- Detects sentiment (positive, negative, neutral)
- Classifies intent (question, greeting, command, statement)
- Shows sentiment emoji in history
- Simulates human-like typing animation
- Responds contextually based on mood and intent
- Allows you to view the chat history
- Supports basic keyword-based responses

Type 'exit', 'quit' or press Ctrl+C to end the session.
Type 'history' to see the conversation so far (with sentiment emojis).
Type 'clear' to start a fresh conversation.
"""

import sys
import json
import random
import time
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


# ============================================================================
# Intent Classification
# ============================================================================

QUESTION_WORDS = {"what", "when", "where", "why", "how", "who", "which", "can", "could", "would", "do", "did", "does"}
GREETING_WORDS = {"hello", "hi", "hey", "greetings", "welcome", "sup", "yo", "howdy"}
COMMAND_WORDS = {"history", "clear", "help", "exit", "quit", "bye"}


def classify_intent(message: str) -> str:
    """
    Classify the intent of a message.
    Returns: 'question', 'greeting', 'command', or 'statement'
    """
    msg_lower = message.lower()
    words = set(msg_lower.split())
    
    # Check for commands first
    if any(word in COMMAND_WORDS for word in words):
        return "command"
    
    # Check for greetings
    if any(word in GREETING_WORDS for word in words):
        return "greeting"
    
    # Check for questions (question words or ends with ?)
    if any(word in QUESTION_WORDS for word in words) or msg_lower.endswith("?"):
        return "question"
    
    # Default to statement
    return "statement"


def get_intent_emoji(intent: str) -> str:
    """Return emoji for intent."""
    return {"question": "❓", "greeting": "👋", "command": "⚙️", "statement": "💬"}.get(intent, "💬")


# ============================================================================
# Typing Effect
# ============================================================================

def typing_effect(text: str, speed: float = 0.03) -> None:
    """
    Display text with a typing animation effect.
    
    Args:
        text: The text to display
        speed: Delay between characters in seconds (default: 0.03)
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()  # New line at the end


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


def get_response(message: str, sentiment: str, intent: str) -> str:
    """Return a response based on keyword matching, sentiment, and intent."""
    if not message.strip():
        return "Say something so I can respond!"

    msg = message.lower()
    
    # Check for keyword matches
    for keyword, response in RESPONSES.items():
        if keyword in msg:
            return response
    
    # Intent-aware responses
    if intent == "question":
        question_responses = [
            "That's a great question! Let me think...",
            "Good question! I'm not sure I have a perfect answer, but here's what I think...",
            "I'm glad you asked that.",
            "That's something to consider.",
        ]
        return random.choice(question_responses)
    
    if intent == "greeting":
        greeting_responses = [
            "Hello! Great to see you!",
            "Hi there! How are you doing?",
            "Hey! What's on your mind?",
            "Greetings! What can I help with?",
        ]
        return random.choice(greeting_responses)
    
    if intent == "statement":
        # Combine sentiment + statement
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
        
        # Neutral statement
        statement_responses = [
            "That's interesting! Tell me more.",
            "I see. Can you elaborate?",
            "That makes sense.",
            "Interesting perspective.",
        ]
        return random.choice(statement_responses)
    
    # Fallback for any other intent
    return random.choice(FALLBACKS)


def main() -> None:
    print("Chatbot with Sentiment & Intent Analysis — type 'history' to see your chat, 'clear' to reset, or 'exit' to leave\n")
    
    history = ConversationHistory()
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                print("Bot: ", end='')
                typing_effect("Say something — I'm listening.")
                print()
                continue
            
            # Check for exit
            if user_input.lower() in EXIT_KEYWORDS:
                print("Bot: ", end='')
                typing_effect("Goodbye! (History saved to chat_history.json)")
                print()
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
                print("Bot: ", end='')
                typing_effect("Conversation history cleared!")
                print()
                continue
            
            # Analyze sentiment and classify intent
            sentiment = analyze_sentiment(user_input)
            intent = classify_intent(user_input)
            
            # Record user message with sentiment
            history.add("user", user_input, sentiment)
            
            # Generate and display response with typing effect
            response = get_response(user_input, sentiment, intent)
            history.add("bot", response, "neutral")
            print("Bot: ", end='')
            typing_effect(response)
            print()
    
    except (KeyboardInterrupt, EOFError):
        print("\nBot: ", end='')
        typing_effect("Goodbye! (History saved to chat_history.json)")
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
