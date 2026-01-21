"""Configuration settings for the Financial Fine-Print Decoder."""

import os
from dotenv import load_dotenv

load_dotenv()

# Provider configurations
PROVIDERS = {
    "Groq (Free)": {
        "env_key": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
        "description": "Free tier, very fast. Uses Llama 3.3 70B.",
    },
    "Google Gemini (Free)": {
        "env_key": "GEMINI_API_KEY",
        "model": "gemini-2.0-flash",
        "description": "Free tier with 60 req/min. Google AI.",
    },
    "Anthropic Claude": {
        "env_key": "ANTHROPIC_API_KEY",
        "model": "claude-sonnet-4-20250514",
        "description": "Paid API. High quality analysis.",
    },
}

# Token settings
MAX_TOKENS_ANALYSIS = 4096
MAX_TOKENS_SCORING = 800
MAX_DOCUMENT_LENGTH = 10000

# App settings
APP_TITLE = "FinePrint AI | Contract Risk Analyzer"
APP_ICON = "chart_with_upwards_trend"

# Risk level definitions
RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
RISK_COLORS = {
    "LOW": "#22c55e",
    "MEDIUM": "#f59e0b",
    "HIGH": "#ef4444",
    "CRITICAL": "#dc2626",
}
RISK_EMOJIS = {
    "LOW": "green_circle",
    "MEDIUM": "yellow_circle",
    "HIGH": "red_circle",
    "CRITICAL": "black_circle",
}
