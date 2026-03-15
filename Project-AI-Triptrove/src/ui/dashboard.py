"""
Dashboard untuk monitoring TripTrove RAG System
Streamlit app untuk visualisasi analytics
"""
import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from analytics import Analytics
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(
    page_title="TripTrove Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analytics
analytics = Analytics()

# Header
st.title("📊 TripTrove Analytics Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    days_filter = st.selectbox(
        "Time Period",
        [1, 7, 14, 30, 90],
        index=1,
        format_func=lambda x: f"Last {x} days"
    )
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.button("📥 Export Report"):
        filename = analytics.export_report(days=days_filter)
        st.success(f"Report exported: {filename}")
    
    st.markdown("---")
    st.info("Dashboard updates automatically when new data is logged.")

# Get statistics
stats = analytics.get_stats(days=days_filter)

# Overview metrics
st.header("📈 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{stats['total_queries']}</div>
        <div class="metric-label">Total Queries</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <div class="metric-value">{stats['success_rate']}%</div>
        <div class="metric-label">Success Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="metric-value">{stats['avg_response_time']}s</div>
        <div class="metric-label">Avg Response Time</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
        <div class="metric-value">{stats['total_errors']}</div>
        <div class="metric-label">Total Errors</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Performance trend
st.header("📉 Performance Trend")

trend_df = analytics.get_performance_trend(days=days_filter)

if not trend_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Response time chart
        fig_time = px.line(
            trend_df,
            x='date',
            y='avg_response_time',
            title='Average Response Time',
            labels={'avg_response_time': 'Response Time (s)', 'date': 'Date'}
        )
        fig_time.update_traces(line_color='#667eea', line_width=3)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        # Success rate chart
        fig_success = px.line(
            trend_df,
            x='date',
            y='success_rate',
            title='Success Rate',
            labels={'success_rate': 'Success Rate (%)', 'date': 'Date'}
        )
        fig_success.update_traces(line_color='#4facfe', line_width=3)
        st.plotly_chart(fig_success, use_container_width=True)
    
    # Query volume chart
    fig_volume = px.bar(
        trend_df,
        x='date',
        y='total',
        title='Query Volume',
        labels={'total': 'Number of Queries', 'date': 'Date'},
        color='total',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_volume, use_container_width=True)
else:
    st.info("No data available for the selected period.")

st.markdown("---")

# Popular queries
st.header("🔥 Popular Keywords")

popular = analytics.get_popular_queries(limit=15)

if popular:
    df_popular = pd.DataFrame(popular)
    
    fig_popular = px.bar(
        df_popular,
        x='count',
        y='keyword',
        orientation='h',
        title='Most Frequent Keywords',
        labels={'count': 'Frequency', 'keyword': 'Keyword'},
        color='count',
        color_continuous_scale='Sunset'
    )
    fig_popular.update_layout(height=500)
    st.plotly_chart(fig_popular, use_container_width=True)
else:
    st.info("No query data available yet.")

st.markdown("---")

# Recent errors
st.header("⚠️ Recent Errors")

recent_errors = analytics.data['errors'][-10:]

if recent_errors:
    for error in reversed(recent_errors):
        with st.expander(f"[{error['timestamp']}] {error['error_type']}"):
            st.code(error['error_message'])
            if error.get('context'):
                st.json(error['context'])
else:
    st.success("No errors logged! 🎉")

st.markdown("---")

# Raw data
with st.expander("📋 View Raw Data"):
    tab1, tab2, tab3 = st.tabs(["Queries", "Sessions", "Errors"])
    
    with tab1:
        if analytics.data['queries']:
            df_queries = pd.DataFrame(analytics.data['queries'][-50:])
            st.dataframe(df_queries, use_container_width=True)
        else:
            st.info("No query data")
    
    with tab2:
        if analytics.data['sessions']:
            df_sessions = pd.DataFrame(analytics.data['sessions'][-50:])
            st.dataframe(df_sessions, use_container_width=True)
        else:
            st.info("No session data")
    
    with tab3:
        if analytics.data['errors']:
            df_errors = pd.DataFrame(analytics.data['errors'][-50:])
            st.dataframe(df_errors, use_container_width=True)
        else:
            st.info("No error data")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999;">
    <p>📊 TripTrove Analytics Dashboard | Real-time Monitoring</p>
</div>
""", unsafe_allow_html=True)
