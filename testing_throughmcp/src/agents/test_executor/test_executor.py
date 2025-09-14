#!/usr/bin/env python3
"""
AI-Powered Test Executor Agent
Executes generated test cases and produces comprehensive execution reports.
Integrates with Test Analyzer and Test Generator agents.
"""

import json
import random
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys

# --- CORRECTED IMPORT LOGIC ---
# Add the 'src' directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))
from agents.base_agent import MCPAgent
# --- END OF CORRECTION ---

class TestExecutorAgent(MCPAgent):
    """
    AI-powered test executor that simulates test execution
    and generates detailed execution reports.
    """
    
    def __init__(self):
        super().__init__("ai-test-executor", "1.0.0")
        
        # Configuration for test execution simulation
        self.pass_rate = 0.85  # Base pass rate
        self.min_exec_time = 0.5
        self.max_exec_time = 5.0
        
        # Risk-based execution modifiers
        self.priority_modifiers = {
            "critical": {"pass_rate_mod": -0.1, "exec_time_mod": 1.5},
            "high": {"pass_rate_mod": -0.05, "exec_time_mod": 1.2},
            "medium": {"pass_rate_mod": 0.0, "exec_time_mod": 1.0},
            "low": {"pass_rate_mod": 0.05, "exec_time_mod": 0.8}
        }
        
        self.log("info", "Test Executor Agent initialized successfully")
    
    def _read_file_content(self, file_path: str) -> Optional[str]:
        """Read file content with error handling"""
        try:
            return Path(file_path).read_text(encoding='utf-8')
        except FileNotFoundError:
            self.log("error", f"File not found: {file_path}")
            return None
        except Exception as e:
            self.log("error", f"Error reading file {file_path}: {str(e)}")
            return None
    
    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute test cases and generate execution report"""
        
        # Validate inputs
        self.validate_inputs(inputs, ["test_cases_path"])
        
        test_cases_path = inputs["test_cases_path"]
        output_dir = inputs.get("output_dir", "src/data/output")
        
        self.log("info", f"Starting test execution from: {test_cases_path}")
        
        # Load test cases
        test_content = self._read_file_content(test_cases_path)
        if not test_content:
            return {"error": f"Failed to load test cases from {test_cases_path}"}
        
        try:
            test_data = json.loads(test_content)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in test cases file: {str(e)}"}
        
        # Initialize execution report
        execution_id = f"EXEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report = {
            "execution_id": execution_id,
            "execution_start": datetime.now().isoformat(),
            "test_source": test_cases_path,
            "environment": "UAT_SIMULATION",
            "agent_info": {
                "agent_id": self.agent_id,
                "version": self.version
            },
            "execution_results": [],
            "summary": {}
        }
        
        # Execute test cases
        stats = {"total": 0, "passed": 0, "failed": 0, "total_duration": 0}
        
        # Handle different input formats (enhanced_test_cases or generated_tests)
        test_cases = test_data.get("enhanced_test_cases", test_data.get("generated_tests", []))
        
        if not test_cases:
            self.log("error", "No test cases found in the input file")
            return {"error": "No test cases found in the input file"}
        
        self.log("info", f"Found {len(test_cases)} test cases to execute")
        
        for test_case in test_cases:
            result = await self._execute_single_test(test_case)
            report["execution_results"].append(result)
            
            stats["total"] += 1
            if result["status"] == "PASSED":
                stats["passed"] += 1
            else:
                stats["failed"] += 1
            stats["total_duration"] += result["execution_time_seconds"]
        
        # Complete execution report
        report["execution_end"] = datetime.now().isoformat()
        report["summary"] = {
            "total_tests": stats["total"],
            "passed": stats["passed"],
            "failed": stats["failed"],
            "pass_rate_percentage": round((stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0, 2),
            "total_execution_time_seconds": round(stats["total_duration"], 2),
            "average_execution_time_seconds": round(stats["total_duration"] / stats["total"] if stats["total"] > 0 else 0, 2)
        }
        
        # Save execution report
        output_path = Path(output_dir) / f"execution_report_{execution_id}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            output_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
            self.log("info", f"Execution report saved to: {output_path}")
        except Exception as e:
            self.log("error", f"Failed to save execution report: {str(e)}")
        
        # Log summary
        self.log("info", f"Execution completed: {stats['total']} tests, "
                        f"{report['summary']['pass_rate_percentage']}% passed")
        
        return report
    
    async def _execute_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single test case with realistic simulation"""
        
        test_id = test_case.get("test_id", "UNKNOWN")
        module = test_case.get("module", "Unknown")
        priority = test_case.get("priority", "medium")
        test_type = test_case.get("test_type", "functional")
        
        self.log("info", f"Executing {test_id}: {module} [{priority}]")
        
        # Calculate execution time based on test complexity
        base_time = random.uniform(self.min_exec_time, self.max_exec_time)
        modifier = self.priority_modifiers.get(priority, {"exec_time_mod": 1.0})
        execution_time = round(base_time * modifier["exec_time_mod"], 2)
        
        # Simulate actual execution time
        await asyncio.sleep(0.1)  # Small delay for realism
        
        # Determine test result based on various factors
        pass_probability = self._calculate_pass_probability(test_case)
        test_passed = random.random() < pass_probability
        
        # Build execution result
        result = {
            "test_id": test_id,
            "test_name": test_case.get("scenario", "Unnamed Test"),
            "module": module,
            "priority": priority,
            "test_type": test_type,
            "status": "PASSED" if test_passed else "FAILED",
            "execution_time_seconds": execution_time,
            "executed_at": datetime.now().isoformat(),
            "test_steps_executed": len(test_case.get("test_steps", [])),
            "execution_logs": self._generate_execution_logs(test_case, test_passed)
        }
        
        # Add failure details if test failed
        if not test_passed:
            result["failure_reason"] = self._generate_failure_reason(test_case)
            result["error_details"] = self._generate_error_details(test_case)
            result["screenshot_path"] = f"screenshots/{test_id}_failure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            self.log("error", f"Test {test_id} FAILED: {result['failure_reason']}")
        else:
            self.log("info", f"Test {test_id} PASSED in {execution_time}s")
        
        return result
    
    def _calculate_pass_probability(self, test_case: Dict[str, Any]) -> float:
        """Calculate pass probability based on test characteristics"""
        
        base_probability = self.pass_rate
        
        # Adjust based on priority
        priority = test_case.get("priority", "medium")
        if priority in self.priority_modifiers:
            base_probability += self.priority_modifiers[priority]["pass_rate_mod"]
        
        # Adjust based on test type
        test_type = test_case.get("test_type", "")
        if "security" in test_type.lower():
            base_probability -= 0.15  # Security tests are more likely to fail
        if "validation" in test_type.lower():
            base_probability -= 0.1   # Validation tests are stricter
        if "functional" in test_type.lower():
            base_probability += 0.05  # Functional tests are more stable
        
        # Ensure probability is within bounds
        return max(0.1, min(0.95, base_probability))
    
    def _generate_failure_reason(self, test_case: Dict[str, Any]) -> str:
        """Generate realistic failure reasons based on test characteristics"""
        
        module = test_case.get("module", "").lower()
        test_type = test_case.get("test_type", "").lower()
        
        failure_scenarios = {
            "user registration": [
                "Mobile number validation failed",
                "Duplicate registration attempt detected",
                "Card number format validation error",
                "OTP verification timeout"
            ],
            "security": [
                "Authentication token expired",
                "Session security violation",
                "OTP verification failed after 3 attempts",
                "Access control validation failed"
            ],
            "payment": [
                "Payment gateway connection timeout",
                "Transaction validation failed",
                "Insufficient balance validation error",
                "Payment method verification failed"
            ],
            "rewards": [
                "Reward point calculation mismatch",
                "Cashback credit failed",
                "Tier upgrade validation error",
                "Point redemption limit exceeded"
            ],
            "validation": [
                "Input boundary condition failed",
                "Data format validation error",
                "Required field validation missed",
                "Invalid data accepted by system"
            ]
        }
        
        # Select appropriate failure reason
        for key, reasons in failure_scenarios.items():
            if key in module or key in test_type:
                return random.choice(reasons)
        
        # Default failure reasons
        default_reasons = [
            "Assertion failed on expected result",
            "Element not found on page",
            "Unexpected system behavior",
            "API response validation failed",
            "Database state inconsistency"
        ]
        
        return random.choice(default_reasons)
    
    def _generate_error_details(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed error information for failed tests"""
        
        return {
            "error_type": "AssertionError",
            "error_location": f"Step {random.randint(1, len(test_case.get('test_steps', [1])))}",
            "expected_behavior": random.choice(test_case.get("expected_results", ["System should behave correctly"])),
            "actual_behavior": "System did not behave as expected",
            "browser_console_errors": [
                "TypeError: Cannot read property 'value' of null",
                "403 Forbidden: Access denied"
            ],
            "network_status": "Connection stable",
            "retry_suggested": True
        }
    
    def _generate_execution_logs(self, test_case: Dict[str, Any], passed: bool) -> List[str]:
        """Generate realistic execution logs"""
        
        logs = [
            f"[START] Test execution started: {test_case.get('test_id', 'UNKNOWN')}",
            f"[INFO] Module: {test_case.get('module', 'Unknown')}",
            f"[INFO] Priority: {test_case.get('priority', 'medium')}",
            f"[SETUP] Preconditions verified: {test_case.get('preconditions', 'None specified')}"
        ]
        
        # Add step execution logs
        test_steps = test_case.get("test_steps", [])
        for i, step in enumerate(test_steps[:5], 1):  # Limit to first 5 steps
            step_text = step[:60] + "..." if len(step) > 60 else step
            logs.append(f"[STEP {i}] {step_text}")
            
            if not passed and i == len(test_steps):
                logs.append(f"[ERROR] Step {i} failed - test execution stopped")
                break
            else:
                logs.append(f"[STEP {i}] ✓ Success")
        
        # Add final status
        if passed:
            logs.extend([
                "[VALIDATION] All expected results verified",
                "[CLEANUP] Postconditions satisfied",
                "[END] Test PASSED"
            ])
        else:
            logs.extend([
                "[VALIDATION] Expected result not achieved",
                "[ERROR] Test execution failed",
                "[END] Test FAILED"
            ])
        
        return logs


# --- Main Entry Point for Testing ---
async def main():
    """Test the executor agent with sample data"""
    executor = TestExecutorAgent()
    
    # Test with the most recent generated test file (adjust path for execution context)
    inputs = {
        "test_cases_path": "../../data/output/generated_tests_20250912_010532.json",
        "output_dir": "../../data/output"
    }
    
    result = await executor.execute(inputs)
    
    if "error" not in result:
        print("\n=== EXECUTION SUMMARY ===")
        print(f"Total Tests: {result['summary']['total_tests']}")
        print(f"Passed: {result['summary']['passed']}")
        print(f"Failed: {result['summary']['failed']}")
        print(f"Pass Rate: {result['summary']['pass_rate_percentage']}%")
        print(f"Total Time: {result['summary']['total_execution_time_seconds']}s")
        print(f"Report ID: {result['execution_id']}")
    else:
        print(f"❌ Execution failed: {result['error']}")


if __name__ == "__main__":
    asyncio.run(main())