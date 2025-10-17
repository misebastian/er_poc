import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Entity Resolution Match Labelling", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with better readability
st.markdown("""
<style>
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* Main background - dark */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* All text white by default */
    * {
        color: #fafafa !important;
    }
    
    /* Sidebar styling - darker */
    [data-testid="stSidebar"] {
        background-color: #1a1d24;
        border-right: 1px solid #2d3139;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #2d3139;
        color: #fafafa !important;
        border: none;
        text-align: left;
        font-size: 14px;
        padding: 10px 14px;
        border-radius: 6px;
        width: 100%;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #3d4149;
        border-left: 3px solid #4a9eff;
    }
    
    /* Sidebar input */
    [data-testid="stSidebar"] input {
        background-color: #2d3139 !important;
        color: #fafafa !important;
        border: 1px solid #404040 !important;
        font-size: 14px !important;
    }
    
    /* Main action buttons - larger and more prominent */
    div[data-testid="column"] > div > div > div > button {
        height: 50px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        transition: all 0.2s;
    }
    
    /* Confirm button - bright green */
    button[kind="primary"] {
        background-color: #10b981 !important;
        color: white !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #059669 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    
    /* Flag button - orange */
    button[key="flag_btn"] {
        background-color: #f59e0b !important;
        color: white !important;
    }
    
    button[key="flag_btn"]:hover {
        background-color: #d97706 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    }
    
    /* Reject button - red */
    button[key="reject_btn"] {
        background-color: #ef4444 !important;
        color: white !important;
    }
    
    button[key="reject_btn"]:hover {
        background-color: #dc2626 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
    }
    
    /* Metrics - larger and more visible */
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #fafafa !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        color: #9ca3af !important;
        font-weight: 500 !important;
    }
    
    /* Tabs - modern dark style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid #2d3139;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px 6px 0 0;
        color: #9ca3af;
        font-weight: 600;
        padding: 12px 20px;
        font-size: 15px;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e293b;
        color: #3b82f6;
        border-bottom: 3px solid #3b82f6;
    }
    
    /* Container boxes - dark cards */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: #1a1d24;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #2d3139;
    }
    
    /* Headers - larger and clearer */
    h1 {
        color: #fafafa !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    h2 {
        color: #fafafa !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }
    
    h3 {
        color: #fafafa !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    h4 {
        color: #fafafa !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    /* Description text - LARGER for easy reading */
    .caption, [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #d1d5db !important;
    }
    
    /* Property labels - clear and readable */
    strong {
        color: #e5e7eb !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    
    /* Priority badges - high contrast */
    .priority-badge-high {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #991b1b;
    }
    
    .priority-badge-medium {
        background-color: #78350f;
        color: #fcd34d;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #92400e;
    }
    
    .priority-badge-low {
        background-color: #064e3b;
        color: #6ee7b7;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #065f46;
    }
    
    /* Status badges - high contrast */
    .status-badge {
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 700;
        display: inline-block;
    }
    
    .status-confirmed {
        background-color: #064e3b;
        color: #6ee7b7;
        border: 1px solid #065f46;
    }
    
    .status-rejected {
        background-color: #7f1d1d;
        color: #fca5a5;
        border: 1px solid #991b1b;
    }
    
    .status-flagged {
        background-color: #78350f;
        color: #fcd34d;
        border: 1px solid #92400e;
    }
    
    /* Dividers */
    hr {
        border-color: #2d3139 !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Input fields */
    input, textarea, select {
        background-color: #1a1d24 !important;
        color: #fafafa !important;
        border: 1px solid #2d3139 !important;
        font-size: 15px !important;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        font-size: 14px !important;
    }
    
    /* Score percentage - HUGE and prominent */
    .score-display {
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #3b82f6 !important;
        line-height: 1 !important;
    }
    
    /* Entity names - prominent */
    .entity-name {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #fafafa !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Property values - larger */
    .property-value {
        font-size: 16px !important;
        color: #d1d5db !important;
        line-height: 1.8 !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sample company data with realistic BU differentiation
def create_sample_dataset():
    companies_data = [
        # LinkedIn BUs
        {
            "raw": "LinkedIn Australia Pty Ltd",
            "canonical": "LinkedIn",
            "score": 0.92,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "518210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "linkedin.com.au",
            "website_canonical": "linkedin.com",
            "desc_raw": "Professional networking platform - Australia regional operations",
            "desc_canonical": "Global professional networking and career development platform"
        },
        {
            "raw": "LinkedIn Sales Navigator",
            "canonical": "LinkedIn",
            "score": 0.88,
            "priority": "High",
            "naics_raw": "541613",
            "naics_canonical": "518210",
            "sic_raw": "7389",
            "sic_canonical": "7372",
            "website_raw": "business.linkedin.com/sales-solutions",
            "website_canonical": "linkedin.com",
            "desc_raw": "Sales intelligence and prospecting software tool - B2B sales enablement",
            "desc_canonical": "Global professional networking and career development platform"
        },
        {
            "raw": "LinkedIn Talent Solutions",
            "canonical": "LinkedIn",
            "score": 0.90,
            "priority": "High",
            "naics_raw": "561311",
            "naics_canonical": "518210",
            "sic_raw": "7361",
            "sic_canonical": "7372",
            "website_raw": "business.linkedin.com/talent-solutions",
            "website_canonical": "linkedin.com",
            "desc_raw": "Recruiting and talent acquisition platform for enterprise hiring",
            "desc_canonical": "Global professional networking and career development platform"
        },
        {
            "raw": "LinkedIn Learning",
            "canonical": "LinkedIn",
            "score": 0.85,
            "priority": "Medium",
            "naics_raw": "611710",
            "naics_canonical": "518210",
            "sic_raw": "8299",
            "sic_canonical": "7372",
            "website_raw": "learning.linkedin.com",
            "website_canonical": "linkedin.com",
            "desc_raw": "Online learning platform offering professional development courses",
            "desc_canonical": "Global professional networking and career development platform"
        },
        # Amazon BUs
        {
            "raw": "Amazon Web Services Inc",
            "canonical": "Amazon",
            "score": 0.89,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "454110",
            "sic_raw": "7374",
            "sic_canonical": "5961",
            "website_raw": "aws.amazon.com",
            "website_canonical": "amazon.com",
            "desc_raw": "Cloud computing infrastructure and services platform - IaaS/PaaS provider",
            "desc_canonical": "Global e-commerce and technology conglomerate"
        },
        {
            "raw": "AWS EMEA SARL",
            "canonical": "Amazon",
            "score": 0.87,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "454110",
            "sic_raw": "7374",
            "sic_canonical": "5961",
            "website_raw": "aws.amazon.com/emea",
            "website_canonical": "amazon.com",
            "desc_raw": "AWS cloud services - Europe, Middle East, and Africa operations",
            "desc_canonical": "Global e-commerce and technology conglomerate"
        },
        {
            "raw": "Amazon Retail LLC",
            "canonical": "Amazon",
            "score": 0.96,
            "priority": "High",
            "naics_raw": "454110",
            "naics_canonical": "454110",
            "sic_raw": "5961",
            "sic_canonical": "5961",
            "website_raw": "amazon.com",
            "website_canonical": "amazon.com",
            "desc_raw": "Online retail and e-commerce marketplace operations",
            "desc_canonical": "Global e-commerce and technology conglomerate"
        },
        {
            "raw": "Amazon Advertising",
            "canonical": "Amazon",
            "score": 0.88,
            "priority": "High",
            "naics_raw": "541810",
            "naics_canonical": "454110",
            "sic_raw": "7311",
            "sic_canonical": "5961",
            "website_raw": "advertising.amazon.com",
            "website_canonical": "amazon.com",
            "desc_raw": "Digital advertising platform and marketing services division",
            "desc_canonical": "Global e-commerce and technology conglomerate"
        },
        # Microsoft BUs
        {
            "raw": "Microsoft Corporation",
            "canonical": "Microsoft",
            "score": 0.98,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "microsoft.com",
            "website_canonical": "microsoft.com",
            "desc_raw": "Software and cloud computing services - corporate headquarters",
            "desc_canonical": "Global technology corporation developing software, hardware, and cloud services"
        },
        {
            "raw": "Microsoft Azure Services",
            "canonical": "Microsoft",
            "score": 0.85,
            "priority": "Medium",
            "naics_raw": "518210",
            "naics_canonical": "511210",
            "sic_raw": "7374",
            "sic_canonical": "7372",
            "website_raw": "azure.microsoft.com",
            "website_canonical": "microsoft.com",
            "desc_raw": "Public cloud computing platform - infrastructure and platform services",
            "desc_canonical": "Global technology corporation developing software, hardware, and cloud services"
        },
        {
            "raw": "Microsoft Dynamics 365",
            "canonical": "Microsoft",
            "score": 0.83,
            "priority": "Medium",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "dynamics.microsoft.com",
            "website_canonical": "microsoft.com",
            "desc_raw": "Enterprise resource planning and CRM software suite",
            "desc_canonical": "Global technology corporation developing software, hardware, and cloud services"
        },
        # Google BUs
        {
            "raw": "Google LLC",
            "canonical": "Google",
            "score": 0.97,
            "priority": "High",
            "naics_raw": "519130",
            "naics_canonical": "519130",
            "sic_raw": "7375",
            "sic_canonical": "7375",
            "website_raw": "google.com",
            "website_canonical": "google.com",
            "desc_raw": "Internet search engine and online advertising services",
            "desc_canonical": "Multinational technology company specializing in Internet services and products"
        },
        {
            "raw": "Google Cloud Platform",
            "canonical": "Google",
            "score": 0.89,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "519130",
            "sic_raw": "7374",
            "sic_canonical": "7375",
            "website_raw": "cloud.google.com",
            "website_canonical": "google.com",
            "desc_raw": "Cloud computing infrastructure and platform services - enterprise solutions",
            "desc_canonical": "Multinational technology company specializing in Internet services and products"
        },
        {
            "raw": "YouTube LLC",
            "canonical": "Google",
            "score": 0.82,
            "priority": "Medium",
            "naics_raw": "519130",
            "naics_canonical": "519130",
            "sic_raw": "7375",
            "sic_canonical": "7375",
            "website_raw": "youtube.com",
            "website_canonical": "google.com",
            "desc_raw": "Video sharing and social media platform - user-generated content",
            "desc_canonical": "Multinational technology company specializing in Internet services and products"
        },
        # Salesforce BUs
        {
            "raw": "Salesforce.com Inc",
            "canonical": "Salesforce",
            "score": 0.96,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "salesforce.com",
            "website_canonical": "salesforce.com",
            "desc_raw": "Cloud-based customer relationship management (CRM) software platform",
            "desc_canonical": "Enterprise cloud computing and CRM software solutions provider"
        },
        {
            "raw": "Tableau Software LLC",
            "canonical": "Salesforce",
            "score": 0.74,
            "priority": "Medium",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "tableau.com",
            "website_canonical": "salesforce.com",
            "desc_raw": "Business intelligence and data visualization analytics platform",
            "desc_canonical": "Enterprise cloud computing and CRM software solutions provider"
        },
        {
            "raw": "Slack Technologies Inc",
            "canonical": "Salesforce",
            "score": 0.71,
            "priority": "Low",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "slack.com",
            "website_canonical": "salesforce.com",
            "desc_raw": "Business communication and team collaboration software platform",
            "desc_canonical": "Enterprise cloud computing and CRM software solutions provider"
        },
        {
            "raw": "Oracle Corporation",
            "canonical": "Oracle",
            "score": 0.97,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "oracle.com",
            "website_canonical": "oracle.com",
            "desc_raw": "Enterprise database management systems and cloud computing solutions",
            "desc_canonical": "Global provider of database software and cloud computing systems"
        },
        {
            "raw": "Adobe Inc",
            "canonical": "Adobe",
            "score": 0.98,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "adobe.com",
            "website_canonical": "adobe.com",
            "desc_raw": "Creative software and digital media production tools - corporate entity",
            "desc_canonical": "Digital media and marketing software solutions company"
        },
        {
            "raw": "Meta Platforms Inc",
            "canonical": "Meta",
            "score": 0.97,
            "priority": "High",
            "naics_raw": "519130",
            "naics_canonical": "519130",
            "sic_raw": "7375",
            "sic_canonical": "7375",
            "website_raw": "meta.com",
            "website_canonical": "meta.com",
            "desc_raw": "Social media and metaverse technology company - corporate entity",
            "desc_canonical": "Social technology and virtual reality company"
        },
    ]
    
    data = []
    for i, company in enumerate(companies_data, 1):
        data.append({
            'id': i,
            'RAW_SUPPLIER': company['raw'],
            'CANONICAL_NAME': company['canonical'],
            'match_score': company['score'],
            'match_priority': company['priority'],
            'naics_code_raw': company['naics_raw'],
            'naics_code_canonical': company['naics_canonical'],
            'sic_code_raw': company['sic_raw'],
            'sic_code_canonical': company['sic_canonical'],
            'website_url_raw': company['website_raw'],
            'website_url_canonical': company['website_canonical'],
            'description_raw': company['desc_raw'],
            'description_canonical': company['desc_canonical'],
            'HITL_Decision': None,
            'last_decision': None,
            'last_decision_by': None,
            'last_decision_date': None,
            'review_status': 'Unreviewed',
            'reviewed_at': None,
            'confidence_level': round(company['score'] * 100)
        })
    
    return pd.DataFrame(data)

# Initialize session state
if 'matches_df' not in st.session_state:
    st.session_state.matches_df = create_sample_dataset()

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if 'change_log' not in st.session_state:
    st.session_state.change_log = []

if 'user_name' not in st.session_state:
    st.session_state.user_name = "Current User"

# Function to log changes
def log_change(match_id, raw_supplier, canonical_name, old_decision, new_decision, user):
    log_entry = {
        'timestamp': datetime.now(),
        'match_id': match_id,
        'raw_supplier': raw_supplier,
        'canonical_name': canonical_name,
        'old_decision': old_decision,
        'new_decision': new_decision,
        'user': user
    }
    st.session_state.change_log.append(log_entry)

# Function to update decision
def update_decision(idx, decision, current_match):
    old_decision = st.session_state.matches_df.at[idx, 'HITL_Decision']
    
    st.session_state.matches_df.at[idx, 'HITL_Decision'] = decision
    st.session_state.matches_df.at[idx, 'last_decision'] = decision
    st.session_state.matches_df.at[idx, 'review_status'] = decision
    st.session_state.matches_df.at[idx, 'last_decision_by'] = st.session_state.user_name
    st.session_state.matches_df.at[idx, 'last_decision_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.matches_df.at[idx, 'reviewed_at'] = datetime.now().strftime("%a, %b %d, %Y, %I:%M %p")
    
    log_change(
        current_match['id'],
        current_match['RAW_SUPPLIER'],
        current_match['CANONICAL_NAME'],
        old_decision,
        decision,
        st.session_state.user_name
    )

# Sidebar
with st.sidebar:
    st.markdown("### Current User")
    st.session_state.user_name = st.text_input("", value=st.session_state.user_name, label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown("### Match Selection")
    
    # Filters
    st.markdown("#### Filter Matches")
    
    priority_filter = st.multiselect(
        "Match Priority",
        options=['High', 'Medium', 'Low'],
        default=['High']
    )
    
    status_filter = st.multiselect(
        "Review Status",
        options=['Unreviewed', 'Confirmed', 'Rejected', 'Flagged'],
        default=['Unreviewed']
    )
    
    score_filter = st.slider(
        "Match Score",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.01
    )
    
    st.markdown("---")
    
    # Apply filters
    df = st.session_state.matches_df
    filtered_df = df[
        (df['match_priority'].isin(priority_filter)) &
        (df['review_status'].isin(status_filter)) &
        (df['match_score'] >= score_filter[0]) &
        (df['match_score'] <= score_filter[1])
    ].reset_index(drop=True)
    
    st.markdown(f"### Matches ({len(filtered_df)})")
    
    # Match list
    for idx, row in filtered_df.iterrows():
        status_icons = {
            'Confirmed': '⚪',
            'Rejected': '⚪',
            'Flagged': '⚪',
            'Unreviewed': '⚪'
        }
        
        button_label = f"{status_icons[row['review_status']]} {row['RAW_SUPPLIER'][:30]}..."
        
        if st.button(button_label, key=f"match_{idx}", use_container_width=True):
            st.session_state.current_index = idx

# Main content
st.markdown("## [ERP Migration] Entity Resolution Match Labelling")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Individual Match Review", 
    "📊 Dataset View & Query", 
    "📜 Change History Log",
    "📈 Analytics"
])

with tab1:
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        unreviewed = len(df[df['review_status'] == 'Unreviewed'])
        st.metric("Unreviewed Matches", unreviewed)
    with col2:
        confirmed = len(df[df['HITL_Decision'] == 'Confirmed'])
        st.metric("Confirmed Matches", confirmed)
    with col3:
        rejected = len(df[df['HITL_Decision'] == 'Rejected'])
        st.metric("Rejected Matches", rejected)
    with col4:
        flagged = len(df[df['HITL_Decision'] == 'Flagged'])
        st.metric("Flagged Matches", flagged)
    
    st.markdown("---")
    
    if len(filtered_df) > 0:
        current_match = filtered_df.iloc[st.session_state.current_index]
        original_idx = df[df['id'] == current_match['id']].index[0]
        
        st.markdown("### Review Match")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Confirm Match", use_container_width=True, type="primary", key="confirm_btn"):
                update_decision(original_idx, 'Confirmed', current_match)
                st.rerun()
        
        with col2:
            if st.button("🚩 Flag Match", use_container_width=True, key="flag_btn"):
                update_decision(original_idx, 'Flagged', current_match)
                st.rerun()
        
        with col3:
            if st.button("❌ Reject Match", use_container_width=True, key="reject_btn"):
                update_decision(original_idx, 'Rejected', current_match)
                st.rerun()
        
        st.markdown("---")
        
        # Score and status
        col1, col2 = st.columns([1, 3])
        with col1:
            score_pct = int(current_match['match_score'] * 100)
            st.markdown(f"<div class='score-display'>{score_pct}%</div>", unsafe_allow_html=True)
            st.caption("Overall Score")
        
        with col2:
            decision = current_match['HITL_Decision'] if pd.notna(current_match['HITL_Decision']) else 'Unreviewed'
            status_class = {
                'Confirmed': 'status-confirmed',
                'Rejected': 'status-rejected',
                'Flagged': 'status-flagged',
                'Unreviewed': ''
            }.get(decision, '')
            
            if status_class:
                st.markdown(f'<div class="status-badge {status_class}">{decision}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"### ⚪ {decision}")
            st.markdown("")
            st.caption(f"Predicated Label | Confirmation Probability: {current_match['confidence_level']}%")
        
        st.markdown("---")
        
        # Match details
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**Match Priority**")
            priority = current_match['match_priority']
            priority_class = f"priority-badge-{priority.lower()}"
            st.markdown(f'<div class="{priority_class}">{priority}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Review Status**")
            st.markdown(current_match['review_status'])
        
        with col3:
            st.markdown("**Match At**")
            if current_match['reviewed_at']:
                st.caption(current_match['reviewed_at'])
            else:
                st.caption("Not reviewed yet")
        
        with col4:
            st.markdown("**ER Score Table**")
            st.markdown("🔵 Supplier Deduplication")
        
        st.markdown("---")
        
        # Entity comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Left Entity")
            st.markdown(f"<div class='entity-name'>{current_match['RAW_SUPPLIER']}</div>", unsafe_allow_html=True)
            st.caption("🔵 [ERP Migration] Supplier")
            st.markdown("")
            
            with st.container():
                st.markdown("**Overview** | Properties")
                st.markdown("---")
                st.markdown("#### Properties")
                st.markdown("")
                st.markdown(f"<div class='property-value'><strong>NAICS Code:</strong> {current_match['naics_code_raw']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='property-value'><strong>SIC Code:</strong> {current_match['sic_code_raw']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='property-value'><strong>Website URL:</strong> {current_match['website_url_raw']}</div>", unsafe_allow_html=True)
                st.markdown("")
                st.markdown("**Short Description:**")
                st.markdown(f"<div class='property-value' style='font-size: 17px; line-height: 1.7;'>{current_match['description_raw']}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📥 Right Entity")
            st.markdown(f"<div class='entity-name'>{current_match['CANONICAL_NAME']}</div>", unsafe_allow_html=True)
            st.caption("🔵 [ERP Migration] Supplier")
            st.markdown("")
            
            with st.container():
                st.markdown("**Overview** | Properties")
                st.markdown("---")
                st.markdown("#### Properties")
                st.markdown("")
                st.markdown(f"<div class='property-value'><strong>NAICS Code:</strong> {current_match['naics_code_canonical']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='property-value'><strong>SIC Code:</strong> {current_match['sic_code_canonical']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='property-value'><strong>Website URL:</strong> {current_match['website_url_canonical']}</div>", unsafe_allow_html=True)
                st.markdown("")
                st.markdown("**Short Description:**")
                st.markdown(f"<div class='property-value' style='font-size: 17px; line-height: 1.7;'>{current_match['description_canonical']}</div>", unsafe_allow_html=True)
        
        # Navigation
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_index == 0):
                st.session_state.current_index -= 1
                st.rerun()
        
        with col2:
            st.markdown(f"<center>Match {st.session_state.current_index + 1} of {len(filtered_df)}</center>", 
                       unsafe_allow_html=True)
        
        with col3:
            if st.button("Next ➡️", disabled=st.session_state.current_index >= len(filtered_df) - 1):
                st.session_state.current_index += 1
                st.rerun()
    
    else:
        st.info("No matches found with the current filters.")

with tab2:
    st.markdown("### Dataset View & Query")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        query_canonical = st.multiselect(
            "Filter by Canonical Name",
            options=sorted(df['CANONICAL_NAME'].unique())
        )
    
    with col2:
        query_decision = st.multiselect(
            "Filter by HITL Decision",
            options=['Confirmed', 'Rejected', 'Flagged', 'Unreviewed']
        )
    
    with col3:
        query_priority = st.multiselect(
            "Filter by Priority",
            options=['High', 'Medium', 'Low']
        )
    
    query_text = st.text_input("🔎 Search in Raw Supplier", "")
    
    queried_df = df.copy()
    
    if query_canonical:
        queried_df = queried_df[queried_df['CANONICAL_NAME'].isin(query_canonical)]
    
    if query_decision:
        if 'Unreviewed' in query_decision:
            queried_df = queried_df[
                (queried_df['HITL_Decision'].isin([d for d in query_decision if d != 'Unreviewed'])) |
                (queried_df['HITL_Decision'].isna())
            ]
        else:
            queried_df = queried_df[queried_df['HITL_Decision'].isin(query_decision)]
    
    if query_priority:
        queried_df = queried_df[queried_df['match_priority'].isin(query_priority)]
    
    if query_text:
        queried_df = queried_df[
            queried_df['RAW_SUPPLIER'].str.contains(query_text, case=False, na=False)
        ]
    
    st.markdown(f"#### Results: {len(queried_df)} matches")
    
    columns_to_show = st.multiselect(
        "Select columns to display",
        options=list(queried_df.columns),
        default=['id', 'RAW_SUPPLIER', 'CANONICAL_NAME', 'match_score', 
                'HITL_Decision', 'naics_code_raw', 'sic_code_raw']
    )
    
    if columns_to_show:
        st.dataframe(
            queried_df[columns_to_show],
            use_container_width=True,
            height=400
        )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(queried_df))
    with col2:
        confirmed_count = len(queried_df[queried_df['HITL_Decision'] == 'Confirmed'])
        st.metric("Confirmed", confirmed_count)
    with col3:
        rejected_count = len(queried_df[queried_df['HITL_Decision'] == 'Rejected'])
        st.metric("Rejected", rejected_count)
    with col4:
        avg_score = queried_df['match_score'].mean()
        st.metric("Avg Score", f"{avg_score:.2%}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Query Results"):
            csv = queried_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Export Full Dataset"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Full Dataset CSV",
                data=csv,
                file_name=f"full_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

with tab3:
    st.markdown("### Change History Log")
    
    if st.session_state.change_log:
        col1, col2 = st.columns(2)
        
        with col1:
            users = list(set([log['user'] for log in st.session_state.change_log]))
            filter_user = st.multiselect("Filter by User", options=users, default=users)
        
        with col2:
            decisions = list(set([log['new_decision'] for log in st.session_state.change_log]))
            filter_decision = st.multiselect("Filter by Decision", options=decisions, default=decisions)
        
        log_df = pd.DataFrame(st.session_state.change_log)
        
        log_df = log_df[
            (log_df['user'].isin(filter_user)) &
            (log_df['new_decision'].isin(filter_decision))
        ]
        
        log_df = log_df.sort_values('timestamp', ascending=False)
        
        st.markdown(f"#### Total Changes: {len(log_df)}")
        
        for idx, row in log_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 2])
                
                with col1:
                    st.markdown(f"**🕐 {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}**")
                    st.caption(f"By: {row['user']}")
                
                with col2:
                    st.markdown(f"**Match #{row['match_id']}**")
                    st.caption(f"{row['raw_supplier']} → {row['canonical_name']}")
                
                with col3:
                    old = row['old_decision'] if pd.notna(row['old_decision']) else "Unreviewed"
                    new = row['new_decision']
                    st.markdown(f"**{old}** → **{new}**")
                    
                    if new == 'Confirmed':
                        st.success("✅ Confirmed")
                    elif new == 'Rejected':
                        st.error("❌ Rejected")
                    elif new == 'Flagged':
                        st.warning("🚩 Flagged")
                
                st.markdown("---")
        
        if st.button("📥 Export Change Log"):
            csv = log_df.to_csv(index=False)
            st.download_button(
                label="Download Change Log CSV",
                data=csv,
                file_name=f"change_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No changes recorded yet. Start reviewing matches to see the change history.")

with tab4:
    st.markdown("### Analytics Dashboard")
    
    df_analytics = st.session_state.matches_df
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_matches = len(df_analytics)
        st.metric("Total Matches", total_matches)
    
    with col2:
        reviewed = len(df_analytics[df_analytics['HITL_Decision'].notna()])
        review_pct = (reviewed / total_matches * 100) if total_matches > 0 else 0
        st.metric("Reviewed", f"{reviewed} ({review_pct:.1f}%)")
    
    with col3:
        avg_score = df_analytics['match_score'].mean()
        st.metric("Avg Match Score", f"{avg_score:.2%}")
    
    with col4:
        high_priority = len(df_analytics[df_analytics['match_priority'] == 'High'])
        st.metric("High Priority", high_priority)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Matches by Canonical Name")
        canonical_counts = df_analytics['CANONICAL_NAME'].value_counts()
        st.bar_chart(canonical_counts)
    
    with col2:
        st.markdown("#### Decision Distribution")
        decision_counts = df_analytics['HITL_Decision'].value_counts()
        st.bar_chart(decision_counts)
    
    st.markdown("---")
    
    st.markdown("#### Summary by Canonical Name")
    
    summary = df_analytics.groupby('CANONICAL_NAME').agg({
        'id': 'count',
        'match_score': 'mean',
        'HITL_Decision': lambda x: (x == 'Confirmed').sum()
    }).reset_index()
    
    summary.columns = ['Canonical Name', 'Total Matches', 'Avg Score', 'Confirmed']
    summary['Avg Score'] = summary['Avg Score'].round(3)
    summary = summary.sort_values('Total Matches', ascending=False)
    
    st.dataframe(summary, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Business Unit Diversity Analysis")
    st.caption("Shows variety of NAICS codes within each canonical entity (indicating BU diversity)")
    
    bu_diversity = df_analytics.groupby('CANONICAL_NAME').agg({
        'naics_code_raw': lambda x: len(set(x)),
        'sic_code_raw': lambda x: len(set(x)),
        'RAW_SUPPLIER': 'count'
    }).reset_index()
    
    bu_diversity.columns = ['Canonical Name', 'Unique NAICS Codes', 'Unique SIC Codes', 'Total Variations']
    bu_diversity = bu_diversity.sort_values('Unique NAICS Codes', ascending=False)
    
    st.dataframe(bu_diversity, use_container_width=True)





