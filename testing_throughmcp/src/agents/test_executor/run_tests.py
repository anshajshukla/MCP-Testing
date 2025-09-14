#!/usr/bin/env python3
"""
Test Executor Agent (Real Pytest Runner)

This agent executes the actual pytest suite from the banking_tests project
and converts JUnit XML output into the pipeline's raw_results JSON format.

Inputs (JSON):
  - test_plan: array (ignored for now; present to keep schema compatible)
  - suite_path: optional path to tests to run (defaults to banking_tests/interview_demo)
  - pytest_args: optional list of extra pytest CLI args

Output (JSON):
  - raw_results: stringified JSON array of test results
"""

import json
import sys
import os
import subprocess
import tempfile
import asyncio
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

# Add parent directory to path for base_agent import
sys.path.append(str(Path(__file__).parent.parent))
from base_agent import MCPAgent, run_agent


def run_pytest_and_collect_junit(suite_dir: Path, extra_args: list[str] | None = None) -> Path:
    """Run pytest on the given suite directory and write a JUnit XML report.

    Returns the path to the generated JUnit XML file (even if tests fail).
    Raises if pytest invocation itself crashes.
    """
    junit_path = suite_dir / f"junit_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    cmd = [sys.executable, "-m", "pytest", str(suite_dir), "-q", f"--junitxml={junit_path}"]
    if extra_args:
        cmd.extend(extra_args)

    sys.stderr.write(f"Executing pytest in: {suite_dir}\n")
    sys.stderr.write(f"Command: {' '.join(cmd)}\n")

    # Run pytest with suite_dir as CWD so relative paths inside tests resolve consistently
    proc = subprocess.run(cmd, cwd=str(suite_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Always print pytest stderr to help diagnose failures
    if proc.stdout:
        sys.stderr.write(proc.stdout + "\n")
    if proc.stderr:
        sys.stderr.write(proc.stderr + "\n")

    # Even if returncode != 0 (some tests failed), we still have a JUnit file to parse
    if not junit_path.exists():
        # If junit file not created, bubble up error context
        raise RuntimeError(f"Pytest did not produce JUnit XML at {junit_path}")

    return junit_path


def parse_junit_to_results(junit_file: Path) -> list[dict]:
    """Convert JUnit XML into a standardized list of test result dicts."""
    tree = ET.parse(junit_file)
    root = tree.getroot()

    # Pytest with xunit2 uses <testsuite> containing <testcase> entries
    testcases = root.findall(".//testcase")
    results: list[dict] = []

    for case in testcases:
        name = case.get("name", "")
        classname = case.get("classname", "")  # often module path
        time_str = case.get("time", "0")
        try:
            exec_time = float(time_str)
        except ValueError:
            exec_time = 0.0

        # Determine status and details
        status = "PASS"
        failure_details = ""

        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")

        if failure is not None:
            status = "FAIL"
            failure_details = (failure.get("message") or "").strip()
            # Append text content for additional context
            if failure.text:
                failure_details = (failure_details + "\n" + failure.text.strip()).strip()
        elif error is not None:
            status = "FAIL"
            failure_details = (error.get("message") or "").strip()
            if error.text:
                failure_details = (failure_details + "\n" + error.text.strip()).strip()
        elif skipped is not None:
            status = "SKIPPED"

        # Compose a stable test_id
        test_id = f"{classname}::{name}" if classname else name

        results.append({
            "test_id": test_id,
            "name": name,
            "module": classname or "unknown",
            "status": status if status != "SKIPPED" else "SKIPPED",
            "execution_time": round(exec_time, 4),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "failure_details": failure_details if status == "FAIL" else ""
        })

    return results


class TestExecutorAgent(MCPAgent):
    """Test Executor Agent using MCP base class"""
    
    def __init__(self):
        super().__init__("test-executor", "1.0.0")
    
    async def execute(self, inputs: dict) -> dict:
        """Execute pytest tests based on inputs"""
        self.log("info", "Starting test execution")
        
        agent_dir = Path(__file__).parent
        workspace_root = agent_dir.parents[2]
        
        default_suite = workspace_root / "banking_tests" / "interview_demo"
        suite_path = inputs.get("suite_path")
        suite_dir = Path(suite_path).resolve() if suite_path else default_suite

        if not suite_dir.exists():
            raise FileNotFoundError(f"Test suite path not found: {suite_dir}")

        extra_args = inputs.get("pytest_args") or []
        if not isinstance(extra_args, list):
            extra_args = []

        self.log("info", f"Running tests in: {suite_dir}")
        
        try:
            junit_file = run_pytest_and_collect_junit(suite_dir, extra_args)
            results = parse_junit_to_results(junit_file)
            
            # Encode results as a JSON string for the downstream analyzer
            raw_results = json.dumps(results)
            
            self.log("info", f"Executed {len(results)} tests")
            
            return {
                "raw_results": raw_results,
                "test_count": len(results),
                "executed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log("error", f"Test execution failed: {str(e)}")
            # Return an error result so the pipeline can still render something
            error_result = [{
                "test_id": "executor.error",
                "name": "ExecutorError",
                "module": "executor",
                "status": "FAIL",
                "execution_time": 0.0,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "failure_details": str(e),
            }]
            return {
                "raw_results": json.dumps(error_result),
                "test_count": 1,
                "executed_at": datetime.now().isoformat(),
                "error": str(e)
            }

def main():
    """Main entry point"""
    asyncio.run(run_agent(TestExecutorAgent))


if __name__ == "__main__":
    main()
