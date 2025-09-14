#!/usr/bin/env python3
"""
AI-Powered Test Analyzer Agent using CrewAI and a local Ollama LLM.
Fixed and Windows-ready version using litellm provider approach.
"""

import json
import asyncio
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# --- Base Agent (simplified MCPAgent) ---
class MCPAgent:
    def __init__(self, agent_id: str, version: str):
        self.agent_id = agent_id
        self.version = version

    def log(self, level: str, message: str):
        import datetime
        print(json.dumps({
            "timestamp": datetime.datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "level": level,
            "message": message
        }))

    def validate_inputs(self, inputs: dict, required_keys: list):
        missing = [k for k in required_keys if k not in inputs]
        if missing:
            raise ValueError(f"Missing required inputs: {missing}")

# --- Main Test Analyzer Agent ---
class TestAnalyzerAgent(MCPAgent):
    """
    AI-powered test analyzer using CrewAI and local Ollama.
    """

    def __init__(self):
        super().__init__("ai-test-analyzer-ollama", "1.0.0")

        # Initialize CrewAI agent with litellm-compatible Ollama configuration
        self.analyzer = Agent(
            role="Senior QA Test Analyst",
            goal="Perform comprehensive gap analysis on test coverage and return valid JSON",
            backstory="""You are an expert QA analyst with 15 years of experience
            in financial systems testing. You specialize in identifying missing test
            scenarios, edge cases, and security vulnerabilities. You ALWAYS return
            properly formatted JSON responses.""",
            llm="ollama/gemma3:1b",  # Use litellm provider format
            verbose=True,
            allow_delegation=False
        )
        
        self.log("info", "Successfully initialized CrewAI agent with Ollama provider.")

    def _read_file_content(self, file_path: str) -> str | None:
        try:
            return Path(file_path).read_text()
        except FileNotFoundError:
            self.log("error", f"File not found: {file_path}")
            return None

    async def execute(self, inputs: dict) -> dict:
        """Execute the AI-powered analysis using CrewAI"""
        self.validate_inputs(inputs, ["baseline_tests_path", "app_model_path"])

        baseline_tests = self._read_file_content(inputs["baseline_tests_path"])
        app_model = self._read_file_content(inputs["app_model_path"])

        if not baseline_tests or not app_model:
            return {"error": "Failed to load source files. Cannot perform analysis."}

        # Define the analysis task
        analysis_task = Task(
            description=f"""
            Analyze test coverage gaps for a banking application. Return ONLY valid JSON.

            Application: {app_model[:1000]}
            Current Tests: {baseline_tests}

            Find missing test scenarios across these categories:
            - UI Tests: login, navigation, forms, responsive design
            - API Tests: authentication, transactions, payments, errors  
            - Security Tests: SQL injection, XSS, authentication, authorization
            - Performance Tests: load, stress, scalability
            - Data Tests: boundary values, edge cases, validation

            Return this exact JSON structure (no extra text):
            {{
              "gap_analysis_report": {{
                "summary": "Brief assessment of gaps found",
                "missing_scenarios": [
                  {{
                    "module": "Login System",
                    "scenario": "Test invalid login attempts",
                    "priority": "high",
                    "reason": "Security vulnerability risk",
                    "category": "security_tests",
                    "test_type": "security"
                  }},
                  {{
                    "module": "Payment Processing", 
                    "scenario": "Test transaction timeout handling",
                    "priority": "critical",
                    "reason": "Financial data integrity",
                    "category": "api_tests",
                    "test_type": "functional"
                  }}
                ],
                "category_coverage": {{
                  "ui_tests": 20,
                  "api_tests": 25,
                  "security_tests": 15,
                  "performance_tests": 10,
                  "data_driven_tests": 15
                }},
                "testing_mandate": "Generate comprehensive test cases for all identified gaps"
              }}
            }}
            """,
            expected_output="A comprehensive JSON gap analysis report.",
            agent=self.analyzer
        )

        # Create Crew and run sequentially
        crew = Crew(
            agents=[self.analyzer],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )

        # Run the crew in a thread to avoid blocking
        result = await asyncio.to_thread(crew.kickoff)

        # Attempt to parse JSON from LLM output with better handling
        try:
            # Handle the CrewAI output format - get the raw string
            result_text = str(result).strip()
            self.log("info", f"Raw LLM output (first 200 chars): {result_text[:200]}")
            
            # Try multiple extraction methods
            json_content = None
            
            # Method 1: Look for content between ```json and ```
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                if json_end > json_start:
                    json_content = result_text[json_start:json_end].strip()
            
            # Method 2: Look for content between ``` and ``` (markdown code block)
            elif "```" in result_text and result_text.count("```") >= 2:
                first_block = result_text.find("```") + 3
                second_block = result_text.find("```", first_block)
                if second_block > first_block:
                    json_content = result_text[first_block:second_block].strip()
            
            # Method 3: Look for JSON object boundaries
            elif "{" in result_text and "}" in result_text:
                start = result_text.find("{")
                end = result_text.rfind("}") + 1
                json_content = result_text[start:end]
            
            # Method 4: Use the raw text if it looks like JSON
            elif result_text.startswith("{") and result_text.endswith("}"):
                json_content = result_text
            
            if json_content:
                self.log("info", f"Extracted JSON content (first 200 chars): {json_content[:200]}")
                parsed_result = json.loads(json_content)
                self.log("info", "Successfully parsed gap analysis JSON")
                return parsed_result
            else:
                self.log("warning", "No JSON content found in LLM response")
                
        except (json.JSONDecodeError, ValueError) as e:
            self.log("error", f"Failed to parse JSON: {e}")
        
        # If JSON parsing fails, create a fallback response with some basic scenarios
        self.log("warning", "Creating fallback gap analysis with basic scenarios")
        return {
            "gap_analysis_report": {
                "summary": "Fallback analysis due to JSON parsing issues - comprehensive testing gaps identified",
                "missing_scenarios": [
                    {
                        "module": "User Authentication",
                        "scenario": "Test login with invalid credentials and account lockout",
                        "priority": "critical",
                        "reason": "Security vulnerability - brute force protection",
                        "category": "security_tests",
                        "test_type": "security"
                    },
                    {
                        "module": "Payment Processing",
                        "scenario": "Test payment gateway timeout handling",
                        "priority": "high",
                        "reason": "Financial transaction integrity",
                        "category": "api_tests", 
                        "test_type": "functional"
                    },
                    {
                        "module": "Transaction Management",
                        "scenario": "Test concurrent transaction processing",
                        "priority": "high",
                        "reason": "Data consistency and race conditions",
                        "category": "performance_tests",
                        "test_type": "performance"
                    },
                    {
                        "module": "User Interface",
                        "scenario": "Test responsive design across devices",
                        "priority": "medium",
                        "reason": "User experience and accessibility",
                        "category": "ui_tests",
                        "test_type": "functional"
                    },
                    {
                        "module": "Data Validation",
                        "scenario": "Test boundary value analysis for transaction amounts",
                        "priority": "high",
                        "reason": "Input validation and edge case handling",
                        "category": "data_driven_tests",
                        "test_type": "functional"
                    }
                ],
                "category_coverage": {
                    "ui_tests": 8,
                    "api_tests": 12,
                    "security_tests": 10,
                    "performance_tests": 6,
                    "data_driven_tests": 8
                },
                "testing_mandate": "Generate comprehensive test cases covering UI, API, security, performance, and data validation scenarios for banking application",
                "raw_analysis": str(result)[:1000]  # Include raw response for debugging
            }
        }

# --- Main Entry Point ---
async def main():
    agent = TestAnalyzerAgent()
    inputs = {
        "baseline_tests_path": "src/data/test_data_baseline_human.json",
        "app_model_path": "docs/FinClusive_Scenario.md"
    }
    result = await agent.execute(inputs)
    print("\n--- FINAL AGENT OUTPUT ---")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
