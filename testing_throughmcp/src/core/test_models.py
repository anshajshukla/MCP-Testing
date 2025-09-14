"""
Test Models - Test Management and Execution Models for MCP Framework
Comprehensive models for test case management, execution tracking, and results
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid
import json

# Enums for test management
class TestStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

class TestPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    REGRESSION = "regression"
    SMOKE = "smoke"
    ACCEPTANCE = "acceptance"

class TestCategory(Enum):
    AUTHENTICATION = "authentication"
    ACCOUNT_MANAGEMENT = "account_management"
    TRANSACTION_PROCESSING = "transaction_processing"
    PAYMENT_PROCESSING = "payment_processing"
    LOAN_PROCESSING = "loan_processing"
    CARD_OPERATIONS = "card_operations"
    FRAUD_DETECTION = "fraud_detection"
    COMPLIANCE = "compliance"
    REPORTING = "reporting"
    API = "api"
    UI = "ui"

class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DISTRIBUTED = "distributed"

# Core Test Models
@dataclass
class TestCase:
    """Individual test case model with comprehensive tracking"""
    test_id: str = field(default_factory=lambda: f"TEST_{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    description: str = ""
    test_type: TestType = TestType.FUNCTIONAL
    category: TestCategory = TestCategory.API
    priority: TestPriority = TestPriority.MEDIUM
    status: TestStatus = TestStatus.PENDING
    tags: List[str] = field(default_factory=list)
    
    # Test implementation details
    test_function: str = ""  # Function name or path
    test_data: Dict[str, Any] = field(default_factory=dict)
    prerequisites: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    # Execution details
    timeout_seconds: int = 300
    retry_count: int = 0
    max_retries: int = 3
    
    # Results
    execution_count: int = 0
    pass_count: int = 0
    fail_count: int = 0
    last_executed: Optional[datetime] = None
    last_result: Optional['TestResult'] = None
    execution_history: List['TestResult'] = field(default_factory=list)
    
    # Banking-specific attributes
    banking_scenario: Optional[str] = None
    customer_type: Optional[str] = None
    account_type: Optional[str] = None
    transaction_type: Optional[str] = None
    
    # Metadata
    created_by: str = "system"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def pass_rate(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return (self.pass_count / self.execution_count) * 100
    
    @property
    def average_execution_time(self) -> float:
        if not self.execution_history:
            return 0.0
        
        durations = [result.duration for result in self.execution_history if result.duration]
        return sum(durations) / len(durations) if durations else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "name": self.name,
            "description": self.description,
            "test_type": self.test_type.value,
            "category": self.category.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "tags": self.tags,
            "test_function": self.test_function,
            "test_data": self.test_data,
            "prerequisites": self.prerequisites,
            "dependencies": self.dependencies,
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "execution_count": self.execution_count,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "pass_rate": self.pass_rate,
            "average_execution_time": self.average_execution_time,
            "last_executed": self.last_executed.isoformat() if self.last_executed else None,
            "banking_scenario": self.banking_scenario,
            "customer_type": self.customer_type,
            "account_type": self.account_type,
            "transaction_type": self.transaction_type,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }

@dataclass
class TestResult:
    """Test execution result with comprehensive tracking"""
    result_id: str = field(default_factory=lambda: f"RESULT_{uuid.uuid4().hex[:8].upper()}")
    test_id: str = ""
    test_name: str = ""
    status: TestStatus = TestStatus.PENDING
    
    # Execution timing
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: float = 0.0  # seconds
    
    # Result details
    message: str = ""
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    stack_trace: Optional[str] = None
    
    # Performance metrics
    memory_usage: float = 0.0  # MB
    cpu_usage: float = 0.0  # percentage
    network_calls: int = 0
    database_queries: int = 0
    
    # Banking-specific results
    banking_operations: List[str] = field(default_factory=list)
    transaction_verified: bool = False
    account_balance_checked: bool = False
    compliance_verified: bool = False
    
    # Evidence and artifacts
    screenshots: List[str] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    
    # Context
    environment: str = "test"
    test_data_used: Dict[str, Any] = field(default_factory=dict)
    browser_info: Optional[Dict[str, str]] = None
    system_info: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    execution_id: str = field(default_factory=lambda: f"EXEC_{uuid.uuid4().hex[:6].upper()}")
    agent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_passed(self) -> bool:
        return self.status == TestStatus.PASSED
    
    @property
    def is_failed(self) -> bool:
        return self.status in [TestStatus.FAILED, TestStatus.ERROR, TestStatus.TIMEOUT]
    
    @property
    def execution_summary(self) -> str:
        if self.is_passed:
            return f"✅ {self.test_name} passed in {self.duration:.2f}s"
        elif self.is_failed:
            return f"❌ {self.test_name} failed: {self.error_message or self.message}"
        else:
            return f"⏸️ {self.test_name} {self.status.value}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "test_id": self.test_id,
            "test_name": self.test_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "message": self.message,
            "error_message": self.error_message,
            "error_type": self.error_type,
            "stack_trace": self.stack_trace,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "network_calls": self.network_calls,
            "database_queries": self.database_queries,
            "banking_operations": self.banking_operations,
            "transaction_verified": self.transaction_verified,
            "account_balance_checked": self.account_balance_checked,
            "compliance_verified": self.compliance_verified,
            "screenshots": self.screenshots,
            "logs": self.logs,
            "artifacts": self.artifacts,
            "environment": self.environment,
            "test_data_used": self.test_data_used,
            "browser_info": self.browser_info,
            "system_info": self.system_info,
            "execution_id": self.execution_id,
            "agent_id": self.agent_id,
            "is_passed": self.is_passed,
            "is_failed": self.is_failed,
            "execution_summary": self.execution_summary,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }

@dataclass
class TestSuite:
    """Collection of related test cases with execution management"""
    suite_id: str = field(default_factory=lambda: f"SUITE_{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    description: str = ""
    test_cases: List[TestCase] = field(default_factory=list)
    
    # Suite configuration
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    parallel_workers: int = 4
    timeout_minutes: int = 60
    setup_steps: List[str] = field(default_factory=list)
    teardown_steps: List[str] = field(default_factory=list)
    
    # Banking-specific configuration
    banking_environment: str = "test"
    test_data_set: str = "default"
    compliance_checks: List[str] = field(default_factory=list)
    
    # Execution tracking
    last_executed: Optional[datetime] = None
    execution_count: int = 0
    results: List['TestSuiteResult'] = field(default_factory=list)
    
    # Metadata
    created_by: str = "system"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def total_tests(self) -> int:
        return len(self.test_cases)
    
    @property
    def last_result(self) -> Optional['TestSuiteResult']:
        return self.results[-1] if self.results else None
    
    @property
    def pass_rate(self) -> float:
        if not self.last_result:
            return 0.0
        return self.last_result.pass_rate
    
    def add_test_case(self, test_case: TestCase):
        """Add a test case to the suite"""
        self.test_cases.append(test_case)
        self.updated_at = datetime.now()
    
    def get_tests_by_category(self, category: TestCategory) -> List[TestCase]:
        """Get tests filtered by category"""
        return [test for test in self.test_cases if test.category == category]
    
    def get_tests_by_priority(self, priority: TestPriority) -> List[TestCase]:
        """Get tests filtered by priority"""
        return [test for test in self.test_cases if test.priority == priority]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "suite_id": self.suite_id,
            "name": self.name,
            "description": self.description,
            "total_tests": self.total_tests,
            "execution_mode": self.execution_mode.value,
            "parallel_workers": self.parallel_workers,
            "timeout_minutes": self.timeout_minutes,
            "setup_steps": self.setup_steps,
            "teardown_steps": self.teardown_steps,
            "banking_environment": self.banking_environment,
            "test_data_set": self.test_data_set,
            "compliance_checks": self.compliance_checks,
            "last_executed": self.last_executed.isoformat() if self.last_executed else None,
            "execution_count": self.execution_count,
            "pass_rate": self.pass_rate,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }

@dataclass
class TestSuiteResult:
    """Results from executing a test suite"""
    suite_result_id: str = field(default_factory=lambda: f"SUITE_RESULT_{uuid.uuid4().hex[:8].upper()}")
    suite_id: str = ""
    suite_name: str = ""
    
    # Execution timing
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: float = 0.0  # seconds
    
    # Test results
    test_results: List[TestResult] = field(default_factory=list)
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    error_tests: int = 0
    
    # Performance metrics
    total_memory_usage: float = 0.0
    peak_memory_usage: float = 0.0
    total_cpu_usage: float = 0.0
    peak_cpu_usage: float = 0.0
    
    # Banking-specific metrics
    banking_operations_count: int = 0
    compliance_checks_passed: int = 0
    compliance_checks_failed: int = 0
    
    # Environment info
    environment: str = "test"
    test_data_set: str = "default"
    execution_agent: Optional[str] = None
    
    # Metadata
    execution_id: str = field(default_factory=lambda: f"EXEC_{uuid.uuid4().hex[:6].upper()}")
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def pass_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100
    
    @property
    def is_successful(self) -> bool:
        return self.failed_tests == 0 and self.error_tests == 0
    
    @property
    def summary(self) -> str:
        return f"Tests: {self.total_tests}, Passed: {self.passed_tests}, Failed: {self.failed_tests}, Pass Rate: {self.pass_rate:.1f}%"
    
    def add_test_result(self, test_result: TestResult):
        """Add a test result and update counters"""
        self.test_results.append(test_result)
        self.total_tests += 1
        
        if test_result.status == TestStatus.PASSED:
            self.passed_tests += 1
        elif test_result.status == TestStatus.FAILED:
            self.failed_tests += 1
        elif test_result.status == TestStatus.SKIPPED:
            self.skipped_tests += 1
        elif test_result.status in [TestStatus.ERROR, TestStatus.TIMEOUT]:
            self.error_tests += 1
        
        # Update performance metrics
        self.total_memory_usage += test_result.memory_usage
        self.peak_memory_usage = max(self.peak_memory_usage, test_result.memory_usage)
        self.total_cpu_usage += test_result.cpu_usage
        self.peak_cpu_usage = max(self.peak_cpu_usage, test_result.cpu_usage)
        
        # Update banking metrics
        self.banking_operations_count += len(test_result.banking_operations)
        if test_result.compliance_verified:
            self.compliance_checks_passed += 1
        else:
            self.compliance_checks_failed += 1
    
    def finalize(self):
        """Finalize the suite result"""
        self.end_time = datetime.now()
        if self.start_time:
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "suite_result_id": self.suite_result_id,
            "suite_id": self.suite_id,
            "suite_name": self.suite_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "skipped_tests": self.skipped_tests,
            "error_tests": self.error_tests,
            "pass_rate": self.pass_rate,
            "is_successful": self.is_successful,
            "summary": self.summary,
            "total_memory_usage": self.total_memory_usage,
            "peak_memory_usage": self.peak_memory_usage,
            "total_cpu_usage": self.total_cpu_usage,
            "peak_cpu_usage": self.peak_cpu_usage,
            "banking_operations_count": self.banking_operations_count,
            "compliance_checks_passed": self.compliance_checks_passed,
            "compliance_checks_failed": self.compliance_checks_failed,
            "environment": self.environment,
            "test_data_set": self.test_data_set,
            "execution_agent": self.execution_agent,
            "execution_id": self.execution_id,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }

# Utility functions for test management
def create_banking_test_case(name: str, category: TestCategory, banking_scenario: str) -> TestCase:
    """Create a banking-specific test case"""
    return TestCase(
        name=name,
        description=f"Banking test case for {banking_scenario}",
        test_type=TestType.FUNCTIONAL,
        category=category,
        priority=TestPriority.HIGH,
        banking_scenario=banking_scenario,
        tags=["banking", category.value, banking_scenario]
    )

def create_performance_test_case(name: str, timeout_seconds: int = 60) -> TestCase:
    """Create a performance test case"""
    return TestCase(
        name=name,
        description=f"Performance test: {name}",
        test_type=TestType.PERFORMANCE,
        category=TestCategory.API,
        priority=TestPriority.HIGH,
        timeout_seconds=timeout_seconds,
        tags=["performance", "api"]
    )

def create_test_suite_from_cases(name: str, test_cases: List[TestCase]) -> TestSuite:
    """Create a test suite from a list of test cases"""
    suite = TestSuite(
        name=name,
        description=f"Test suite containing {len(test_cases)} test cases",
        test_cases=test_cases
    )
    return suite

# Test model registry
TEST_MODEL_REGISTRY = {
    "test_case": TestCase,
    "test_result": TestResult,
    "test_suite": TestSuite,
    "test_suite_result": TestSuiteResult
}

def create_test_model_instance(model_type: str, **kwargs) -> Any:
    """Create a test model instance dynamically"""
    if model_type not in TEST_MODEL_REGISTRY:
        raise ValueError(f"Unknown test model type: {model_type}")
    
    model_class = TEST_MODEL_REGISTRY[model_type]
    return model_class(**kwargs)

def get_test_model_schema(model_type: str) -> Dict[str, Any]:
    """Get the schema for a test model type"""
    if model_type not in TEST_MODEL_REGISTRY:
        raise ValueError(f"Unknown test model type: {model_type}")
    
    model_class = TEST_MODEL_REGISTRY[model_type]
    return {
        "model_type": model_type,
        "fields": [field.name for field in model_class.__dataclass_fields__.values()],
        "enums": {
            "TestStatus": [status.value for status in TestStatus],
            "TestPriority": [priority.value for priority in TestPriority],
            "TestType": [test_type.value for test_type in TestType],
            "TestCategory": [category.value for category in TestCategory],
            "ExecutionMode": [mode.value for mode in ExecutionMode]
        }
    }
