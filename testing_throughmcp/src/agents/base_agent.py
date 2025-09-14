#!/usr/bin/env python3
"""
Enhanced Agent Base Class for Real MCP Server
"""

import json
import sys
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import traceback

class MCPAgent(ABC):
    """Base class for all MCP agents"""
    
    def __init__(self, agent_id: str, version: str = "1.0.0"):
        self.agent_id = agent_id
        self.version = version
        self.start_time = datetime.now()
        self.execution_context = {}
    
    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any], required_fields: list) -> bool:
        """Validate that all required input fields are present"""
        missing_fields = [field for field in required_fields if field not in inputs]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        return True
    
    def log(self, level: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log a message with timestamp and context"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "level": level,
            "message": message
        }
        if extra:
            log_entry.update(extra)
        
        # Print to stderr so it doesn't interfere with JSON output
        print(json.dumps(log_entry), file=sys.stderr)
    
    def set_context(self, key: str, value: Any):
        """Set execution context"""
        self.execution_context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get execution context"""
        return self.execution_context.get(key, default)
    
    async def run(self) -> Dict[str, Any]:
        """Main entry point for agent execution"""
        try:
            # Read input from stdin
            input_data = sys.stdin.read()
            if not input_data:
                raise ValueError("No input data provided")
            
            inputs = json.loads(input_data)
            self.log("info", f"Agent {self.agent_id} starting execution")
            
            # Execute agent logic
            start_time = datetime.now()
            outputs = await self.execute(inputs)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Prepare response
            response = {
                "agent_id": self.agent_id,
                "version": self.version,
                "status": "success",
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "outputs": outputs
            }
            
            self.log("info", f"Agent {self.agent_id} completed successfully", {
                "execution_time": execution_time
            })
            
            # Return JSON response to stdout
            print(json.dumps(response, indent=2))
            return response
            
        except Exception as e:
            error_response = {
                "agent_id": self.agent_id,
                "version": self.version,
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat()
            }
            
            self.log("error", f"Agent {self.agent_id} failed: {str(e)}")
            print(json.dumps(error_response, indent=2))
            sys.exit(1)

async def run_agent(agent_class, *args, **kwargs):
    """Helper function to run an agent"""
    agent = agent_class(*args, **kwargs)
    return await agent.run()
