"""LLM-powered financial document analyzer."""

import json

from .prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT, SCORING_PROMPT
from .config import PROVIDERS, MAX_TOKENS_ANALYSIS, MAX_TOKENS_SCORING, MAX_DOCUMENT_LENGTH


def _call_llm(provider: str, api_key: str, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
    """
    Call the appropriate LLM based on provider selection.

    Args:
        provider: The provider name (key from PROVIDERS dict)
        api_key: API key for the provider
        system_prompt: System prompt for the LLM
        user_prompt: User prompt/message
        max_tokens: Maximum tokens for response

    Returns:
        The LLM response text
    """
    model = PROVIDERS[provider]["model"]

    if "Groq" in provider:
        from groq import Groq
        client = Groq(api_key=api_key)
        message = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return message.choices[0].message.content

    elif "Gemini" in provider:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_prompt,
        )
        response = model_instance.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens),
        )
        return response.text

    elif "Anthropic" in provider:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text

    else:
        raise ValueError(f"Unknown provider: {provider}")


def analyze_document(document_text: str, api_key: str, provider: str = "Groq (Free)") -> str:
    """
    Analyze a financial document using an LLM as a Senior Consumer Rights Attorney.

    Args:
        document_text: The financial agreement text to analyze
        api_key: API key for the selected provider
        provider: The LLM provider to use

    Returns:
        Risk Scorecard analysis as formatted markdown
    """
    if not document_text.strip():
        return "Please provide a document to analyze."

    if not api_key:
        return "Please provide your API key."

    return _call_llm(
        provider=provider,
        api_key=api_key,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=ANALYSIS_PROMPT.format(document_text=document_text),
        max_tokens=MAX_TOKENS_ANALYSIS,
    )


def get_risk_scores(document_text: str, api_key: str, provider: str = "Groq (Free)") -> dict | None:
    """
    Get individual risk scores for each category.

    Args:
        document_text: The financial agreement text
        api_key: API key for the selected provider
        provider: The LLM provider to use

    Returns:
        Dictionary with risk scores for each category, or None on failure
    """
    if not document_text.strip() or not api_key:
        return None

    response_text = _call_llm(
        provider=provider,
        api_key=api_key,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=SCORING_PROMPT.format(document_text=document_text[:MAX_DOCUMENT_LENGTH]),
        max_tokens=MAX_TOKENS_SCORING,
    )

    try:
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        return json.loads(response_text)
    except json.JSONDecodeError:
        return None
