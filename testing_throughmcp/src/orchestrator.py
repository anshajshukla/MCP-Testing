#!/usr/bin/env python3
"""
AI Test Suite Orchestrator
Coordinates the Test Analyzer and Test Generator agents in a pipeline.
"""
import json
import asyncio
from pathlib import Path
from datetime import datetime
import sys

# --- CORRECTED IMPORT LOGIC ---
# Add the 'src' directory (the orchestrator's parent) to the path
sys.path.append(str(Path(__file__).parent))
# --- END OF CORRECTION ---

from agents.test_analyzer.test_analyzer import TestAnalyzerAgent
from agents.test_generator.test_generator import TestGeneratorAgent
from agents.test_executor.test_executor import TestExecutorAgent
from agents.result_analyzer.result_analyzer import ResultAnalyzerAgent

class TestSuiteOrchestrator:
    """
    Orchestrates the complete test generation and execution pipeline:
    1. Analyze gaps in existing tests
    2. Generate new tests to fill those gaps
    3. Execute the generated tests and produce reports
    """
    def __init__(self):
        self.analyzer = TestAnalyzerAgent()
        self.generator = TestGeneratorAgent()
        self.executor = TestExecutorAgent()
        self.result_analyzer = ResultAnalyzerAgent()
        self.results = {}

    async def run_pipeline(self, config: dict) -> dict:
        """
        Run the complete test generation pipeline.
        """
        print("🚀 Starting AI Test Suite Generation Pipeline")
        print("=" * 60)
        
        # Step 1: Analyze existing test gaps
        print("\n📊 Phase 1: Analyzing Test Coverage Gaps...")
        print("-" * 40)
        analyzer_inputs = {
            "baseline_tests_path": config["baseline_tests_path"],
            "app_model_path": config["app_model_path"]
        }
        gap_analysis = await self.analyzer.execute(analyzer_inputs)
        
        output_dir = Path(config.get("output_dir", "src/data/output"))
        output_dir.mkdir(parents=True, exist_ok=True)
        gap_analysis_file = output_dir / f"gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        gap_analysis_file.write_text(json.dumps(gap_analysis, indent=2))
        print(f"✅ Gap analysis saved to: {gap_analysis_file}")
        
        if "gap_analysis_report" in gap_analysis:
            report = gap_analysis["gap_analysis_report"]
            if isinstance(report, dict):
                scenarios = report.get("missing_scenarios", [])
                print(f"📌 Found {len(scenarios)} missing test scenarios")
                priority_counts = {}
                for scenario in scenarios:
                    priority = scenario.get("priority", "unknown")
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
                for priority, count in priority_counts.items():
                    print(f"   - {priority.upper()}: {count} scenarios")

        # Step 2: Generate tests for identified gaps
        print("\n🔧 Phase 2: Generating Test Cases...")
        print("-" * 40)
        generator_inputs = {
            "gap_analysis": gap_analysis,
            "app_model_path": config["app_model_path"],
            "validate_tests": config.get("validate_tests", True),
            "output_file": str(output_dir / f"generated_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        }
        generated_tests = await self.generator.execute(generator_inputs)
        
        if "generated_tests" in generated_tests:
            tests = generated_tests["generated_tests"]
            print(f"✅ Generated {len(tests)} test cases")
            if "test_summary" in generated_tests:
                summary = generated_tests["test_summary"]
                print("\n📈 Test Generation Summary:")
                if "by_priority" in summary:
                    print("   By Priority:")
                    for priority, count in summary["by_priority"].items():
                        print(f"      - {priority}: {count}")
                if "by_type" in summary:
                    print("   By Type:")
                    for test_type, count in summary["by_type"].items():
                        print(f"      - {test_type}: {count}")

        # Step 3: Execute the generated tests
        print("\n🚀 Phase 3: Executing Generated Test Cases...")
        print("-" * 40)
        
        # Find the most recent generated tests file
        generated_tests_file = generator_inputs["output_file"]
        if Path(generated_tests_file).exists():
            executor_inputs = {
                "test_cases_path": generated_tests_file,
                "output_dir": str(output_dir)
            }
            execution_report = await self.executor.execute(executor_inputs)
            
            if "error" not in execution_report:
                summary = execution_report["summary"]
                print(f"✅ Executed {summary['total_tests']} test cases")
                print(f"📊 Results: {summary['passed']} passed, {summary['failed']} failed")
                print(f"📈 Pass Rate: {summary['pass_rate_percentage']}%")
                print(f"⏱️  Total Execution Time: {summary['total_execution_time_seconds']}s")
                print(f"📄 Execution Report: {execution_report['execution_id']}")
            else:
                print(f"❌ Test execution failed: {execution_report['error']}")
        else:
            print("❌ Generated tests file not found, skipping execution phase")

        # Step 4: Analyze Results
        print("\n📈 Phase 4: Analyzing Test Results...")
        print("-" * 40)
        analysis_summary = None
        if Path(generated_tests_file).exists() and execution_report and "error" not in execution_report:
            # Save execution report to file for the analyzer
            execution_report_file = output_dir / f"execution_report_{execution_report['execution_id']}.json"
            with open(execution_report_file, 'w') as f:
                json.dump(execution_report, f, indent=2)
            
            analysis_summary = self.result_analyzer.analyze(str(execution_report_file))
            if "error" not in analysis_summary:
                print(f"✅ Analysis complete: {analysis_summary.get('analysis_id', 'N/A')}")
                print(f"📊 Insights generated: {len(analysis_summary.get('ai_insights', {}).get('recommendations', []))} recommendations")
            else:
                print(f"❌ Result analysis failed: {analysis_summary['error']}")
        else:
            print("⚠️  Skipping result analysis - no execution report available")
        
        # Step 5: Launch Dashboard
        print("\n🎯 Phase 5: Launching Executive Dashboard...")
        print("-" * 40)
        try:
            import subprocess
            import webbrowser
            import time
            
            # Launch Streamlit dashboard in background
            dashboard_path = Path(__file__).parent / "agents" / "dashboard_agent_professional.py"
            if dashboard_path.exists():
                print("🚀 Starting Streamlit dashboard...")
                subprocess.Popen([
                    "python", "-m", "streamlit", "run", str(dashboard_path),
                    "--server.headless", "true",
                    "--server.port", "8501"
                ], cwd=Path(__file__).parent.parent)
                
                # Give it a moment to start
                time.sleep(3)
                
                # Open browser
                dashboard_url = "http://localhost:8501"
                print(f"🌐 Dashboard available at: {dashboard_url}")
                webbrowser.open(dashboard_url)
                print("✅ Executive dashboard launched successfully!")
            else:
                print("❌ Dashboard agent not found")
        except Exception as e:
            print(f"⚠️  Dashboard launch failed: {str(e)}")
            print("💡 You can manually run: streamlit run src/agents/dashboard_agent_professional.py")

        print("\n" + "=" * 60)
        print("✨ Complete 5-phase pipeline finished successfully!")
        print("=" * 60)
        print("📋 PHASES COMPLETED:")
        print("   ✅ Phase 1: Gap Analysis")
        print("   ✅ Phase 2: AI Test Generation") 
        print("   ✅ Phase 3: Test Execution")
        print("   ✅ Phase 4: Result Analysis")
        print("   ✅ Phase 5: Executive Dashboard")
        print("=" * 60)

        print("\n" + "=" * 60)
        print("✨ Complete pipeline finished successfully!")
        
        # Return comprehensive results
        return {
            "gap_analysis": gap_analysis,
            "generated_tests": generated_tests,
            "execution_report": execution_report if Path(generated_tests_file).exists() else None,
            "analysis_summary": analysis_summary
        }

async def main():
    """Main entry point."""
    orchestrator = TestSuiteOrchestrator()
    config = {
        "baseline_tests_path": "c:/Users/ansha/Desktop/TESTING/testing_throughmcp/src/data/original_requirements/human_baseline_tests_original.json",
        "app_model_path": "c:/Users/ansha/Desktop/TESTING/testing_throughmcp/src/data/original_requirements/FinClusive_Original_Scenario.md",
        "output_dir": "c:/Users/ansha/Desktop/TESTING/testing_throughmcp/src/data/output",
        "validate_tests": False
    }
    await orchestrator.run_pipeline(config)

if __name__ == "__main__":
    asyncio.run(main())
