"""
MCP CrewAI Integration Configuration
Configuration for integrating CrewAI with Hugging Face models in the MCP system
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: str  # 'huggingface', 'openai', 'anthropic'
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    
class MCPLLMConfig:
    """Central configuration for MCP LLM integration"""
    
    # Hugging Face Models Configuration
    HF_MODELS = {
        "code_generation": {
            "model_name": "microsoft/DialoGPT-medium",
            "temperature": 0.3,
            "max_tokens": 1024
        },
        "test_analysis": {
            "model_name": "google/flan-t5-base", 
            "temperature": 0.5,
            "max_tokens": 512
        },
        "general_chat": {
            "model_name": "microsoft/DialoGPT-large",
            "temperature": 0.7,
            "max_tokens": 2048
        }
    }
    
    # CrewAI Agent Configurations
    CREW_AGENTS = {
        "test_generator": {
            "role": "Banking Test Generator",
            "goal": "Generate comprehensive test cases for banking applications",
            "backstory": "Expert in banking domain testing with deep knowledge of financial regulations and testing best practices",
            "llm_config": "code_generation"
        },
        "test_executor": {
            "role": "Test Execution Specialist", 
            "goal": "Execute test cases efficiently and capture detailed results",
            "backstory": "Specialized in automated test execution and result analysis",
            "llm_config": "general_chat"
        },
        "result_analyzer": {
            "role": "Test Results Analyst",
            "goal": "Analyze test results and provide actionable insights",
            "backstory": "Expert in test result interpretation and quality metrics analysis",
            "llm_config": "test_analysis"
        },
        "dashboard_reporter": {
            "role": "Dashboard Reporter",
            "goal": "Create comprehensive dashboards and reports from test results",
            "backstory": "Visualization expert specialized in creating meaningful test reports and dashboards",
            "llm_config": "general_chat"
        }
    }
    
    @classmethod
    def get_llm_config(cls, config_name: str) -> LLMConfig:
        """Get LLM configuration by name"""
        # Read token lazily to ensure .env is already loaded
        hf_token = os.getenv("HUGGINGFACE_API_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or ""
        if config_name in cls.HF_MODELS:
            hf_config = cls.HF_MODELS[config_name]
            return LLMConfig(
                provider="huggingface",
                model_name=hf_config["model_name"],
                api_key=hf_token,
                temperature=hf_config["temperature"],
                max_tokens=hf_config["max_tokens"]
            )
        else:
            # Default configuration
            return LLMConfig(
                provider="huggingface",
                model_name="microsoft/DialoGPT-medium",
                api_key=hf_token,
                temperature=0.7,
                max_tokens=1024
            )
    
    @classmethod
    def get_agent_config(cls, agent_name: str) -> Dict[str, Any]:
        """Get agent configuration by name"""
        return cls.CREW_AGENTS.get(agent_name, {})
