# result_analyzer.py
"""
Hybrid Result Analyzer Agent - Combines statistical analysis with AI insights
"""

# result_analyzer.py
"""
Hybrid Result Analyzer Agent - Combines statistical analysis with AI insights
"""

import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from crewai import Agent, Task, Crew, Process
import sys


class ResultAnalyzerAgent:
    """
    Hybrid Result Analyzer - Uses Python for stats and AI for insights
    """
    
    def __init__(self, output_dir="data/output", llm_model='ollama/gemma3:1b'):
        self.output_dir = output_dir
        self.llm_model = llm_model
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def log(self, level: str, message: str):
        """Simple logging method"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level.upper()}: {message}")
    
    def analyze(self, execution_report_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Main analysis method - combines statistical analysis with AI insights
        """
        self.log("info", f"Starting hybrid analysis of: {execution_report_path}")
        
        # Step 1: Load the execution report
        try:
            with open(execution_report_path, 'r') as f:
                execution_report = json.load(f)
        except Exception as e:
            self.log("error", f"Failed to load report: {str(e)}")
            return {"error": f"Failed to load report: {str(e)}"}
        
        # Step 2: Calculate objective metrics using Python
        self.log("info", "📊 Calculating statistical metrics...")
        stats = self._calculate_statistics(execution_report)
        
        # Step 3: Generate AI insights based on the statistics
        self.log("info", "🤖 Generating AI insights...")
        ai_insights = self._generate_ai_insights(stats, execution_report)
        
        # Step 4: Combine everything into the final analysis
        analysis_summary = {
            "analysis_id": f"ANALYSIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "report_source": execution_report_path,
            "analyzed_at": datetime.now().isoformat(),
            "execution_id": execution_report.get("execution_id", "Unknown"),
            "statistics": stats,
            "ai_insights": ai_insights,
            "recommendations": ai_insights.get("recommendations", [])
        }
        
        # Save the analysis
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.output_dir, f"analysis_summary_{timestamp}.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(analysis_summary, f, indent=2)
        
        self.log("info", f"Analysis saved to: {output_path}")
        
        # Log summary
        self._log_analysis_summary(analysis_summary)
        
        return analysis_summary
    
    def _calculate_statistics(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates objective metrics from the execution report
        """
        stats = {
            "overview": {},
            "failure_analysis": {
                "by_module": defaultdict(lambda: {"total": 0, "failed": 0}),
                "by_category": defaultdict(lambda: {"total": 0, "failed": 0}),
                "by_priority": defaultdict(lambda: {"total": 0, "failed": 0})
            },
            "performance_analysis": {
                "slowest_tests": [],
                "fastest_tests": [],
                "average_execution_time": 0,
                "total_execution_time": 0
            },
            "test_distribution": {
                "baseline_tests": {"total": 0, "passed": 0, "failed": 0},
                "ai_generated_tests": {"total": 0, "passed": 0, "failed": 0}
            }
        }
        
        # Get summary stats
        summary = report.get("summary", {})
        stats["overview"] = {
            "total_tests": summary.get("total_tests", 0),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
            "pass_rate": summary.get("pass_rate_percentage", 0),  # Updated to match actual JSON field
            "execution_duration": summary.get("total_execution_time_seconds", 0)
        }
        
        # Collect all test results
        all_tests = []
        
        # Check if execution_results is a list or dict
        execution_results = report.get("execution_results", [])
        
        if isinstance(execution_results, list):
            # Handle flat list structure (our actual format)
            for test in execution_results:
                all_tests.append(test)
                # Assume all are AI-generated for our current pipeline
                stats["test_distribution"]["ai_generated_tests"]["total"] += 1
                if test.get("status") == "PASSED":
                    stats["test_distribution"]["ai_generated_tests"]["passed"] += 1
                else:
                    stats["test_distribution"]["ai_generated_tests"]["failed"] += 1
        else:
            # Handle structured format (baseline_tests/ai_generated_tests)
            baseline_results = execution_results.get("baseline_tests", [])
            for test in baseline_results:
                all_tests.append(test)
                stats["test_distribution"]["baseline_tests"]["total"] += 1
                if test.get("status") == "PASSED":
                    stats["test_distribution"]["baseline_tests"]["passed"] += 1
                else:
                    stats["test_distribution"]["baseline_tests"]["failed"] += 1
            
            # Process AI-generated tests
            ai_results = execution_results.get("ai_generated_tests", [])
            for test in ai_results:
                all_tests.append(test)
                stats["test_distribution"]["ai_generated_tests"]["total"] += 1
                if test.get("status") == "PASSED":
                    stats["test_distribution"]["ai_generated_tests"]["passed"] += 1
                else:
                    stats["test_distribution"]["ai_generated_tests"]["failed"] += 1
        
        # Analyze failures by dimensions
        for test in all_tests:
            module = test.get("module", "Unknown")
            category = test.get("category", "Unknown")
            priority = test.get("priority", "medium")
            
            # Update counts
            stats["failure_analysis"]["by_module"][module]["total"] += 1
            stats["failure_analysis"]["by_category"][category]["total"] += 1
            stats["failure_analysis"]["by_priority"][priority]["total"] += 1
            
            if test.get("status") == "FAILED":
                stats["failure_analysis"]["by_module"][module]["failed"] += 1
                stats["failure_analysis"]["by_category"][category]["failed"] += 1
                stats["failure_analysis"]["by_priority"][priority]["failed"] += 1
        
        # Convert defaultdicts to regular dicts and calculate failure rates
        for dimension in ["by_module", "by_category", "by_priority"]:
            stats["failure_analysis"][dimension] = dict(stats["failure_analysis"][dimension])
            for key, data in stats["failure_analysis"][dimension].items():
                data["failure_rate"] = round((data["failed"] / data["total"] * 100) if data["total"] > 0 else 0, 2)
        
        # Performance analysis
        if all_tests:
            sorted_by_time = sorted(all_tests, key=lambda x: x.get("execution_time_seconds", 0))
            stats["performance_analysis"]["fastest_tests"] = [
                {"test_id": t.get("test_id", "Unknown"), "time": t.get("execution_time_seconds", 0)} 
                for t in sorted_by_time[:3]
            ]
            stats["performance_analysis"]["slowest_tests"] = [
                {"test_id": t.get("test_id", "Unknown"), "time": t.get("execution_time_seconds", 0)} 
                for t in sorted_by_time[-3:]
            ]
            
            total_time = sum(t.get("execution_time_seconds", 0) for t in all_tests)
            stats["performance_analysis"]["total_execution_time"] = round(total_time, 2)
            stats["performance_analysis"]["average_execution_time"] = round(total_time / len(all_tests), 2)
        
        return stats
    
    def _generate_ai_insights(self, stats: Dict[str, Any], report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uses AI to generate insights and recommendations based on the statistics
        """
        # Prepare a summary for the AI
        stats_summary = self._format_stats_for_ai(stats)
        
        # Find specific failure examples for context
        failed_tests = []
        execution_results = report.get("execution_results", [])
        
        if isinstance(execution_results, list):
            # Handle flat list structure
            for test in execution_results:
                if test.get("status") == "FAILED":
                    failed_tests.append({
                        "id": test.get("test_id", "Unknown"),
                        "name": test.get("test_name", "Unknown"),
                        "module": test.get("module", "Unknown"),
                        "reason": test.get("failure_reason", "Unknown")
                    })
        else:
            # Handle structured format
            for test_type in ["baseline_tests", "ai_generated_tests"]:
                for test in execution_results.get(test_type, []):
                    if test.get("status") == "FAILED":
                        failed_tests.append({
                            "id": test.get("test_id", "Unknown"),
                            "name": test.get("test_name", "Unknown"),
                            "module": test.get("module", "Unknown"),
                            "reason": test.get("failure_reason", "Unknown")
                        })
        
        # If no results found, check alternative structure
        if not failed_tests:
            for test in report.get("results", []):
                if test.get("status") == "FAILED":
                    failed_tests.append({
                        "id": test.get("test_id", "Unknown"),
                        "name": test.get("scenario", "Unknown"),
                        "module": test.get("module", "Unknown"),
                        "reason": test.get("failure_reason", "Unknown")
                    })
        
        # Define the AI analyst
        analyst = Agent(
            role='Senior QA Manager',
            goal='Analyze test execution statistics and provide actionable recommendations',
            backstory="""You are an experienced QA Manager with 15 years in software testing. 
            You excel at finding patterns in test data and translating them into clear, 
            actionable recommendations for development teams.""",
            verbose=True,
            llm=self.llm_model
        )
        
        # Create the analysis task
        task = Task(
            description=f"""
            Analyze these test execution statistics and provide insights:
            
            **Test Execution Statistics:**
            {stats_summary}
            
            **Sample Failed Tests:**
            {json.dumps(failed_tests[:5], indent=2)}
            
            Based on this data, provide:
            1. A brief summary of the key findings (2-3 sentences)
            2. Identification of the most critical issue
            3. 3-5 specific, actionable recommendations
            
            Format your response as a JSON object with this structure:
            {{
              "summary": "Your 2-3 sentence summary",
              "critical_issue": "The most important problem to address",
              "recommendations": [
                "First recommendation",
                "Second recommendation",
                "Third recommendation"
              ]
            }}
            """,
            agent=analyst,
            expected_output="JSON object with summary, critical issue, and recommendations"
        )
        
        # Run the analysis
        crew = Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=True)
        
        try:
            result = crew.kickoff()
            # Clean up the result to extract JSON
            result_str = str(result)
            if "```json" in result_str:
                json_part = result_str.split("```json")[1].split("```")[0]
            elif "```" in result_str:
                json_part = result_str.split("```")[1].split("```")[0]
            else:
                json_part = result_str
            
            insights = json.loads(json_part.strip())
            return insights
        except json.JSONDecodeError:
            self.log("warning", "AI produced invalid JSON, using fallback")
            return self._generate_fallback_insights(stats)
        except Exception as e:
            self.log("error", f"AI analysis failed: {str(e)}")
            return self._generate_fallback_insights(stats)
    
    def _format_stats_for_ai(self, stats: Dict[str, Any]) -> str:
        """
        Formats statistics into a readable summary for the AI
        """
        summary_parts = [
            f"Overall: {stats['overview']['total_tests']} tests executed, "
            f"{stats['overview']['pass_rate']}% pass rate",
            f"\nExecution Time: {stats['performance_analysis']['total_execution_time']}s total, "
            f"{stats['performance_analysis']['average_execution_time']}s average",
            "\n\nFailure Analysis:"
        ]
        
        # Add module failures
        summary_parts.append("\n- By Module:")
        for module, data in sorted(stats['failure_analysis']['by_module'].items(), 
                                 key=lambda x: x[1]['failure_rate'], reverse=True)[:3]:
            if data['failed'] > 0:
                summary_parts.append(f"  • {module}: {data['failure_rate']}% failure rate ({data['failed']}/{data['total']})")
        
        # Add category failures
        summary_parts.append("\n- By Category:")
        for category, data in sorted(stats['failure_analysis']['by_category'].items(), 
                                   key=lambda x: x[1]['failure_rate'], reverse=True)[:3]:
            if data['failed'] > 0:
                summary_parts.append(f"  • {category}: {data['failure_rate']}% failure rate ({data['failed']}/{data['total']})")
        
        # Add performance insights
        if stats['performance_analysis']['slowest_tests']:
            summary_parts.append(f"\n\nPerformance:")
            summary_parts.append(f"- Slowest test: {stats['performance_analysis']['slowest_tests'][0]['test_id']} "
                               f"({stats['performance_analysis']['slowest_tests'][0]['time']}s)")
            summary_parts.append(f"- Fastest test: {stats['performance_analysis']['fastest_tests'][0]['test_id']} "
                               f"({stats['performance_analysis']['fastest_tests'][0]['time']}s)")
        
        # Add test distribution
        summary_parts.append(f"\n\nTest Distribution:")
        baseline = stats['test_distribution']['baseline_tests']
        ai_gen = stats['test_distribution']['ai_generated_tests']
        summary_parts.append(f"- Baseline: {baseline['failed']}/{baseline['total']} failed")
        summary_parts.append(f"- AI-Generated: {ai_gen['failed']}/{ai_gen['total']} failed")
        
        return "\n".join(summary_parts)
    
    def _generate_fallback_insights(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates rule-based insights when AI fails
        """
        insights = {
            "summary": "",
            "critical_issue": "",
            "recommendations": []
        }
        
        # Generate summary
        pass_rate = stats['overview']['pass_rate']
        total_tests = stats['overview']['total_tests']
        failed_tests = stats['overview']['failed']
        
        insights["summary"] = (
            f"Test execution completed with {pass_rate}% pass rate across {total_tests} tests. "
            f"{failed_tests} tests failed, requiring immediate attention. "
        )
        
        # Find critical issue
        worst_module = None
        worst_rate = 0
        for module, data in stats['failure_analysis']['by_module'].items():
            if data['failure_rate'] > worst_rate and data['failed'] > 1:
                worst_module = module
                worst_rate = data['failure_rate']
        
        if worst_module:
            insights["critical_issue"] = f"{worst_module} module showing {worst_rate}% failure rate"
        else:
            insights["critical_issue"] = "No significant failure patterns detected"
        
        # Generate recommendations based on data
        recommendations = []
        
        # Module-based recommendations
        if worst_module and worst_rate > 30:
            recommendations.append(
                f"Prioritize fixing {worst_module} module - it has the highest failure rate at {worst_rate}%"
            )
        
        # Performance recommendations
        if stats['performance_analysis']['slowest_tests']:
            slowest = stats['performance_analysis']['slowest_tests'][0]
            if slowest['time'] > 5.0:
                recommendations.append(
                    f"Optimize test {slowest['test_id']} which takes {slowest['time']}s to execute"
                )
        
        # Test distribution recommendations
        ai_tests = stats['test_distribution']['ai_generated_tests']
        if ai_tests['total'] > 0:
            ai_failure_rate = (ai_tests['failed'] / ai_tests['total'] * 100) if ai_tests['total'] > 0 else 0
            if ai_failure_rate > 20:
                recommendations.append(
                    f"Review AI-generated tests - {ai_failure_rate:.1f}% failure rate suggests they may need refinement"
                )
        
        # Category-based recommendations
        for category, data in stats['failure_analysis']['by_category'].items():
            if category == "Security" and data['failure_rate'] > 25:
                recommendations.append("Conduct security review - multiple security tests are failing")
                break
        
        # General recommendation if few specific issues
        if len(recommendations) < 3:
            recommendations.append("Continue monitoring test stability and address intermittent failures")
        
        insights["recommendations"] = recommendations[:5]  # Limit to 5 recommendations
        
        return insights
    
    def _log_analysis_summary(self, analysis: Dict[str, Any]):
        """
        Logs a human-readable summary of the analysis
        """
        self.log("info", "\n" + "="*60)
        self.log("info", "📊 ANALYSIS SUMMARY")
        self.log("info", "="*60)
        
        # Overview
        stats = analysis['statistics']['overview']
        self.log("info", f"\n📈 Overall Results:")
        self.log("info", f"   • Total Tests: {stats['total_tests']}")
        self.log("info", f"   • Pass Rate: {stats['pass_rate']}%")
        self.log("info", f"   • Failed Tests: {stats['failed']}")
        
        # Critical failures
        self.log("info", f"\n🔍 Failure Hotspots:")
        for module, data in sorted(
            analysis['statistics']['failure_analysis']['by_module'].items(),
            key=lambda x: x[1]['failure_rate'], reverse=True
        )[:3]:
            if data['failed'] > 0:
                self.log("info", f"   • {module}: {data['failure_rate']}% failure rate")
        
        # AI Insights
        ai_insights = analysis.get('ai_insights', {})
        if ai_insights.get('critical_issue'):
            self.log("info", f"\n⚠️  Critical Issue: {ai_insights['critical_issue']}")
        
        # Recommendations
        self.log("info", f"\n💡 Recommendations:")
        for i, rec in enumerate(analysis.get('recommendations', [])[:3], 1):
            self.log("info", f"   {i}. {rec}")
        
        self.log("info", "\n" + "="*60)


def create_sample_execution_report():
    """Creates a sample execution report for testing"""
    report = {
        "execution_id": "EXEC_20240115_140230_ABC123",
        "execution_start": "2024-01-15T14:02:30",
        "execution_end": "2024-01-15T14:05:45",
        "summary": {
            "total_tests": 15,
            "passed": 11,
            "failed": 4,
            "pass_rate": 73.33,
            "total_execution_time_seconds": 67.5,
            "average_execution_time_seconds": 4.5
        },
        "execution_results": {
            "baseline_tests": [
                {"test_id": "FP-001", "test_name": "Full Payment", "status": "PASSED", 
                 "module": "Payments & Rewards", "category": "Happy Path", "priority": "high",
                 "execution_time_seconds": 3.2},
                {"test_id": "SEC-001", "test_name": "OTP Verification", "status": "FAILED",
                 "module": "Security", "category": "Security", "priority": "high",
                 "execution_time_seconds": 7.8, "failure_reason": "OTP timeout"},
                {"test_id": "VAL-001", "test_name": "Input Validation", "status": "PASSED",
                 "module": "Validation", "category": "Negative Path", "priority": "medium",
                 "execution_time_seconds": 2.1}
            ],
            "ai_generated_tests": [
                {"test_id": "AI-SEC-001", "test_name": "Session Timeout", "status": "FAILED",
                 "module": "Security", "category": "Security", "priority": "high",
                 "execution_time_seconds": 8.5, "failure_reason": "Session not invalidated"},
                {"test_id": "AI-PAY-001", "test_name": "Concurrent Payments", "status": "FAILED",
                 "module": "Payments & Rewards", "category": "Edge Case", "priority": "medium",
                 "execution_time_seconds": 6.3, "failure_reason": "Race condition detected"},
                {"test_id": "AI-SEC-002", "test_name": "Brute Force Protection", "status": "FAILED",
                 "module": "Security", "category": "Security", "priority": "high",
                 "execution_time_seconds": 9.2, "failure_reason": "No rate limiting"}
            ]
        }
    }
    
    os.makedirs("data/output", exist_ok=True)
    sample_path = "data/output/sample_execution_report.json"
    with open(sample_path, "w") as f:
        json.dump(report, f, indent=2)
    
    return sample_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Hybrid Result Analyzer Agent')
    parser.add_argument('--report', type=str, help='Path to execution report JSON file')
    args = parser.parse_args()
    
    print("🔍 Hybrid Result Analyzer Agent Demo")
    print("="*60)
    
    # Determine report path
    if args.report:
        report_path = args.report
        print(f"📁 Using provided report: {report_path}")
    else:
        # Create sample data if no report provided
        report_path = create_sample_execution_report()
        print(f"📝 Created sample execution report: {report_path}")
    
    # Run the analyzer
    analyzer = ResultAnalyzerAgent(llm_model='ollama/gemma3:1b')
    
    print("\n🚀 Starting hybrid analysis...")
    print("-"*60)
    
    analysis = analyzer.analyze(report_path)
    
    if "error" not in analysis:
        print(f"\n✅ Analysis complete!")
    else:
        print(f"\n❌ Analysis failed: {analysis['error']}")