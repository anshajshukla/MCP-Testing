"""
MCP Banking Test Framework
AI-Powered Testing with Multi-Agent Architecture
"""

__version__ = "1.0.0"
__author__ = "Anshaj Shukla"
__description__ = "Model Context Protocol Banking Test Framework with CrewAI Agents"

# Core components
from . import core
from . import agents
from . import tools
from . import config
from . import data
from . import dashboards

__all__ = [
    "core",
    "agents", 
    "tools",
    "config",
    "data",
    "dashboards"
]
