# dashboard_agent_professional.py
"""
Executive-grade MCP Banking Test Framework Dashboard
Professional corporate theme with clean design and proper color hierarchy.
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
  page_title="MCP Banking Test Framework - Executive Dashboard",
  layout="wide",
  initial_sidebar_state="collapsed"
)

# ------------------ PROFESSIONAL CORPORATE THEME CSS ------------------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --primary-blue: #1f4e79;
  --secondary-blue: #2e5b8a;
  --accent-blue: #4a90e2;
  --light-blue: #e8f2ff;
  --success-green: #28a745;
  --warning-orange: #fd7e14;
  --danger-red: #dc3545;
  --text-dark: #2c3e50;
  --text-muted: #6c757d;
  --border-light: #dee2e6;
  --bg-light: #f8f9fa;
  --white: #ffffff;
  --shadow: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-hover: 0 8px 24px rgba(0,0,0,0.12);
}

/* Global Styles */
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
  background: linear-gradient(135deg, var(--bg-light) 0%, var(--white) 100%);
}

.main .block-container {
  background: transparent;
  padding-top: 2rem;
}

/* Header Styles */
.dashboard-header {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
  color: white;
  padding: 3rem 2rem;
  border-radius: 16px;
  margin-bottom: 2rem;
  box-shadow: var(--shadow);
  text-align: center;
}

.dashboard-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  letter-spacing: -0.02em;
}

.dashboard-subtitle {
  font-size: 1.3rem;
  font-weight: 400;
  opacity: 0.9;
  margin: 0;
}

/* KPI Cards */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.kpi-card {
  background: var(--white);
  border: none;
  border-radius: 16px;
  padding: 2rem 1.5rem;
  text-align: center;
  box-shadow: var(--shadow);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-blue), var(--primary-blue));
}

.kpi-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 0.8rem;
}

.kpi-value {
  font-size: 2.8rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0.5rem 0;
  line-height: 1;
  letter-spacing: -0.02em;
}

.kpi-delta {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
  margin-top: 0.5rem;
}

.kpi-positive { color: var(--success-green); }
.kpi-negative { color: var(--danger-red); }
.kpi-warning { color: var(--warning-orange); }

/* Section Headers */
.section-header {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-blue);
  margin: 3rem 0 1.5rem 0;
  padding-bottom: 1rem;
  border-bottom: 3px solid var(--border-light);
  position: relative;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-blue), var(--primary-blue));
  border-radius: 2px;
}

/* Chart Cards */
.chart-card {
  background: var(--white);
  border: none;
  border-radius: 16px;
  padding: 2rem;
  margin: 1.5rem 0;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: var(--shadow-hover);
}

/* Tabs Enhancement */
.stTabs [data-baseweb="tab-list"] {
  background: var(--white);
  border-radius: 16px;
  border: none;
  padding: 0.5rem;
  gap: 0.5rem;
  box-shadow: var(--shadow);
}

.stTabs [data-baseweb="tab"] {
  background: transparent;
  border-radius: 12px;
  color: var(--text-muted);
  font-weight: 600;
  padding: 1rem 2rem;
  border: none;
  transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
  background: var(--accent-blue) !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
}

/* Enhanced Buttons */
.stButton > button {
  background: linear-gradient(135deg, var(--accent-blue), var(--primary-blue));
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.8rem 2rem;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

/* Data Tables */
.stDataFrame {
  border: none;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

/* Status Badges */
.status-badge {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-success { 
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.status-warning { 
  background: linear-gradient(135deg, #fd7e14, #ffc107);
  color: white;
}

.status-danger { 
  background: linear-gradient(135deg, #dc3545, #e74c3c);
  color: white;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Enhanced scrollbar */
::-webkit-scrollbar {
  width: 12px;
}
::-webkit-scrollbar-track {
  background: var(--bg-light);
  border-radius: 6px;
}
::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--accent-blue), var(--primary-blue));
  border-radius: 6px;
  border: 2px solid var(--bg-light);
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
}
}

</style>
""", unsafe_allow_html=True)

# ------------------ Helper loaders ------------------
@st.cache_data(ttl=300)
def load_latest_analysis_data():
    data_dir = Path("data/output")
    analysis_files = list(data_dir.glob("analysis_summary_*.json")) if data_dir.exists() else []
    if not analysis_files:
        return None
    # Prefer a specifically named comprehensive file if present
    preferred = data_dir / "analysis_summary_20250912_220048.json"
    latest_file = preferred if preferred.exists() else max(analysis_files, key=lambda x: x.stat().st_mtime)
    try:
        return json.loads(latest_file.read_text())
    except Exception:
        return None

@st.cache_data(ttl=300)
def load_sample_execution_data():
    try:
        return json.loads(Path("data/output/sample_execution_report.json").read_text())
    except Exception:
        return None

# Load data
analysis_data = load_latest_analysis_data()
sample_data = load_sample_execution_data()

# Corporate color palette
CORPORATE_COLORS = {
    'primary': '#1f4e79',
    'secondary': '#2e5b8a', 
    'accent': '#4a90e2',
    'success': '#28a745',
    'warning': '#fd7e14',
    'danger': '#dc3545',
    'muted': '#6c757d',
    'light': '#f8f9fa'
}

def create_professional_chart_layout():
    """Create consistent professional chart layout"""
    return {
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': CORPORATE_COLORS['primary']},
        'title': {'font': {'size': 16, 'color': CORPORATE_COLORS['primary']}},
        'xaxis': {
            'showgrid': True,
            'gridcolor': '#f0f0f0',
            'linecolor': '#e0e0e0',
            'tickfont': {'color': CORPORATE_COLORS['muted']}
        },
        'yaxis': {
            'showgrid': True,
            'gridcolor': '#f0f0f0',
            'linecolor': '#e0e0e0',
            'tickfont': {'color': CORPORATE_COLORS['muted']}
        },
        'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60}
    }

if not analysis_data:
    st.warning("No analysis data found. Run the MCP pipeline first!")
    st.info("Execute: `python src/orchestrator.py` to generate analysis data")
    st.stop()

# Extract metrics with proper null handling
stats = analysis_data.get('statistics', {}) if analysis_data else {}
overview = stats.get('overview', {}) if stats else {}
failure_analysis = stats.get('failure_analysis', {}) if stats else {}
performance = stats.get('performance_analysis', {}) if stats else {}
ai_insights = analysis_data.get('ai_insights', {}) if analysis_data else {}

# Header with professional corporate styling
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">MCP Banking Test Framework</div>
    <div class="dashboard-subtitle">Executive Analytics & Performance Intelligence</div>
</div>
""", unsafe_allow_html=True)

# Professional KPI Grid
st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)

cols = st.columns(5)
with cols[0]:
    total_tests = int(overview.get('total_tests', 0))
    ai_generated = total_tests - 7
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Total Tests Executed</div>
        <div class="kpi-value">{total_tests:,}</div>
        <div class="kpi-delta kpi-positive">AI Generated: +{ai_generated}</div>
    </div>
    ''', unsafe_allow_html=True)

with cols[1]:
    pass_rate = float(overview.get('pass_rate', 0.0))
    passed = int(overview.get('passed', 0))
    status_class = "kpi-positive" if pass_rate >= 85 else "kpi-warning" if pass_rate >= 70 else "kpi-negative"
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Pass Rate</div>
        <div class="kpi-value">{pass_rate:.1f}%</div>
        <div class="kpi-delta {status_class}">{passed:,} passed</div>
    </div>
    ''', unsafe_allow_html=True)

with cols[2]:
    exec_time = float(overview.get('execution_duration', 0.0))
    avg_exec = float(performance.get('average_execution_time', 0.0))
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Execution Time</div>
        <div class="kpi-value">{exec_time:.1f}s</div>
        <div class="kpi-delta">Avg {avg_exec:.1f}s per test</div>
    </div>
    ''', unsafe_allow_html=True)

with cols[3]:
    critical = int(failure_analysis.get('by_priority', {}).get('critical', {}).get('failed', 0))
    high = int(failure_analysis.get('by_priority', {}).get('high', {}).get('failed', 0))
    status_class = "kpi-negative" if critical > 0 else "kpi-warning" if high > 0 else "kpi-positive"
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Critical Issues</div>
        <div class="kpi-value">{critical}</div>
        <div class="kpi-delta {status_class}">{high} high priority</div>
    </div>
    ''', unsafe_allow_html=True)

with cols[4]:
    coverage_increase = ((total_tests / 7) - 1) * 100 if 7 > 0 else 0
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Coverage Increase</div>
        <div class="kpi-value">{coverage_increase:.0f}%</div>
        <div class="kpi-delta kpi-positive">vs Baseline</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Professional Tabs Section
tab1, tab2, tab3, tab4 = st.tabs(["Executive Summary", "Module Performance", "Risk Analysis", "Technical Insights"])

with tab1:
    st.markdown('<div class="section-header">Test Execution Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        
        # Professional execution summary chart
        execution_data = {
            'Status': ['Passed', 'Failed'],
            'Count': [int(overview.get('passed', 0)), int(overview.get('failed', 0))],
            'Percentage': [pass_rate, max(0.0, 100.0 - pass_rate)]
        }
        
        fig_summary = px.bar(
            x=execution_data['Status'],
            y=execution_data['Count'],
            color=execution_data['Status'],
            color_discrete_map={
                'Passed': CORPORATE_COLORS['success'],
                'Failed': CORPORATE_COLORS['danger']
            },
            title="Test Execution Results",
            text=execution_data['Count']
        )
        
        fig_summary.update_layout(create_professional_chart_layout())
        fig_summary.update_traces(
            texttemplate='%{text}', 
            textposition='outside',
            textfont={'size': 14, 'color': CORPORATE_COLORS['primary']}
        )
        fig_summary.update_layout(
            title={'x': 0.5, 'xanchor': 'center'},
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_summary, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("### Key Metrics")

        # Performance metrics
        metrics_data = {
            "Total Tests": f"{total_tests:,}",
            "Pass Rate": f"{pass_rate:.1f}%",
            "Avg Execution": f"{avg_exec:.2f}s",
            "Coverage Boost": f"+{coverage_increase:.0f}%"
        }

        for metric, value in metrics_data.items():
            st.markdown(f"""
            <div style=\"display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid #f0f0f0;\">
                <span style=\"color: {CORPORATE_COLORS['muted']}; font-weight: 500;\">{metric}</span>
                <span style=\"color: {CORPORATE_COLORS['primary']}; font-weight: 700;\">{value}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">Module-Specific Analysis</div>', unsafe_allow_html=True)
    modules = failure_analysis.get('by_module', {}) or {}
    if modules:
        module_names = list(modules.keys())
        total_tests_mod = [int(modules[m].get('total', 0)) for m in module_names]
        failed_tests = [int(modules[m].get('failed', 0)) for m in module_names]
        failure_rates = [float(modules[m].get('failure_rate', 0.0)) for m in module_names]

        fig_modules = make_subplots(rows=1, cols=2, subplot_titles=('Test Distribution by Module', 'Failure Rate Analysis'), specs=[[{"type": "bar"}, {"type": "bar"}]])
        fig_modules.add_trace(go.Bar(x=module_names, y=total_tests_mod, name='Total Tests', marker_color=CORPORATE_COLORS['accent'], text=total_tests_mod, textposition='outside'), row=1, col=1)
        colors = [
          CORPORATE_COLORS['danger'] if rate > 20 else (
            CORPORATE_COLORS['warning'] if rate > 10 else CORPORATE_COLORS['accent']
          ) for rate in failure_rates
        ]
        fig_modules.add_trace(go.Bar(x=module_names, y=failure_rates, name='Failure Rate (%)', marker_color=colors, text=[f"{rate:.1f}%" for rate in failure_rates], textposition='outside'), row=1, col=2)
        fig_modules.update_layout(height=500, showlegend=False, template='plotly_white')
        st.plotly_chart(fig_modules, use_container_width=True)

        st.markdown('<div class="section-header">Module Recommendations</div>', unsafe_allow_html=True)
        for module, data in modules.items():
            rate = float(data.get('failure_rate', 0.0))
            if rate > 0:
                severity = "High" if rate > 20 else "Medium" if rate > 10 else "Low"
                st.markdown(f"<div class='card metric-container'><strong>{module}</strong> — Failure Rate: {rate:.1f}%  <br>Failed: {int(data.get('failed',0))} / {int(data.get('total',0))} — Severity: {severity}</div>", unsafe_allow_html=True)
    else:
        st.info("No module-level failure data available.")

with tab3:
    st.markdown('<div class="section-header">Risk Assessment Matrix</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        priorities = failure_analysis.get('by_priority', {}) or {}
        if priorities:
            priority_names = list(priorities.keys())
            priority_totals = [int(priorities[p].get('total', 0)) for p in priority_names]
            priority_rates = [float(priorities[p].get('failure_rate', 0.0)) for p in priority_names]
            priority_failures = [int(priorities[p].get('failed', 0)) for p in priority_names]
            fig_priority = px.scatter(x=priority_totals, y=priority_rates, size=priority_failures, color=priority_names, hover_name=priority_names, title=None, template='plotly_white')
            fig_priority.update_layout(height=420)
            st.plotly_chart(fig_priority, use_container_width=True)
        else:
            st.info("No priority breakdown available.")
    with col2:
        if performance.get('slowest_tests') and performance.get('fastest_tests'):
            performance_data = []
            for t in performance['slowest_tests']:
                performance_data.append({'Test ID': t.get('test_id'), 'Time (s)': float(t.get('time', 0.0)), 'Category': 'Slowest'})
            for t in performance['fastest_tests']:
                performance_data.append({'Test ID': t.get('test_id'), 'Time (s)': float(t.get('time', 0.0)), 'Category': 'Fastest'})
            df_perf = pd.DataFrame(performance_data)
            fig_perf = px.bar(df_perf, x='Test ID', y='Time (s)', color='Category', color_discrete_sequence=[CORPORATE_COLORS['danger'], CORPORATE_COLORS['accent']], title=None, template='plotly_white')
            fig_perf.update_layout(height=420)
            st.plotly_chart(fig_perf, use_container_width=True)
        else:
            st.info('No performance extremes data available.')

    if ai_insights.get('critical_issue'):
        st.markdown('<div class="section-header">Critical Issues Identified</div>', unsafe_allow_html=True)
        st.error(ai_insights['critical_issue'])

with tab4:
    st.markdown('<div class="section-header">AI-Generated Insights</div>', unsafe_allow_html=True)
    left, right = st.columns([2, 1])
    with left:
        recs = ai_insights.get('recommendations') or []
        if recs:
            st.markdown('### Actionable Recommendations')
            for i, rec in enumerate(recs[:6], 1):
                st.markdown(f"<div class='card metric-container'><strong>Recommendation {i}</strong><div style='color:var(--text-muted); margin-top:0.35rem'>{rec}</div></div>", unsafe_allow_html=True)
        else:
            st.info('No AI recommendations available.')
    with right:
        avg_time = float(performance.get('average_execution_time', 0.0))
        total_time = float(performance.get('total_execution_time', 0.0))
        throughput = (total_tests / (total_time / 60)) if total_time > 0 else 0.0
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"**Execution Performance**  \n- Average Test Time: **{avg_time:.2f}s**  \n- Total Execution: **{total_time:.1f}s**  \n- Throughput: **{throughput:.1f} tests/min**", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer / Actions
st.markdown('---')
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown('### Framework Benefits')
    st.markdown('- Neutral, executive visual language  \n- Subtle textures and muted tones  \n- Scales to enterprise dashboards')
with col2:
    report_data = {
        'overview': overview,
        'failure_analysis': failure_analysis,
        'performance': performance,
        'ai_insights': ai_insights
    }
    report_json = json.dumps(report_data, indent=2)
    st.download_button('Generate Executive Report (JSON)', data=report_json, file_name='executive_summary.json', mime='application/json')
with col3:
    if st.button('Refresh Data'):
        st.cache_data.clear()

# Sidebar
with st.sidebar:
    st.markdown('## Technical Specifications')
    analyzed_at = analysis_data.get('analyzed_at') if analysis_data else None
    analyzed_str = 'N/A'
    try:
        if analyzed_at:
            # Normalize ISO timestamp if ends with Z
            iso = analyzed_at.replace('Z', '+00:00') if isinstance(analyzed_at, str) else None
            analyzed_str = datetime.fromisoformat(iso).strftime('%Y-%m-%d %H:%M') if iso else analyzed_at
    except Exception:
        analyzed_str = analyzed_at or 'N/A'

    analysis_id = analysis_data.get('analysis_id', 'N/A') if analysis_data else 'N/A'
    st.markdown(f"**Analysis ID:** {analysis_id}  \n**Execution Time:** {analyzed_str}  \n**Framework:** MCP + CrewAI  \n**AI Model:** Ollama/Gemma 3")
    st.markdown('---')
    st.markdown('## Architecture Highlights')
    st.markdown('- Multi-agent orchestration  \n- Real-time analysis  \n- Statistical + ML insights')