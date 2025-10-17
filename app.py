import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(page_title="Entity Resolution Match Labelling", layout="wide")

# Custom CSS for light theme matching the image
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f5f5f7;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 4px;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 600;
    }
    
    /* Cards/Containers */
    [data-testid="stVerticalBlock"] > div {
        background-color: #ffffff;
        border-radius: 6px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 4px;
        color: #666;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #f0f0f0;
        color: #000;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #d0d0d0;
    }
    
    /* Priority badge */
    .priority-high {
        background-color: #fee;
        color: #c00;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .priority-medium {
        background-color: #fff4e0;
        color: #d97706;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .priority-low {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sample company data with NAICS, SIC, website, description
def create_sample_dataset():
    companies_data = [
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
            "desc_raw": "Professional networking platform - Australia",
            "desc_canonical": "Professional networking and career development platform"
        },
        {
            "raw": "LinkedIn Sales Navigator",
            "canonical": "LinkedIn",
            "score": 0.88,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "518210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "business.linkedin.com/sales-solutions",
            "website_canonical": "linkedin.com",
            "desc_raw": "Sales intelligence and prospecting tool",
            "desc_canonical": "Professional networking and career development platform"
        },
        {
            "raw": "LinkedIn Corporation",
            "canonical": "LinkedIn",
            "score": 0.95,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "518210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "linkedin.com",
            "website_canonical": "linkedin.com",
            "desc_raw": "Professional social networking service",
            "desc_canonical": "Professional networking and career development platform"
        },
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
            "desc_raw": "Software and cloud computing services",
            "desc_canonical": "Technology corporation developing software, hardware, and cloud services"
        },
        {
            "raw": "Microsoft Ireland Operations Ltd",
            "canonical": "Microsoft",
            "score": 0.94,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "microsoft.com/ie",
            "website_canonical": "microsoft.com",
            "desc_raw": "Microsoft European operations subsidiary",
            "desc_canonical": "Technology corporation developing software, hardware, and cloud services"
        },
        {
            "raw": "MS Azure Services",
            "canonical": "Microsoft",
            "score": 0.85,
            "priority": "Medium",
            "naics_raw": "518210",
            "naics_canonical": "511210",
            "sic_raw": "7374",
            "sic_canonical": "7372",
            "website_raw": "azure.microsoft.com",
            "website_canonical": "microsoft.com",
            "desc_raw": "Cloud computing platform and services",
            "desc_canonical": "Technology corporation developing software, hardware, and cloud services"
        },
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
            "desc_raw": "Internet search and online advertising",
            "desc_canonical": "Multinational technology company specializing in Internet services"
        },
        {
            "raw": "Google Cloud EMEA",
            "canonical": "Google",
            "score": 0.93,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "519130",
            "sic_raw": "7374",
            "sic_canonical": "7375",
            "website_raw": "cloud.google.com",
            "website_canonical": "google.com",
            "desc_raw": "Cloud computing services - EMEA region",
            "desc_canonical": "Multinational technology company specializing in Internet services"
        },
        {
            "raw": "YouTube LLC",
            "canonical": "Google",
            "score": 0.78,
            "priority": "Medium",
            "naics_raw": "519130",
            "naics_canonical": "519130",
            "sic_raw": "7375",
            "sic_canonical": "7375",
            "website_raw": "youtube.com",
            "website_canonical": "google.com",
            "desc_raw": "Video sharing and social media platform",
            "desc_canonical": "Multinational technology company specializing in Internet services"
        },
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
            "desc_raw": "Cloud-based CRM software and applications",
            "desc_canonical": "Customer relationship management (CRM) software and cloud computing"
        },
        {
            "raw": "Salesforce EMEA Ltd",
            "canonical": "Salesforce",
            "score": 0.92,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "salesforce.com/eu",
            "website_canonical": "salesforce.com",
            "desc_raw": "Salesforce European operations",
            "desc_canonical": "Customer relationship management (CRM) software and cloud computing"
        },
        {
            "raw": "Tableau Software LLC",
            "canonical": "Salesforce",
            "score": 0.72,
            "priority": "Medium",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "tableau.com",
            "website_canonical": "salesforce.com",
            "desc_raw": "Business intelligence and analytics software",
            "desc_canonical": "Customer relationship management (CRM) software and cloud computing"
        },
        {
            "raw": "Amazon Web Services Inc",
            "canonical": "Amazon Web Services",
            "score": 0.95,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "518210",
            "sic_raw": "7374",
            "sic_canonical": "7374",
            "website_raw": "aws.amazon.com",
            "website_canonical": "aws.amazon.com",
            "desc_raw": "Cloud computing and web hosting services",
            "desc_canonical": "On-demand cloud computing platforms and APIs"
        },
        {
            "raw": "AWS EMEA SARL",
            "canonical": "Amazon Web Services",
            "score": 0.91,
            "priority": "High",
            "naics_raw": "518210",
            "naics_canonical": "518210",
            "sic_raw": "7374",
            "sic_canonical": "7374",
            "website_raw": "aws.amazon.com/emea",
            "website_canonical": "aws.amazon.com",
            "desc_raw": "AWS European operations",
            "desc_canonical": "On-demand cloud computing platforms and APIs"
        },
        {
            "raw": "SAP SE",
            "canonical": "SAP",
            "score": 0.98,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "sap.com",
            "website_canonical": "sap.com",
            "desc_raw": "Enterprise application software",
            "desc_canonical": "Enterprise resource planning (ERP) software and solutions"
        },
        {
            "raw": "SAP America Inc",
            "canonical": "SAP",
            "score": 0.94,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "sap.com/usa",
            "website_canonical": "sap.com",
            "desc_raw": "SAP North America operations",
            "desc_canonical": "Enterprise resource planning (ERP) software and solutions"
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
            "desc_raw": "Database and cloud computing solutions",
            "desc_canonical": "Computer technology corporation specializing in database software"
        },
        {
            "raw": "Oracle EMEA Limited",
            "canonical": "Oracle",
            "score": 0.93,
            "priority": "High",
            "naics_raw": "511210",
            "naics_canonical": "511210",
            "sic_raw": "7372",
            "sic_canonical": "7372",
            "website_raw": "oracle.com/emea",
            "website_canonical": "oracle.com",
            "desc_raw": "Oracle European operations",
            "desc_canonical": "Computer technology corporation specializing in database software"
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
            "desc_raw": "Creative software and digital marketing solutions",
            "desc_canonical": "Computer software company focused on creative and multimedia products"
        },
        {
            "raw": "Zoom Video Communications",
            "canonical": "Zoom",
            "score": 0.96,
            "priority": "High",
            "naics_raw": "517311",
            "naics_canonical": "517311",
            "sic_raw": "4899",
            "sic_canonical": "4899",
            "website_raw": "zoom.us",
            "website_canonical": "zoom.us",
            "desc_raw": "Video conferencing and communications platform",
            "desc_canonical": "Video telephony and online chat services"
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

# Main title
st.markdown("### [ERP Migration] Entity Resolution Match Labelling")

# User settings in sidebar
with st.sidebar:
    st.markdown("#### 👤 User Settings")
    st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
    st.divider()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Individual Match Review", 
    "📊 Dataset View & Query", 
    "📜 Change History Log",
    "📈 Analytics"
])

with tab1:
    df = st.session_state.matches_df
    
    # Top metrics
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
    
    st.divider()
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("#### Match Selection")
        st.markdown("##### 🔍 Filter Matches")
        
        # Text search
        search_text = st.text_input("🔎 Search Supplier/Canonical", "")
        
        # Filters
        priority_filter = st.multiselect(
            "Match Priority",
            options=['High', 'Medium', 'Low'],
            default=['High', 'Medium', 'Low']
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
        
        # Apply filters
        filtered_df = df[
            (df['match_priority'].isin(priority_filter)) &
            (df['review_status'].isin(status_filter)) &
            (df['match_score'] >= score_filter[0]) &
            (df['match_score'] <= score_filter[1])
        ]
        
        # Search filter
        if search_text:
            filtered_df = filtered_df[
                filtered_df['RAW_SUPPLIER'].str.contains(search_text, case=False, na=False) |
                filtered_df['CANONICAL_NAME'].str.contains(search_text, case=False, na=False)
            ]
        
        filtered_df = filtered_df.reset_index(drop=True)
        
        st.divider()
        st.markdown(f"##### Matches ({len(filtered_df)})")
        
        # Match list
        for idx, row in filtered_df.head(50).iterrows():
            status_color = {
                'Confirmed': '✅',
                'Rejected': '❌',
                'Flagged': '🚩',
                'Unreviewed': '⚪'
            }
            
            button_label = f"{status_color[row['review_status']]} {row['RAW_SUPPLIER'][:35]}..."
            
            if st.button(button_label, key=f"match_{idx}", use_container_width=True):
                st.session_state.current_index = idx
    
    # Main review area
    if len(filtered_df) > 0:
        current_match = filtered_df.iloc[st.session_state.current_index]
        original_idx = df[df['id'] == current_match['id']].index[0]
        
        # Review Match header
        st.markdown("#### Review Match")
        
        # Action buttons
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        
        with col1:
            if st.button("✅ Confirm Match", use_container_width=True, type="primary"):
                update_decision(original_idx, 'Confirmed', current_match)
                st.success(f"Match confirmed by {st.session_state.user_name}")
                st.rerun()
        
        with col2:
            if st.button("🚩 Flag Match", use_container_width=True):
                update_decision(original_idx, 'Flagged', current_match)
                st.warning(f"Match flagged by {st.session_state.user_name}")
                st.rerun()
        
        with col3:
            if st.button("❌ Reject Match", use_container_width=True):
                update_decision(original_idx, 'Rejected', current_match)
                st.error(f"Match rejected by {st.session_state.user_name}")
                st.rerun()
        
        st.divider()
        
        # Score and status
        col1, col2 = st.columns([1, 4])
        with col1:
            score_pct = int(current_match['match_score'] * 100)
            st.markdown(f"### {score_pct}%")
            st.caption("Overall Score")
        
        with col2:
            status_emoji = {
                'Confirmed': '✅',
                'Rejected': '❌',
                'Flagged': '🚩',
                'Unreviewed': '⚪'
            }
            decision = current_match['HITL_Decision'] if pd.notna(current_match['HITL_Decision']) else 'Unreviewed'
            st.markdown(f"### {status_emoji.get(decision, '⚪')} {decision}")
            st.caption(f"Predicated Label | Confirmation Probability: {current_match['confidence_level']}%")
        
        st.divider()
        
        # Match details
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**Match Priority**")
            priority = current_match['match_priority']
            priority_class = f"priority-{priority.lower()}"
            st.markdown(f'<span class="{priority_class}">{priority}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Review Status**")
            st.markdown(f"{status_emoji.get(current_match['review_status'], '⚪')} {current_match['review_status']}")
        
        with col3:
            st.markdown("**Match At**")
            if current_match['reviewed_at']:
                st.markdown(current_match['reviewed_at'])
            else:
                st.markdown("Not reviewed yet")
        
        with col4:
            st.markdown("**ER Score Table**")
            st.markdown("🔵 Supplier Deduplication")
        
        st.divider()
        
        # Side by side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📤 Left Entity")
            st.markdown(f"**{current_match['RAW_SUPPLIER']}**")
            st.caption("[ERP Migration] Supplier")
            
            with st.container(border=True):
                st.markdown("**Overview** | Properties")
                st.divider()
                st.markdown("##### Properties")
                
                st.markdown(f"**NAICS Code:** {current_match['naics_code_raw']}")
                st.markdown(f"**SIC Code:** {current_match['sic_code_raw']}")
                st.markdown(f"**Website URL:** {current_match['website_url_raw']}")
                st.markdown(f"**Short Description:**")
                st.caption(current_match['description_raw'])
        
        with col2:
            st.markdown("#### 📥 Right Entity")
            st.markdown(f"**{current_match['CANONICAL_NAME']}**")
            st.caption("[ERP Migration] Supplier")
            
            with st.container(border=True):
                st.markdown("**Overview** | Properties")
                st.divider()
                st.markdown("##### Properties")
                
                st.markdown(f"**NAICS Code:** {current_match['naics_code_canonical']}")
                st.markdown(f"**SIC Code:** {current_match['sic_code_canonical']}")
                st.markdown(f"**Website URL:** {current_match['website_url_canonical']}")
                st.markdown(f"**Short Description:**")
                st.caption(current_match['description_canonical'])
        
        # Navigation
        st.divider()
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
    st.markdown("### 📊 Dataset View & Query")
    
    # Query builder
    st.markdown("#### 🔍 Query Dataset")
    
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
    
    # Text search
    query_text = st.text_input("🔎 Search in Raw Supplier", "")
    
    # Apply queries
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
    
    # Show results
    st.markdown(f"#### Results: {len(queried_df)} matches")
    
    # Column selection
    columns_to_show = st.multiselect(
        "Select columns to display",
        options=list(queried_df.columns),
        default=['id', 'RAW_SUPPLIER', 'CANONICAL_NAME', 'match_score', 
                'HITL_Decision', 'last_decision_by', 'last_decision_date']
    )
    
    if columns_to_show:
        st.dataframe(
            queried_df[columns_to_show],
            use_container_width=True,
            height=400
        )
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(queried_df))
    with col2:
        confirmed_count = len(queried_df[queried_df['HITL_Decision'] == 'Confirmed'])
        st.metric("Confirmed", confirmed_count)
    with col3:
        rejected_count = len(queried_df[queried_df['HITL_Decision'] == 'Rejected'])
        st.metric("Rejected", rejected_count


