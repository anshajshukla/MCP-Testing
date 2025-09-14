#!/usr/bin/env python3
"""
Professional MCP Dashboard Launcher
Quick launcher for interview demonstrations
"""

import subprocess
import webbrowser
import time
import sys
from pathlib import Path

def find_open_port(preferred=8501, max_tries=10):
    import socket
    port = preferred
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    return preferred


def launch_dashboard():
    """Launch the professional dashboard for demos"""
    print("Launching Professional MCP Banking Test Dashboard...")
    print("="*60)
    
    # Get the dashboard path
    dashboard_path = Path(__file__).parent / "src" / "agents" / "dashboard_agent_professional.py"
    
    if not dashboard_path.exists():
        print("ERROR: Dashboard file not found!")
        print(f"Expected: {dashboard_path}")
        return False
    
    try:
        # Launch Streamlit
        port = find_open_port(8501)
        print(f"Starting Streamlit server on port {port}...")
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", str(dashboard_path),
            "--server.headless", "true",
            "--server.port", str(port),
            "--theme.base", "light",
            "--theme.primaryColor", "#1e40af"
        ], cwd=Path(__file__).parent)
        
        # Wait for server to start
        print("Waiting for server to initialize...")
        time.sleep(4)
        
        # Open browser
        dashboard_url = f"http://localhost:{port}"
        print(f"Opening dashboard: {dashboard_url}")
        webbrowser.open(dashboard_url)
        
        print("Professional Dashboard Launched Successfully!")
        print("="*60)
        print("INTERVIEW DEMO READY:")
        print("   • Multi-Agent Pipeline Visualization")
        print("   • Executive KPI Dashboard")
        print("   • AI-Generated Test Insights")
        print("   • Real Banking Test Results")
        print("   • Professional Corporate Theme")
        print("="*60)
        print("Press Ctrl+C to stop the dashboard")
        
        # Keep process alive
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping dashboard...")
            process.terminate()
            print("Dashboard stopped successfully!")
            
    except Exception as e:
        print(f"ERROR: Failed to launch dashboard: {e}")
        print("Try running manually:")
        print(f"   streamlit run {dashboard_path}")
        return False
    
    return True

if __name__ == "__main__":
    launch_dashboard()