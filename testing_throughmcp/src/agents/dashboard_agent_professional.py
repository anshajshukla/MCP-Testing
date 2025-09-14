# dashboard_agent_professional.py
"""
Multi-Agent Test Automation Dashboard
Professional Interview-Ready Streamlit Dashboard

This dashboard showcases the complete MCP Banking Test Framework pipeline:
1. Scenario Analysis → 2. Test Generation → 3. Test Execution → 4. Result Analysis → 5. Insights
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
    page_title="Multi-Agent Test Automation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Corporate Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --primary: #1e40af;
  --secondary: #3b82f6;
  --accent: #60a5fa;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --text: #1f2937;
  --text-light: #6b7280;
  --bg: #f8fafc;
  --card: #ffffff;
  --border: #e5e7eb;
}

.main {
  font-family: 'Inter', sans-serif;
  background: linear-gradient(135deg, #f1f5f9 0%, #ffffff 100%);
}

/* Pipeline Status */
.pipeline-container {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  color: white;
  padding: 2rem;
  border-radius: 16px;
  margin: 1rem 0 2rem 0;
  box-shadow: 0 8px 32px rgba(30, 64, 175, 0.2);
}

.pipeline-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-align: center;
}

.pipeline-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  text-align: center;
  margin-bottom: 2rem;
}

.pipeline-flow {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}

.pipeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255,255,255,0.1);
  padding: 1rem;
  border-radius: 12px;
  min-width: 140px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.pipeline-step.completed {
  background: rgba(16, 185, 129, 0.2);
  border: 2px solid var(--success);
}

.pipeline-step.active {
  background: rgba(245, 158, 11, 0.2);
  border: 2px solid var(--warning);
}

.step-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.step-title {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.step-time {
  font-size: 0.8rem;
  opacity: 0.8;
}

/* Agent Cards */
.agent-card {
  background: var(--card);
  border: none;
  border-radius: 16px;
  padding: 2rem;
  margin: 1rem 0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  border-left: 4px solid var(--accent);
}

.agent-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.agent-icon {
  font-size: 2rem;
  margin-right: 1rem;
  color: var(--primary);
}

.agent-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  margin: 0;
}

.agent-subtitle {
  color: var(--text-light);
  font-size: 0.9rem;
  margin: 0;
}

/* KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.kpi-card {
  background: var(--card);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  border-top: 4px solid var(--accent);
  transition: transform 0.2s ease;
}

.kpi-card:hover {
  transform: translateY(-2px);
}

.kpi-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary);
  margin: 0.5rem 0;
}

.kpi-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kpi-delta {
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.kpi-positive { color: var(--success); }
.kpi-negative { color: var(--danger); }
.kpi-warning { color: var(--warning); }

/* Status Badges */
.status-badge {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-success { background: var(--success); color: white; }
.status-warning { background: var(--warning); color: white; }
.status-danger { background: var(--danger); color: white; }
.status-info { background: var(--accent); color: white; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: var(--card);
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.stTabs [data-baseweb="tab"] {
  background: transparent;
  border-radius: 8px;
  color: var(--text-light);
  font-weight: 500;
  padding: 0.75rem 1.5rem;
}

.stTabs [aria-selected="true"] {
  background: var(--primary) !important;
  color: white !important;
}

/* Download Buttons */
.download-section {
  background: var(--bg);
  padding: 1.5rem;
  border-radius: 12px;
  margin: 2rem 0;
  text-align: center;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

</style>
""", unsafe_allow_html=True)

# Corporate Colors
COLORS = {
    'primary': '#1e40af',
    'secondary': '#3b82f6', 
    'accent': '#60a5fa',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'text': '#1f2937',
    'muted': '#6b7280'
}

def load_pipeline_data():
    """Load all pipeline data files"""
    data_dir = Path("data/output")
    
    # Find latest files
    gap_files = list(data_dir.glob("gap_analysis_*.json")) if data_dir.exists() else []
    test_files = list(data_dir.glob("generated_tests_*.json")) if data_dir.exists() else []
    exec_files = list(data_dir.glob("execution_report_*.json")) if data_dir.exists() else []
    analysis_files = list(data_dir.glob("analysis_summary_*.json")) if data_dir.exists() else []
    
    latest_data = {}
    
    if gap_files:
        latest_gap = max(gap_files, key=lambda x: x.stat().st_mtime)
        try:
            latest_data['gap_analysis'] = json.loads(latest_gap.read_text())
            latest_data['gap_timestamp'] = datetime.fromtimestamp(latest_gap.stat().st_mtime)
        except: pass
    
    if test_files:
        latest_test = max(test_files, key=lambda x: x.stat().st_mtime)
        try:
            latest_data['generated_tests'] = json.loads(latest_test.read_text())
            latest_data['test_timestamp'] = datetime.fromtimestamp(latest_test.stat().st_mtime)
        except: pass
    
    if exec_files:
        latest_exec = max(exec_files, key=lambda x: x.stat().st_mtime)
        try:
            latest_data['execution'] = json.loads(latest_exec.read_text())
            latest_data['exec_timestamp'] = datetime.fromtimestamp(latest_exec.stat().st_mtime)
        except: pass
    
    if analysis_files:
        latest_analysis = max(analysis_files, key=lambda x: x.stat().st_mtime)
        try:
            latest_data['analysis'] = json.loads(latest_analysis.read_text())
            latest_data['analysis_timestamp'] = datetime.fromtimestamp(latest_analysis.stat().st_mtime)
        except: pass
    
    return latest_data

def create_pipeline_status(data):
    """Create pipeline status flow (clean corporate, no symbols)"""
    steps = [
        {"name": "Scenario Docs", "key": "gap_analysis"},
        {"name": "Analyzer Agent", "key": "gap_analysis"},
        {"name": "Generator Agent", "key": "generated_tests"},
        {"name": "Executor Agent", "key": "execution"},
        {"name": "Result Analyzer", "key": "analysis"},
        {"name": "Dashboard", "key": "dashboard"}
    ]

    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline-title">Multi-Agent Test Automation Pipeline</div>
        <div class="pipeline-subtitle">AI-Powered Banking Test Framework • End-to-End Automation</div>
        <div class="pipeline-flow">
    """, unsafe_allow_html=True)

    for step in steps:
        status_class = ""
        timestamp = ""

        if step["key"] in data:
            status_class = "completed"
            if f"{step['key']}_timestamp" in data:
                timestamp = data[f"{step['key']}_timestamp"].strftime("%H:%M:%S")
        elif step["key"] == "dashboard":
            status_class = "active"
            timestamp = datetime.now().strftime("%H:%M:%S")

        st.markdown(f"""
            <div class="pipeline-step {status_class}">
                <div class="step-title">{step['name']}</div>
                <div class="step-time">{timestamp}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

def create_sankey_pipeline(data):
    """Innovative Sankey flow showing pipeline movement"""
    gap = len(((data.get('gap_analysis') or {}).get('gap_analysis_report') or {}).get('missing_test_scenarios', []))
    gen = len((data.get('generated_tests') or {}).get('generated_tests', []))
    exec_summary = (data.get('execution') or {}).get('summary', {})
    total = int(exec_summary.get('total_tests', max(gen, 0)))
    passed = int(exec_summary.get('passed', max(total - 1, 0)))
    failed = int(exec_summary.get('failed', max(total - passed, 0)))

    labels = [
        "Scenario Docs", "Analyzer", "Generator", "Executor", "Passed", "Failed"
    ]
    sources = [0, 1, 2, 3, 3]
    targets = [1, 2, 3, 4, 5]
    values = [max(gap, 1), max(gen, 1), max(total, 1), max(passed, 0), max(failed, 0)]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=18,
            line=dict(color="#eee", width=0.5),
            label=labels,
            color=[COLORS['accent'], COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success'], COLORS['danger']]
        ),
        link=dict(source=sources, target=targets, value=values)
    )])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320)
    st.plotly_chart(fig, use_container_width=True)

def create_agent_timeline(data):
    """Innovative timeline of agent completion"""
    events = []
    now = datetime.now()
    order = [
        ("Analyzer", data.get('gap_timestamp')),
        ("Generator", data.get('test_timestamp')),
        ("Executor", data.get('exec_timestamp')),
        ("Result Analyzer", data.get('analysis_timestamp')),
    ]
    start_base = (order[0][1] or now).replace(microsecond=0)
    prev = start_base
    for name, ts in order:
        end = (ts or prev).replace(microsecond=0)
        if end <= prev:
            end = prev
        events.append(dict(Task=name, Start=prev, Finish=end))
        prev = end
    if events:
        df = pd.DataFrame(events)
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Task",
                          color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning']])
        fig.update_layout(height=320, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

def create_failure_heatmap(data):
    """Innovative heatmap: modules vs priority failures"""
    analysis = (data.get('analysis') or {}).get('statistics', {})
    by_module = (analysis.get('failure_analysis') or {}).get('by_module', {})
    priorities = ['critical', 'high', 'medium', 'low']
    modules = list(by_module.keys())
    if not modules:
        st.info("No failure distribution data available.")
        return
    matrix = []
    for m in modules:
        row = []
        for p in priorities:
            row.append(int(((by_module.get(m) or {}).get('by_priority', {}) or {}).get(p, 0)))
        matrix.append(row)
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=[p.title() for p in priorities],
        y=modules,
        colorscale=[[0, '#e8f2ff'], [0.5, COLORS['accent']], [1, COLORS['danger']]]
    ))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

def create_kpi_grid(data):
    """Create executive KPI overview"""
    exec_data = data.get('execution', {})
    summary = exec_data.get('summary', {})
    
    total_tests = summary.get('total_tests', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    pass_rate = summary.get('pass_rate_percentage', 0)
    exec_time = summary.get('total_execution_time_seconds', 0)
    
    baseline_tests = 7  # Original human tests
    ai_generated = total_tests - baseline_tests
    coverage_increase = ((total_tests / baseline_tests) - 1) * 100 if baseline_tests > 0 else 0
    
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    cols = st.columns(5)
    
    with cols[0]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Tests</div>
            <div class="kpi-value">{total_tests}</div>
            <div class="kpi-delta kpi-positive">+{ai_generated} AI Generated</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        delta_class = "kpi-positive" if pass_rate >= 85 else "kpi-warning" if pass_rate >= 70 else "kpi-negative"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Pass Rate</div>
            <div class="kpi-value">{pass_rate:.1f}%</div>
            <div class="kpi-delta {delta_class}">{passed}/{total_tests} passed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        avg_time = exec_time / total_tests if total_tests > 0 else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Execution Time</div>
            <div class="kpi-value">{exec_time:.1f}s</div>
            <div class="kpi-delta">Avg {avg_time:.2f}s per test</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Failures</div>
            <div class="kpi-value">{failed}</div>
            <div class="kpi-delta kpi-warning">Needs attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[4]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Coverage Boost</div>
            <div class="kpi-value">{coverage_increase:.0f}%</div>
            <div class="kpi-delta kpi-positive">vs Baseline</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_agent_section(title, icon, subtitle, content_func, data):
    """Create standardized agent section"""
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-header">
            <div class="agent-icon">{icon}</div>
            <div>
                <div class="agent-title">{title}</div>
                <div class="agent-subtitle">{subtitle}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    content_func(data)
    st.markdown('</div>', unsafe_allow_html=True)

def analyzer_content(data):
    """Analyzer Agent Output"""
    gap_data = data.get('gap_analysis', {})
    report = gap_data.get('gap_analysis_report', {})
    missing_scenarios = report.get('missing_test_scenarios', [])
    
    if missing_scenarios:
        # Gap Analysis Chart
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Test Coverage Gaps Identified")
            
            # Create category breakdown
            categories = {}
            priorities = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            
            for scenario in missing_scenarios:
                cat = scenario.get('category', 'Other')
                categories[cat] = categories.get(cat, 0) + 1
                priority = scenario.get('priority', 'medium').lower()
                priorities[priority] = priorities.get(priority, 0) + 1
            
            # Category pie chart
            if categories:
                fig_cat = px.pie(
                    values=list(categories.values()),
                    names=list(categories.keys()),
                    title="Coverage Gaps by Category",
                    color_discrete_sequence=[COLORS['primary'], COLORS['accent'], COLORS['warning'], COLORS['success']]
                )
                fig_cat.update_layout(height=300, font=dict(size=12))
                st.plotly_chart(fig_cat, use_container_width=True)
        
        with col2:
            st.subheader("Priority Breakdown")
            
            # Priority metrics
            for priority, count in priorities.items():
                if count > 0:
                    color = {
                        'critical': 'danger',
                        'high': 'warning', 
                        'medium': 'info',
                        'low': 'success'
                    }.get(priority, 'info')
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0;">
                        <span style="text-transform: capitalize; font-weight: 500;">{priority}</span>
                        <span class="status-badge status-{color}">{count}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Detailed gaps table
        st.subheader("Detailed Gap Analysis")
        gap_df = pd.DataFrame([
            {
                'Module': s.get('module', 'N/A'),
                'Scenario': s.get('scenario', 'N/A')[:100] + '...' if len(s.get('scenario', '')) > 100 else s.get('scenario', 'N/A'),
                'Priority': s.get('priority', 'medium'),
                'Category': s.get('category', 'other')
            } for s in missing_scenarios[:10]  # Show top 10
        ])
        st.dataframe(gap_df, use_container_width=True)
    else:
        st.info("No gap analysis data available. Run the pipeline first.")

def generator_content(data):
    """Generator Agent Output"""
    test_data = data.get('generated_tests', {})
    generated_tests = test_data.get('generated_tests', [])
    summary = test_data.get('test_summary', {})
    
    if generated_tests:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("AI-Generated Test Cases")
            
            # Test cases table
            test_df = pd.DataFrame([
                {
                    'Test ID': t.get('test_id', 'N/A'),
                    'Module': t.get('module', 'N/A'),
                    'Scenario': t.get('scenario', 'N/A')[:80] + '...' if len(t.get('scenario', '')) > 80 else t.get('scenario', 'N/A'),
                    'Priority': t.get('priority', 'medium'),
                    'Category': t.get('category', 'unknown')
                } for t in generated_tests
            ])
            st.dataframe(test_df, use_container_width=True)
        
        with col2:
            st.subheader("Generation Summary")
            
            # Category breakdown
            categories = {}
            for test in generated_tests:
                cat = test.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in categories.items():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0;">
                    <span style="text-transform: capitalize;">{cat.replace('_', ' ')}</span>
                    <span style="font-weight: 700; color: {COLORS['primary']};">{count}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Comparison with baseline
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <div style="font-weight: 600; margin-bottom: 0.5rem;">Baseline Comparison</div>
                <div>Original Tests: <strong>7</strong></div>
                <div>AI Generated: <strong>{len(generated_tests)}</strong></div>
                <div style="color: {COLORS['success']};">Increase: <strong>{((len(generated_tests) + 7) / 7 - 1) * 100:.0f}%</strong></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No generated tests available. Run the pipeline first.")

def executor_content(data):
    """Executor Agent Output"""
    exec_data = data.get('execution', {})
    test_results = exec_data.get('test_results', [])
    summary = exec_data.get('summary', {})
    
    if test_results:
        # Execution metrics
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Test Execution Results")
            
            # Results table with status styling
            results_df = pd.DataFrame([
                {
                    'Test ID': t.get('test_id', 'N/A'),
                    'Module': t.get('module', 'N/A'),
                    'Status': 'PASS' if t.get('status') == 'passed' else 'FAIL',
                    'Duration': f"{t.get('execution_time_seconds', 0):.2f}s",
                    'Priority': t.get('priority', 'medium'),
                    'Reason': t.get('failure_reason', 'N/A') if t.get('status') == 'failed' else 'Success'
                } for t in test_results
            ])
            st.dataframe(results_df, use_container_width=True)
        
        with col2:
            st.subheader("Execution Metrics")
            
            # Status distribution pie chart
            status_counts = {'Passed': 0, 'Failed': 0}
            for test in test_results:
                status = 'Passed' if test.get('status') == 'passed' else 'Failed'
                status_counts[status] += 1
            
            fig_status = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                color_discrete_map={'Passed': COLORS['success'], 'Failed': COLORS['danger']},
                title="Test Results Distribution"
            )
            fig_status.update_layout(height=250, font=dict(size=10))
            st.plotly_chart(fig_status, use_container_width=True)
            
            # Performance stats
            durations = [t.get('execution_time_seconds', 0) for t in test_results]
            if durations:
                avg_duration = np.mean(durations)
                max_duration = max(durations)
                min_duration = min(durations)
                
                st.markdown(f"""
                <div style=\"background: #f8fafc; padding: 1rem; border-radius: 8px;\">
                    <div style=\"font-weight: 600; margin-bottom: 0.5rem;\">Performance</div>
                    <div>Avg Duration: <strong>{avg_duration:.2f}s</strong></div>
                    <div>Fastest: <strong>{min_duration:.2f}s</strong></div>
                    <div>Slowest: <strong>{max_duration:.2f}s</strong></div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No execution results available. Run the pipeline first.")

def analyzer_insights_content(data):
    """Result Analyzer Output"""
    analysis_data = data.get('analysis', {})
    statistics = analysis_data.get('statistics', {})
    ai_insights = analysis_data.get('ai_insights', {})
    
    if statistics and ai_insights:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Failure Pattern Analysis")
            
            # Module failure analysis
            failure_by_module = statistics.get('failure_analysis', {}).get('by_module', {})
            if failure_by_module:
                modules = list(failure_by_module.keys())
                failure_rates = [failure_by_module[m].get('failure_rate', 0) for m in modules]
                
                fig_modules = px.bar(
                    x=modules,
                    y=failure_rates,
                    title="Failure Rate by Module",
                    color=failure_rates,
                    color_continuous_scale=['green', 'yellow', 'red']
                )
                fig_modules.update_layout(
                    height=300,
                    xaxis_title="Module",
                    yaxis_title="Failure Rate (%)"
                )
                st.plotly_chart(fig_modules, use_container_width=True)
        
        with col2:
            st.subheader("AI Insights")
            
            # AI-generated insights
            summary = ai_insights.get('summary', 'No insights available')
            critical_issue = ai_insights.get('critical_issue', 'No critical issues identified')
            recommendations = ai_insights.get('recommendations', [])
            
            st.markdown(f"""
            <div style=\"background: #fef3c7; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['warning']};\">
                <div style=\"font-weight: 600; margin-bottom: 0.5rem;\">Summary</div>
                <div style=\"font-size: 0.9rem;\">{summary}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style=\"background: #fecaca; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['danger']}; margin-top: 1rem;\">
                <div style=\"font-weight: 600; margin-bottom: 0.5rem;\">Critical Issue</div>
                <div style=\"font-size: 0.9rem;\">{critical_issue}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Recommendations
            if recommendations:
                st.subheader("Recommendations")
                for i, rec in enumerate(recommendations[:3], 1):
                    st.markdown(f"""
                    <div style="background: #dcfce7; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem; border-left: 3px solid {COLORS['success']};">
                        <strong>{i}.</strong> {rec}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No analysis insights available. Run the pipeline first.")

def create_download_section(data):
    """Create download section for all reports"""
    st.markdown("""
    <div class="download-section">
        <h3 style="margin-bottom: 1.5rem; color: var(--primary);">Export Pipeline Reports</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    with cols[0]:
        if 'gap_analysis' in data:
            st.download_button(
                label="Gap Analysis",
                data=json.dumps(data['gap_analysis'], indent=2),
                file_name=f"gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with cols[1]:
        if 'generated_tests' in data:
            st.download_button(
                label="Generated Tests",
                data=json.dumps(data['generated_tests'], indent=2),
                file_name=f"generated_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with cols[2]:
        if 'execution' in data:
            st.download_button(
                label="Execution Report",
                data=json.dumps(data['execution'], indent=2),
                file_name=f"execution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with cols[3]:
        if 'analysis' in data:
            st.download_button(
                label="Analysis Summary",
                data=json.dumps(data['analysis'], indent=2),
                file_name=f"analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Main Dashboard
def main():
    # Load all pipeline data
    data = load_pipeline_data()
    
    # Pipeline Status Header
    create_pipeline_status(data)
    
    # Executive KPI Overview
    create_kpi_grid(data)
    
    # Agent Outputs in Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Analyzer Agent", 
        "Generator Agent", 
        "Executor Agent", 
        "Result Analyzer", 
        "Executive Summary"
    ])
    
    with tab1:
        create_agent_section(
            "Analyzer Agent", 
            "", 
            "Identifies test coverage gaps and missing scenarios",
            analyzer_content,
            data
        )
    
    with tab2:
        create_agent_section(
            "Generator Agent", 
            "", 
            "Creates comprehensive test cases using AI",
            generator_content,
            data
        )
    
    with tab3:
        create_agent_section(
            "Executor Agent", 
            "", 
            "Executes test cases and collects results",
            executor_content,
            data
        )
    
    with tab4:
        create_agent_section(
            "Result Analyzer", 
            "", 
            "Analyzes patterns and provides AI insights",
            analyzer_insights_content,
            data
        )
    
    with tab5:
        st.markdown("### Executive Summary Dashboard")
        
        if data:
            # Final summary card
            exec_data = data.get('execution', {})
            summary = exec_data.get('summary', {})
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']}); color: white; padding: 2rem; border-radius: 16px; text-align: center; margin: 2rem 0;">
                <h2 style="margin: 0 0 1rem 0;">Pipeline Execution Complete</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">{summary.get('total_tests', 0)}</div>
                        <div style="opacity: 0.9;">Tests Executed</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">{summary.get('failed', 0)}</div>
                        <div style="opacity: 0.9;">Failures</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">Authentication</div>
                        <div style="opacity: 0.9;">Top Risk Area</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">{summary.get('total_execution_time_seconds', 0):.0f}s</div>
                        <div style="opacity: 0.9;">Run Duration</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Innovative visuals row
            v1, v2 = st.columns(2)
            with v1:
                st.markdown("#### Pipeline Flow")
                create_sankey_pipeline(data)
            with v2:
                st.markdown("#### Agent Timeline")
                create_agent_timeline(data)

            st.markdown("#### Failure Heatmap (Module vs Priority)")
            create_failure_heatmap(data)
            
            # Business impact metrics
            st.markdown("### Business Impact")
            
            baseline_tests = 7
            total_tests = summary.get('total_tests', 0)
            ai_generated = total_tests - baseline_tests
            coverage_increase = ((total_tests / baseline_tests) - 1) * 100 if baseline_tests > 0 else 0
            
            impact_cols = st.columns(3)
            
            with impact_cols[0]:
                st.metric(
                    label="Test Coverage Expansion",
                    value=f"{coverage_increase:.0f}%",
                    delta=f"+{ai_generated} AI-generated tests"
                )
            
            with impact_cols[1]:
                st.metric(
                    label="Automation Efficiency", 
                    value="100%",
                    delta="Fully automated pipeline"
                )
            
            with impact_cols[2]:
                avg_time = summary.get('total_execution_time_seconds', 0) / total_tests if total_tests > 0 else 0
                st.metric(
                    label="Avg Test Execution",
                    value=f"{avg_time:.2f}s",
                    delta="Per test case"
                )
        else:
            st.warning("No pipeline data available. Please run the MCP pipeline first by executing `python src/orchestrator.py`")
    
    # Download Section
    if data:
        create_download_section(data)
    
    # Sidebar with pipeline info
    with st.sidebar:
        st.markdown("### Pipeline Control")
        st.info("This dashboard displays results from the latest MCP pipeline execution.")
        
        if st.button("Refresh Data", type="primary"):
            st.rerun()
        
        if data:
            st.markdown("### Latest Run Info")
            if 'analysis_timestamp' in data:
                st.write(f"**Last Analysis:** {data['analysis_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            if 'exec_timestamp' in data:
                st.write(f"**Last Execution:** {data['exec_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("---")
        st.markdown("### Pipeline Commands")
        st.code("python src/orchestrator.py", language="bash")
        st.caption("Run this command to execute the full MCP pipeline")

if __name__ == "__main__":
    main()