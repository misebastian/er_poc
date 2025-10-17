import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import random

# Configuración de página
st.set_page_config(page_title="Entity Resolution Match Labelling", layout="wide")

# Función para crear dataset de ejemplo
def create_sample_dataset():
    suppliers = [
        # LinkedIn variants
        ("LinkedIn Australia Pty Ltd", "LinkedIn", 0.92, "High"),
        ("LinkedIn Sales Navigator", "LinkedIn", 0.88, "High"),
        ("LinkedIn Corporation", "LinkedIn", 0.95, "High"),
        ("Linkedin Ireland Unlimited", "LinkedIn", 0.89, "High"),
        ("LINKEDIN TALENT SOLUTIONS", "LinkedIn", 0.91, "High"),
        
        # Microsoft variants
        ("Microsoft Corporation", "Microsoft", 0.98, "High"),
        ("Microsoft Ireland Operations Ltd", "Microsoft", 0.94, "High"),
        ("MS Azure Services", "Microsoft", 0.85, "Medium"),
        ("Microsoft 365 Business", "Microsoft", 0.87, "High"),
        ("MSFT Cloud Solutions", "Microsoft", 0.82, "Medium"),
        
        # Google variants
        ("Google LLC", "Google", 0.97, "High"),
        ("Google Cloud EMEA", "Google", 0.93, "High"),
        ("Google Workspace", "Google", 0.90, "High"),
        ("YouTube LLC", "Google", 0.78, "Medium"),
        ("Google Ireland Limited", "Google", 0.95, "High"),
        
        # Salesforce variants
        ("Salesforce.com Inc", "Salesforce", 0.96, "High"),
        ("Salesforce EMEA Ltd", "Salesforce", 0.92, "High"),
        ("SFDC Ireland", "Salesforce", 0.84, "Medium"),
        ("Tableau Software LLC", "Salesforce", 0.72, "Medium"),
        ("Slack Technologies Inc", "Salesforce", 0.68, "Low"),
        
        # AWS variants
        ("Amazon Web Services Inc", "Amazon Web Services", 0.95, "High"),
        ("AWS EMEA SARL", "Amazon Web Services", 0.91, "High"),
        ("Amazon Web Srvcs Ireland", "Amazon Web Services", 0.88, "High"),
        
        # SAP variants
        ("SAP SE", "SAP", 0.98, "High"),
        ("SAP America Inc", "SAP", 0.94, "High"),
        ("SAP Labs LLC", "SAP", 0.86, "Medium"),
        ("SAP Ariba", "SAP", 0.79, "Medium"),
        
        # Oracle variants
        ("Oracle Corporation", "Oracle", 0.97, "High"),
        ("Oracle EMEA Limited", "Oracle", 0.93, "High"),
        ("Oracle Cloud Infrastructure", "Oracle", 0.88, "High"),
        ("NetSuite Inc", "Oracle", 0.65, "Low"),
        
        # Adobe variants
        ("Adobe Inc", "Adobe", 0.98, "High"),
        ("Adobe Systems Software", "Adobe", 0.94, "High"),
        ("Adobe Ireland", "Adobe", 0.92, "High"),
        
        # Zoom variants
        ("Zoom Video Communications", "Zoom", 0.96, "High"),
        ("Zoom.us", "Zoom", 0.91, "High"),
        ("Zoom Meetings", "Zoom", 0.87, "High"),
        
        # Casos ambiguos / difíciles
        ("Meta Platforms Ireland", "Meta", 0.89, "Medium"),
        ("Facebook Ireland Ltd", "Meta", 0.83, "Medium"),
        ("Apple Distribution International", "Apple", 0.86, "Medium"),
        ("Atlassian Pty Ltd", "Atlassian", 0.94, "High"),
        ("Dropbox International Unlimited", "Dropbox", 0.91, "High"),
    ]
    
    data = []
    for i, (raw, canonical, score, priority) in enumerate(suppliers, 1):
        data.append({
            'id': i,
            'RAW_SUPPLIER': raw,
            'CANONICAL_NAME': canonical,
            'match_score': score,
            'match_priority': priority,
            'HITL_Decision': None,
            'last_decision': None,
            'last_decision_by': None,
            'last_decision_date': None,
            'review_status': 'Unreviewed',
            'reviewed_at': None,
            'confidence_level': round(score * 100)
        })
    
    return pd.DataFrame(data)

# Inicializar session state
if 'matches_df' not in st.session_state:
    st.session_state.matches_df = create_sample_dataset()

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if 'change_log' not in st.session_state:
    st.session_state.change_log = []

if 'user_name' not in st.session_state:
    st.session_state.user_name = "Current User"

# Función para registrar cambios
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

# Función para actualizar decisión
def update_decision(idx, decision, current_match):
    old_decision = st.session_state.matches_df.at[idx, 'HITL_Decision']
    
    st.session_state.matches_df.at[idx, 'HITL_Decision'] = decision
    st.session_state.matches_df.at[idx, 'last_decision'] = decision
    st.session_state.matches_df.at[idx, 'review_status'] = decision
    st.session_state.matches_df.at[idx, 'last_decision_by'] = st.session_state.user_name
    st.session_state.matches_df.at[idx, 'last_decision_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.matches_df.at[idx, 'reviewed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_change(
        current_match['id'],
        current_match['RAW_SUPPLIER'],
        current_match['CANONICAL_NAME'],
        old_decision,
        decision,
        st.session_state.user_name
    )

# Título principal
st.title("🔄 [ERP Migration] Entity Resolution Match Labelling")

# Configuración de usuario
with st.sidebar:
    st.header("👤 User Settings")
    st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
    st.divider()

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Individual Match Review", 
    "📊 Dataset View & Query", 
    "📜 Change History Log",
    "📈 Analytics"
])

with tab1:
    df = st.session_state.matches_df
    
    # Métricas en la parte superior
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        unreviewed = len(df[df['review_status'] == 'Unreviewed'])
        st.metric("Unreviewed", unreviewed)
    with col2:
        confirmed = len(df[df['HITL_Decision'] == 'Confirmed'])
        st.metric("Confirmed", confirmed)
    with col3:
        rejected = len(df[df['HITL_Decision'] == 'Rejected'])
        st.metric("Rejected", rejected)
    with col4:
        flagged = len(df[df['HITL_Decision'] == 'Flagged'])
        st.metric("Flagged", flagged)
    with col5:
        total = len(df)
        progress = ((confirmed + rejected + flagged) / total * 100) if total > 0 else 0
        st.metric("Progress", f"{progress:.1f}%")
    
    st.divider()
    
    # Sidebar para filtros
    with st.sidebar:
        st.header("Match Selection")
        st.subheader("🔍 Filter Matches")
        
        # Búsqueda por texto
        search_text = st.text_input("🔎 Search Supplier/Canonical", "")
        
        # Filtros
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
        
        # Aplicar filtros
        filtered_df = df[
            (df['match_priority'].isin(priority_filter)) &
            (df['review_status'].isin(status_filter)) &
            (df['match_score'] >= score_filter[0]) &
            (df['match_score'] <= score_filter[1])
        ]
        
        # Filtro de búsqueda
        if search_text:
            filtered_df = filtered_df[
                filtered_df['RAW_SUPPLIER'].str.contains(search_text, case=False, na=False) |
                filtered_df['CANONICAL_NAME'].str.contains(search_text, case=False, na=False)
            ]
        
        filtered_df = filtered_df.reset_index(drop=True)
        
        st.divider()
        st.subheader(f"Matches ({len(filtered_df)})")
        
        # Lista de matches
        for idx, row in filtered_df.head(50).iterrows():
            status_color = {
                'Confirmed': '🟢',
                'Rejected': '🔴',
                'Flagged': '🟡',
                'Unreviewed': '⚪'
            }
            
            if st.button(
                f"{status_color[row['review_status']]} {row['RAW_SUPPLIER'][:30]}...",
                key=f"match_{idx}",
                use_container_width=True
            ):
                st.session_state.current_index = idx
    
    # Área principal de revisión
    if len(filtered_df) > 0:
        current_match = filtered_df.iloc[st.session_state.current_index]
        original_idx = df[df['id'] == current_match['id']].index[0]
        
        # Botones de acción
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
        
        # Score y status
        col1, col2, col3 = st.columns([1, 2, 2])
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
            st.caption(f"Confidence: {current_match['confidence_level']}%")
        
        with col3:
            if current_match['last_decision_by']:
                st.markdown(f"**Last Decision By:** {current_match['last_decision_by']}")
                st.caption(f"Date: {current_match['last_decision_date']}")
            else:
                st.markdown("**Status:** Not reviewed yet")
        
        st.divider()
        
        # Detalles del match
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Match Priority**")
            priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
            st.markdown(f"{priority_color[current_match['match_priority']]} {current_match['match_priority']}")
        
        with col2:
            st.markdown("**Review Status**")
            st.markdown(f"{status_emoji.get(current_match['review_status'], '⚪')} {current_match['review_status']}")
        
        with col3:
            st.markdown("**Match ID**")
            st.markdown(f"#{current_match['id']}")
        
        st.divider()
        
        # Comparación lado a lado
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Left Entity (Raw)")
            st.markdown("**Source: Raw Supplier Data**")
            
            with st.container(border=True):
                st.markdown("#### Properties")
                st.markdown(f"**Raw Supplier Name:**")
                st.markdown(f"# {current_match['RAW_SUPPLIER']}")
                st.divider()
                st.markdown(f"**Match Score:** {current_match['match_score']}")
                st.markdown(f"**Priority:** {current_match['match_priority']}")
                st.markdown(f"**Record ID:** {current_match['id']}")
        
        with col2:
            st.markdown("### 📥 Right Entity (Canonical)")
            st.markdown("**Target: Canonical Master Data**")
            
            with st.container(border=True):
                st.markdown("#### Properties")
                st.markdown(f"**Canonical Name:**")
                st.markdown(f"# {current_match['CANONICAL_NAME']}")
                st.divider()
                st.markdown(f"**Match Score:** {current_match['match_score']}")
                st.markdown(f"**HITL Decision:** {current_match['HITL_Decision'] or 'Pending'}")
                st.markdown(f"**Status:** {current_match['review_status']}")
        
        # Navegación
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
    st.header("📊 Dataset View & Query")
    
    # Query builder
    st.subheader("🔍 Query Dataset")
    
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
    
    # Búsqueda por texto
    query_text = st.text_input("🔎 Search in Raw Supplier", "")
    
    # Aplicar queries
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
    
    # Mostrar resultados
    st.subheader(f"Results: {len(queried_df)} matches")
    
    # Configurar columnas a mostrar
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
    
    # Estadísticas del query
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
    
    # Exportar resultados
    st.divider()
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
    st.header("📜 Change History Log")
    
    if st.session_state.change_log:
        # Filtros para el log
        col1, col2 = st.columns(2)
        
        with col1:
            users = list(set([log['user'] for log in st.session_state.change_log]))
            filter_user = st.multiselect("Filter by User", options=users, default=users)
        
        with col2:
            decisions = list(set([log['new_decision'] for log in st.session_state.change_log]))
            filter_decision = st.multiselect("Filter by Decision", options=decisions, default=decisions)
        
        # Crear DataFrame del log
        log_df = pd.DataFrame(st.session_state.change_log)
        
        # Aplicar filtros
        log_df = log_df[
            (log_df['user'].isin(filter_user)) &
            (log_df['new_decision'].isin(filter_decision))
        ]
        
        # Ordenar por timestamp descendente
        log_df = log_df.sort_values('timestamp', ascending=False)
        
        st.subheader(f"📊 Total Changes: {len(log_df)}")
        
        # Mostrar log en formato tabla
        for idx, row in log_df.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 3, 2])
                
                with col1:
                    st.markdown(f"**🕐 {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}**")
                    st.caption(f"By: {row['user']}")
                
                with col2:
                    st.markdown(f"**Match #{row['match_id']}**")
                    st.markdown(f"`{row['raw_supplier']}` → `{row['canonical_name']}`")
                
                with col3:
                    old = row['old_decision'] if pd.notna(row['old_decision']) else "Unreviewed"
                    new = row['new_decision']
                    st.markdown(f"**{old}** → **{new}**")
                    
                    if new == 'Confirmed':
                        st.success("Confirmed")
                    elif new == 'Rejected':
                        st.error("Rejected")
                    elif new == 'Flagged':
                        st.warning("Flagged")
        
        # Exportar log
        st.divider()
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
    st.header("📈 Analytics Dashboard")
    
    df_analytics = st.session_state.matches_df
    
    # Métricas generales
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
    
    st.divider()
    
    # Análisis por Canonical Name
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Matches by Canonical Name")
        canonical_counts = df_analytics['CANONICAL_NAME'].value_counts()
        st.bar_chart(canonical_counts)
    
    with col2:
        st.subheader("✅ Decision Distribution")
        decision_counts = df_analytics['HITL_Decision'].value_counts()
        st.bar_chart(decision_counts)
    
    st.divider()
    
    # Tabla de resumen por Canonical
    st.subheader("📋 Summary by Canonical Name")
    
    summary = df_analytics.groupby('CANONICAL_NAME').agg({
        'id': 'count',
        'match_score': 'mean',
        'HITL_Decision': lambda x: (x == 'Confirmed').sum()
    }).reset_index()
    
    summary.columns = ['Canonical Name', 'Total Matches', 'Avg Score', 'Confirmed']
    summary['Avg Score'] = summary['Avg Score'].round(3)
    summary = summary.sort_values('Total Matches', ascending=False)
    
    st.dataframe(summary, use_container_width=True)

