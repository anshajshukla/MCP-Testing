#!/usr/bin/env python3
"""
Result Analyzer Agent

This agent is responsible for analyzing raw test results and producing
meaningful metrics and insights.
"""

import json
import sys
import os
import asyncio
from datetime import datetime
from collections import Counter
from pathlib import Path

# Add parent directory to path for base_agent import
sys.path.append(str(Path(__file__).parent.parent))
from base_agent import MCPAgent, run_agent

def analyze_results(raw_results_str):
    """
    Analyze test execution results and generate metrics and insights.
    
    Args:
        raw_results_str: String containing raw test results
        
    Returns:
        Dictionary with analysis results
    """
    try:
        # Parse the raw results string back into JSON
        results = json.loads(raw_results_str)
        
        sys.stderr.write(f"Analyzing results for {len(results)} tests...\n")

        # Basic metrics (handle SKIPPED separately)
        total_tests = len(results)
        skipped_tests = sum(1 for r in results if r.get("status") == "SKIPPED")
        executed_tests = total_tests - skipped_tests
        passed_tests = sum(1 for r in results if r.get("status") == "PASS")
        failed_tests = executed_tests - passed_tests if executed_tests >= 0 else 0
        pass_rate = (passed_tests / executed_tests) * 100 if executed_tests > 0 else 0

        # Average execution time
        avg_execution_time = sum(r["execution_time"] for r in results) / total_tests if total_tests > 0 else 0

        # Results by module
        modules = Counter([r["module"] for r in results])
        module_results = {}
        for module in modules:
            module_tests = [r for r in results if r["module"] == module]
            module_skipped = sum(1 for r in module_tests if r.get("status") == "SKIPPED")
            module_executed = len(module_tests) - module_skipped
            module_passed = sum(1 for r in module_tests if r.get("status") == "PASS")
            module_results[module] = {
                "total": len(module_tests),
                "passed": module_passed,
                "failed": max(module_executed - module_passed, 0),
                "skipped": module_skipped,
                "pass_rate": (module_passed / module_executed) * 100 if module_executed > 0 else 0
            }

        # Failure analysis
        failures = [r for r in results if r.get("status") == "FAIL"]
        failure_details = [{
            "test_id": f["test_id"],
            "name": f["name"],
            "module": f["module"],
            "details": f["failure_details"]
        } for f in failures]

        # Generate recommendations
        recommendations = []
        if pass_rate < 90:
            recommendations.append("Overall pass rate is below 90%. Investigate failing tests before proceeding.")

        for module, stats in module_results.items():
            if stats["pass_rate"] < 75:
                recommendations.append(f"Module '{module}' has a low pass rate of {stats['pass_rate']:.1f}%. Prioritize fixing these tests.")

        # Generate basic failure analysis for failures
        if failures:
            try:
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from ai_analyzer.analyze_errors import ErrorAnalyzer
                analyzer = ErrorAnalyzer()
                failure_analysis = analyzer.analyze_failures(failures, module_results)
            except Exception as e:
                print(f"Error running analysis: {e}")
                failure_analysis = {
                    "failures": failure_details,
                    "insights": {"patterns_detected": [], "testing_gaps": [], "quality_score": 50, "note": "Analysis failed"}
                }
        else:
            failure_analysis = {
                "failures": [],
                "insights": {"patterns_detected": ["All tests passing"], "testing_gaps": [], "quality_score": 95, "note": "No failures to analyze"}
            }

        # Compile the analysis
        analysis = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "skipped_tests": skipped_tests,
                "pass_rate": pass_rate,
                "avg_execution_time": avg_execution_time
            },
            "module_results": module_results,
            "failures": failure_details,
            "recommendations": recommendations,
            "failure_analysis": failure_analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return analysis
        
    except Exception as e:
        sys.stderr.write(f"Error analyzing results: {str(e)}\n")
        # Return a basic error analysis
        return {
            "error": str(e),
            "summary": {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "pass_rate": 0,
                "avg_execution_time": 0
            },
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class ResultAnalyzerAgent(MCPAgent):
    """Result Analyzer Agent using MCP base class"""
    
    def __init__(self):
        super().__init__("result-analyzer", "1.0.0")
    
    async def execute(self, inputs: dict) -> dict:
        """Analyze test results based on inputs"""
        self.validate_inputs(inputs, ["raw_results"])
        
        raw_results = inputs.get("raw_results", "{}")
        self.log("info", f"Analyzing test results")
        
        # Analyze the results
        analysis = analyze_results(raw_results)
        
        self.log("info", f"Analysis completed for {analysis.get('summary', {}).get('total_tests', 0)} tests")
        
        return {
            "analysis": analysis,
            "analyzed_at": datetime.now().isoformat()
        }

def main():
    """Main entry point"""
    asyncio.run(run_agent(ResultAnalyzerAgent))

if __name__ == "__main__":
    main()
