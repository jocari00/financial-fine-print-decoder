"""Financial Fine-Print Decoder - AI-powered contract risk analysis."""

from .analyzer import analyze_document, get_risk_scores
from .config import PROVIDERS

__all__ = ["analyze_document", "get_risk_scores", "PROVIDERS"]
__version__ = "1.0.0"
