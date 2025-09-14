"""
Models Package - Data Models for MCP Banking Test Framework
Centralized model management and exports
"""

# Banking models
from .banking_models import (
    # Data classes
    Customer,
    Account, 
    Transaction,
    LoanApplication,
    Card,
    Address,
    
    # Enums
    CustomerStatus,
    AccountStatus,
    TransactionStatus,
    RiskLevel,
    KYCStatus,
    
    # Utility functions
    create_sample_customer,
    create_sample_account,
    create_sample_transaction,
    create_model_instance,
    get_model_schema,
    MODEL_REGISTRY
)

# Test models  
from .test_models import (
    # Data classes
    TestCase,
    TestResult,
    TestSuite,
    TestSuiteResult,
    
    # Enums
    TestStatus,
    TestPriority,
    TestType,
    TestCategory,
    ExecutionMode,
    
    # Utility functions
    create_banking_test_case,
    create_performance_test_case,
    create_test_suite_from_cases,
    create_test_model_instance,
    get_test_model_schema,
    TEST_MODEL_REGISTRY
)

# Combined registry for all models
ALL_MODELS = {
    **MODEL_REGISTRY,
    **TEST_MODEL_REGISTRY
}

# Version information
__version__ = "1.0.0"
__author__ = "MCP Banking Test Framework"

# Model categories for easier organization
BANKING_MODELS = [
    "customer", "account", "transaction", 
    "loan_application", "card", "address"
]

TEST_MODELS = [
    "test_case", "test_result", 
    "test_suite", "test_suite_result"
]

def get_available_models():
    """Get list of all available models"""
    return {
        "banking_models": BANKING_MODELS,
        "test_models": TEST_MODELS,
        "all_models": list(ALL_MODELS.keys())
    }

def create_any_model(model_type: str, **kwargs):
    """Create any model instance from combined registry"""
    if model_type not in ALL_MODELS:
        raise ValueError(f"Unknown model type: {model_type}. Available: {list(ALL_MODELS.keys())}")
    
    model_class = ALL_MODELS[model_type]
    return model_class(**kwargs)

# Export all models and utilities
__all__ = [
    # Banking models
    "Customer", "Account", "Transaction", "LoanApplication", "Card", "Address",
    "CustomerStatus", "AccountStatus", "TransactionStatus", "RiskLevel", "KYCStatus",
    "create_sample_customer", "create_sample_account", "create_sample_transaction",
    
    # Test models
    "TestCase", "TestResult", "TestSuite", "TestSuiteResult",
    "TestStatus", "TestPriority", "TestType", "TestCategory", "ExecutionMode",
    "create_banking_test_case", "create_performance_test_case", "create_test_suite_from_cases",
    
    # Utilities
    "create_model_instance", "get_model_schema", "create_test_model_instance", 
    "get_test_model_schema", "create_any_model", "get_available_models",
    
    # Registries
    "MODEL_REGISTRY", "TEST_MODEL_REGISTRY", "ALL_MODELS",
    
    # Constants
    "BANKING_MODELS", "TEST_MODELS"
]
