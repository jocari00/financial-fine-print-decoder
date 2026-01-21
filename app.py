"""
Financial Fine-Print Decoder
A professional fintech dashboard for analyzing financial agreements.
"""

import os
import io
import streamlit as st
from src.fineprint import analyze_document, get_risk_scores, PROVIDERS


def extract_text_from_file(uploaded_file) -> str:
    """Extract text from uploaded file (PDF, DOCX, or TXT)."""
    file_type = uploaded_file.type
    file_name = uploaded_file.name.lower()

    try:
        # Plain text files
        if file_type == "text/plain" or file_name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")

        # PDF files
        elif file_type == "application/pdf" or file_name.endswith(".pdf"):
            import pdfplumber
            text_parts = []
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            return "\n\n".join(text_parts)

        # Word documents
        elif file_name.endswith(".docx") or "wordprocessingml" in file_type:
            from docx import Document
            doc = Document(io.BytesIO(uploaded_file.read()))
            return "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])

        else:
            return f"Unsupported file type: {file_type}"

    except Exception as e:
        return f"Error reading file: {str(e)}"

# Page configuration
st.set_page_config(
    page_title="FinePrint AI | Contract Risk Analyzer",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional fintech CSS styling
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .sub-header {
        color: #8892b0;
        font-size: 1.1rem;
        margin-top: 0;
    }

    /* Risk cards */
    .risk-card {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }

    .risk-critical {
        background: linear-gradient(135deg, rgba(220,38,38,0.2) 0%, rgba(127,29,29,0.2) 100%);
        border: 1px solid #dc2626;
        border-radius: 12px;
        padding: 20px;
    }

    .risk-high {
        background: linear-gradient(135deg, rgba(239,68,68,0.15) 0%, rgba(185,28,28,0.15) 100%);
        border: 1px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
    }

    .risk-medium {
        background: linear-gradient(135deg, rgba(245,158,11,0.15) 0%, rgba(180,83,9,0.15) 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
    }

    .risk-low {
        background: linear-gradient(135deg, rgba(34,197,94,0.15) 0%, rgba(21,128,61,0.15) 100%);
        border: 1px solid #22c55e;
        border-radius: 12px;
        padding: 20px;
    }

    /* Metric cards */
    .metric-container {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        text-align: center;
    }

    .metric-label {
        color: #8892b0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
    }

    .metric-delta {
        font-size: 0.8rem;
        margin-top: 4px;
    }

    /* Status badges */
    .status-critical { color: #dc2626; }
    .status-high { color: #ef4444; }
    .status-medium { color: #f59e0b; }
    .status-low { color: #22c55e; }

    /* Sidebar styling */
    .sidebar-section {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .step-number {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.85rem;
        margin-right: 10px;
    }

    /* Document input area */
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'SF Mono', 'Fira Code', monospace !important;
        font-size: 13px !important;
    }

    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.1) !important;
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 12px !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sample document
SAMPLE_DOCUMENT = """CREDIT CARD AGREEMENT - TERMS AND CONDITIONS
Premier Rewards Card

========== INTEREST RATES ==========
ANNUAL PERCENTAGE RATE (APR) FOR PURCHASES: 24.99% variable, based on Prime Rate
PENALTY APR: 29.99% variable. This APR may be applied to your account if you make a late payment.
How Long Will the Penalty APR Apply? If your APRs are increased for any reason, the Penalty APR will apply indefinitely.

========== FEES ==========
ANNUAL FEE: $0 for the first year, then $95.

TRANSACTION FEES:
- Balance Transfer: 3% of each transfer (minimum $5)
- Cash Advance: 5% of each advance (minimum $10)
- Foreign Transaction: 3% of each transaction

PENALTY FEES:
- Late Payment: Up to $40
- Returned Payment: Up to $40

========== TERMS AND CONDITIONS ==========

1. ARBITRATION AGREEMENT AND CLASS ACTION WAIVER
PLEASE READ THIS SECTION CAREFULLY. IT AFFECTS YOUR LEGAL RIGHTS.

You and we agree that any dispute, claim or controversy arising from or relating to this Agreement will be resolved by binding arbitration administered by the American Arbitration Association, rather than in court.

YOU ARE WAIVING YOUR RIGHT TO A JURY TRIAL AND YOUR RIGHT TO PARTICIPATE IN A CLASS ACTION. You may not act as a class representative or participate as a member of a class of claimants.

The arbitrator's decision will be final and binding. The arbitration will take place in our headquarters city unless we agree otherwise.

2. CHANGE OF TERMS
We may change the terms of this Agreement, including the APRs, at any time for any reason. Changes to APR, fees, and other terms will be effective immediately for future transactions and may apply to your existing balance with 45 days notice.

3. DEFAULT AND ACCELERATION
You will be in default if you fail to make any minimum payment by the due date, exceed your credit limit, make a payment that is returned, or file for bankruptcy. Upon default, we may declare your entire balance immediately due and payable.

4. CROSS-DEFAULT PROVISION
Default on this account or any other account you have with us or our affiliates may, at our sole discretion, result in default on all your accounts with us.

5. INFORMATION SHARING AND PRIVACY
We collect personal information including your name, address, Social Security number, income, employment information, and transaction history.

We may share your personal information with:
- Our affiliates for marketing purposes
- Third-party service providers
- Other financial institutions for joint marketing
- Credit bureaus
- Third parties who purchase our assets

We may share and sell aggregated and de-identified transaction data with third-party data brokers for marketing analytics and research purposes.

To opt out of affiliate marketing sharing, you must call 1-800-XXX-XXXX within 30 days of account opening. You cannot opt out of information sharing with service providers or credit bureaus.

6. ACCOUNT MONITORING
We may monitor and record your phone calls and electronic communications for quality assurance and may use this data to develop and improve our services and products.

7. AUTOMATIC RENEWAL
This card automatically renews each year unless you provide written notice of cancellation at least 45 days before your renewal date. The annual fee is non-refundable once charged."""

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'risk_scores' not in st.session_state:
    st.session_state.risk_scores = None
if 'document_text' not in st.session_state:
    st.session_state.document_text = ""

# ============== SIDEBAR ==============
with st.sidebar:
    # Logo/Brand
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin-bottom: 12px;">
            <span style="color: white; font-weight: 800; font-size: 1.4rem;">FP</span>
        </div>
        <h2 style="margin: 10px 0 5px 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">FinePrint AI</h2>
        <p style="color: #8892b0; font-size: 0.85rem; margin: 0;">Contract Risk Analyzer</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # API Configuration
    st.markdown("#### API Configuration")

    # Provider selector
    selected_provider = st.selectbox(
        "Select AI Provider",
        options=list(PROVIDERS.keys()),
        help="Choose your preferred AI provider"
    )

    # Show provider description
    st.caption(PROVIDERS[selected_provider]["description"])

    # API key input
    env_key = PROVIDERS[selected_provider]["env_key"]
    env_api_key = os.getenv(env_key, "")

    api_key = st.text_input(
        "API Key",
        type="password",
        value=env_api_key,
        placeholder="Enter your API key...",
        help=f"Get your key from the provider's console. Or set {env_key} in .env"
    )

    if api_key:
        st.success("API key configured")
    else:
        st.warning("Enter API key to begin")

    # Store in session state
    st.session_state.selected_provider = selected_provider
    st.session_state.api_key = api_key

    st.divider()

    # How to Use section
    st.markdown("#### How to Use")

    with st.expander("**Step-by-step Guide**", expanded=False):
        st.markdown("""
        <div style="padding: 10px 0;">
            <p><span class="step-number">1</span><strong>Select Provider</strong></p>
            <p style="color: #8892b0; font-size: 0.85rem; margin-left: 38px;">Choose Groq (free), Gemini (free), or Anthropic</p>
        </div>
        <div style="padding: 10px 0;">
            <p><span class="step-number">2</span><strong>Enter API Key</strong></p>
            <p style="color: #8892b0; font-size: 0.85rem; margin-left: 38px;">Get a free key from your provider</p>
        </div>
        <div style="padding: 10px 0;">
            <p><span class="step-number">3</span><strong>Paste Document</strong></p>
            <p style="color: #8892b0; font-size: 0.85rem; margin-left: 38px;">Copy & paste your financial agreement</p>
        </div>
        <div style="padding: 10px 0;">
            <p><span class="step-number">4</span><strong>Analyze</strong></p>
            <p style="color: #8892b0; font-size: 0.85rem; margin-left: 38px;">Click analyze and review your Risk Scorecard</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("**What We Analyze**", expanded=False):
        st.markdown("""
        **Hidden Fees**
        Fees buried in fine print, not shown in headers

        **Arbitration Clauses**
        Your right to sue, class action eligibility

        **Variable Rates**
        How easily they can raise your rates

        **Privacy & Data**
        What personal data they sell or share
        """)

    with st.expander("**Understanding Risk Levels**", expanded=False):
        st.markdown("""
        <div style="padding: 8px 0;">
            <span style="color: #22c55e; font-weight: bold;">●</span> <strong>LOW</strong>
            <p style="color: #8892b0; font-size: 0.85rem; margin: 4px 0 0 28px;">Consumer-friendly terms</p>
        </div>
        <div style="padding: 8px 0;">
            <span style="color: #f59e0b; font-weight: bold;">●</span> <strong>MEDIUM</strong>
            <p style="color: #8892b0; font-size: 0.85rem; margin: 4px 0 0 28px;">Some concerning clauses</p>
        </div>
        <div style="padding: 8px 0;">
            <span style="color: #ef4444; font-weight: bold;">●</span> <strong>HIGH</strong>
            <p style="color: #8892b0; font-size: 0.85rem; margin: 4px 0 0 28px;">Significant consumer risks</p>
        </div>
        <div style="padding: 8px 0;">
            <span style="color: #dc2626; font-weight: bold;">●</span> <strong>CRITICAL</strong>
            <p style="color: #8892b0; font-size: 0.85rem; margin: 4px 0 0 28px;">Major red flags detected</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Disclaimer
    st.caption("""
    **Disclaimer**: This tool provides AI-powered analysis for informational purposes only.
    It does not constitute legal advice. Always consult a licensed attorney for legal guidance.
    """)

# ============== MAIN CONTENT ==============

# Header
st.markdown("""
<div style="display: flex; align-items: center; gap: 16px; margin-bottom: 8px;">
    <div style="display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; flex-shrink: 0;">
        <span style="color: white; font-weight: 800; font-size: 1.2rem;">FP</span>
    </div>
    <div>
        <h1 class="main-header" style="margin: 0;">Financial Fine-Print Decoder</h1>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered contract analysis by a Senior Consumer Rights Attorney</p>', unsafe_allow_html=True)

st.markdown("")

# Main layout - changes based on whether analysis is complete
if not st.session_state.analysis_complete:
    # INPUT MODE: Show document input prominently

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Add Your Financial Document")
        st.markdown("*Credit card agreements, loan contracts, terms of service...*")

        # Tabs for input method
        tab_paste, tab_upload = st.tabs(["Paste Text", "Upload File"])

        document_input = ""

        with tab_paste:
            # Check if we should load sample
            default_text = SAMPLE_DOCUMENT if st.session_state.get("load_sample", False) else ""
            if st.session_state.get("load_sample", False):
                st.session_state.load_sample = False

            pasted_text = st.text_area(
                "Document Text",
                value=default_text,
                height=350,
                placeholder="Paste your financial agreement here...\n\nSupported documents:\n- Credit card agreements\n- Loan contracts\n- Mortgage terms\n- Account terms & conditions\n- Any financial fine print",
                label_visibility="collapsed"
            )
            if pasted_text:
                document_input = pasted_text

        with tab_upload:
            uploaded_file = st.file_uploader(
                "Upload a document",
                type=["pdf", "txt", "docx"],
                help="Supported formats: PDF, TXT, DOCX"
            )
            if uploaded_file:
                with st.spinner("Extracting text from file..."):
                    extracted_text = extract_text_from_file(uploaded_file)
                    if extracted_text and not extracted_text.startswith("Error"):
                        document_input = extracted_text
                        st.success(f"Extracted {len(extracted_text):,} characters from {uploaded_file.name}")
                        with st.expander("Preview extracted text"):
                            st.text(extracted_text[:2000] + ("..." if len(extracted_text) > 2000 else ""))
                    else:
                        st.error(extracted_text)

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Load Sample", use_container_width=True, type="secondary"):
                st.session_state.load_sample = True
                st.rerun()

        with col_btn2:
            analyze_clicked = st.button("Analyze Document", use_container_width=True, type="primary")

    with col2:
        st.markdown("### Quick Preview")

        st.markdown("""
        <div class="risk-card">
            <h4 style="margin-top: 0;">Your Risk Scorecard will include:</h4>
            <p>- Overall risk assessment</p>
            <p>- Hidden fees analysis</p>
            <p>- Arbitration clause review</p>
            <p>- Variable rate risks</p>
            <p>- Privacy & data exposure</p>
            <p>- Top red flags</p>
            <p>- Recommended actions</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.info("**Tip:** Try the sample document to see how the analysis works!")

    # Process analysis
    if analyze_clicked:
        current_api_key = st.session_state.get("api_key", "")
        current_provider = st.session_state.get("selected_provider", "Groq (Free)")

        if not current_api_key:
            st.error("Please enter your API key in the sidebar.")
        elif not document_input or not document_input.strip():
            st.warning("Please paste a document to analyze.")
        else:
            st.session_state.document_text = document_input

            with st.status(f"Analyzing with {current_provider}...", expanded=True) as status:
                st.write("Performing quick risk assessment...")
                scores = get_risk_scores(document_input, current_api_key, current_provider)
                st.session_state.risk_scores = scores

                st.write("Generating detailed analysis...")
                analysis = analyze_document(document_input, current_api_key, current_provider)
                st.session_state.analysis_result = analysis

                st.session_state.analysis_complete = True
                status.update(label="Analysis complete!", state="complete", expanded=False)

            st.rerun()

else:
    # RESULTS MODE: Show analysis results with document in expander

    scores = st.session_state.risk_scores
    analysis = st.session_state.analysis_result

    # Overall Risk Banner
    if scores:
        overall = scores.get('overall_risk', 'UNKNOWN')
        risk_class = f"risk-{overall.lower()}"
        verdict = scores.get('one_line_verdict', '')

        st.markdown(f"""
        <div class="{risk_class}">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                <div>
                    <span style="font-size: 2rem; font-weight: 800;">Overall Risk: {overall}</span>
                </div>
            </div>
            <p style="margin-top: 15px; font-size: 1.1rem; color: #cbd5e1;">{verdict}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Risk Metrics Dashboard
        st.markdown("### Risk Breakdown")

        metric_cols = st.columns(4)

        risk_colors = {
            'LOW': '#22c55e',
            'MEDIUM': '#f59e0b',
            'HIGH': '#ef4444',
            'CRITICAL': '#dc2626'
        }

        # Hidden Fees
        with metric_cols[0]:
            hf = scores.get('hidden_fees', {})
            hf_risk = hf.get('risk', 'N/A')
            hf_color = risk_colors.get(hf_risk, '#8892b0')

            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Hidden Fees</div>
                <div class="metric-value" style="color: {hf_color};">{hf_risk}</div>
                <div class="metric-delta" style="color: {hf_color};">{hf.get('count', '?')} fees found</div>
            </div>
            """, unsafe_allow_html=True)

        # Arbitration
        with metric_cols[1]:
            arb = scores.get('arbitration', {})
            arb_risk = arb.get('risk', 'N/A')
            arb_color = risk_colors.get(arb_risk, '#8892b0')
            can_sue = "Yes" if arb.get('can_sue') else "No"

            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Arbitration</div>
                <div class="metric-value" style="color: {arb_color};">{arb_risk}</div>
                <div class="metric-delta">Can Sue: {can_sue}</div>
            </div>
            """, unsafe_allow_html=True)

        # Variable Rates
        with metric_cols[2]:
            vr = scores.get('variable_rates', {})
            vr_risk = vr.get('risk', 'N/A')
            vr_color = risk_colors.get(vr_risk, '#8892b0')
            rate_type = "Variable" if vr.get('is_variable') else "Fixed"

            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Rate Risk</div>
                <div class="metric-value" style="color: {vr_color};">{vr_risk}</div>
                <div class="metric-delta">{rate_type}</div>
            </div>
            """, unsafe_allow_html=True)

        # Privacy
        with metric_cols[3]:
            priv = scores.get('privacy', {})
            priv_risk = priv.get('risk', 'N/A')
            priv_color = risk_colors.get(priv_risk, '#8892b0')
            sells = priv.get('sells_data')
            sells_str = "Sells Data" if sells == True else ("Safe" if sells == False else "Unclear")

            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Privacy</div>
                <div class="metric-value" style="color: {priv_color};">{priv_risk}</div>
                <div class="metric-delta">{sells_str}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.divider()

    # Document in expander (collapsed by default after analysis)
    with st.expander("**View Original Document**", expanded=False):
        st.code(st.session_state.document_text, language=None)

    st.markdown("")

    # Full Analysis
    st.markdown("### Detailed Analysis")

    # Convert markdown to HTML-friendly format for proper rendering
    import re

    def render_analysis(text):
        """Convert markdown + HTML mix to renderable HTML."""
        # Convert markdown headers to HTML
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2 style="color: #e2e8f0; margin-top: 1.5rem;">\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'<h3 style="color: #cbd5e1;">\1</h3>', text, flags=re.MULTILINE)
        # Convert bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Convert italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Convert markdown list items to HTML
        text = re.sub(r'^- (.+)$', r'<li style="margin-left: 1rem; color: #94a3b8;">\1</li>', text, flags=re.MULTILINE)
        # Convert horizontal rules
        text = re.sub(r'^---+$', r'<hr style="border-color: rgba(255,255,255,0.1); margin: 1.5rem 0;">', text, flags=re.MULTILINE)
        # Convert newlines to breaks for proper spacing
        text = text.replace('\n\n', '</p><p style="color: #94a3b8; line-height: 1.6;">')
        return f'<div style="color: #94a3b8; line-height: 1.6;"><p style="color: #94a3b8;">{text}</p></div>'

    st.markdown(render_analysis(analysis), unsafe_allow_html=True)

    st.markdown("")
    st.divider()

    # Action buttons
    col_action1, col_action2, col_action3 = st.columns([1, 1, 2])

    with col_action1:
        if st.button("Analyze New Document", use_container_width=True, type="primary"):
            st.session_state.analysis_complete = False
            st.session_state.analysis_result = None
            st.session_state.risk_scores = None
            st.session_state.document_text = ""
            st.rerun()

    with col_action2:
        if st.button("Copy Analysis", use_container_width=True):
            st.toast("Analysis copied to clipboard!")

# Footer
st.markdown("")
st.divider()
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 8px;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 6px;">
            <span style="color: white; font-weight: 700; font-size: 0.7rem;">FP</span>
        </div>
        <span style="color: #8892b0; font-size: 0.85rem;"><strong>FinePrint AI</strong> | Multi-Provider AI Analysis</span>
    </div>
    <p style="color: #64748b; font-size: 0.75rem; margin-top: 8px;">
        For informational purposes only | Not legal advice | Consult a licensed attorney
    </p>
</div>
""", unsafe_allow_html=True)
