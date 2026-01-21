# FinePrint AI

AI-powered financial contract risk analyzer. Analyze credit card agreements, loan contracts, and other financial documents to identify hidden risks and protect your interests.

## Features

- **Hidden Fees Detection** - Identifies fees buried in fine print that aren't prominently disclosed
- **Arbitration Clause Analysis** - Determines if you can sue in court or are bound to arbitration
- **Variable Rate Assessment** - Analyzes how easily terms and rates can change
- **Privacy & Data Review** - Identifies what personal data is collected and shared

## Requirements

- Python 3.10+
- Anthropic API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/financial-fine-print-decoder.git
cd financial-fine-print-decoder
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### How to Use

1. Enter your Anthropic API key in the sidebar
2. Paste a financial document (credit card agreement, loan contract, etc.)
3. Click "Analyze Document"
4. Review your Risk Scorecard with detailed findings

## Project Structure

```
financial-fine-print-decoder/
├── app.py                 # Main Streamlit application
├── src/
│   └── fineprint/
│       ├── analyzer.py    # Document analysis logic
│       ├── config.py      # Configuration settings
│       └── prompts.py     # LLM prompt templates
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata
└── .env.example           # Environment template
```

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Claude (Anthropic API)
- **Language**: Python 3.10+

## Disclaimer

This tool provides AI-powered analysis for informational purposes only. It does not constitute legal advice. Always consult a licensed attorney for legal guidance regarding financial agreements.

## License

MIT License
