"""
Banking Models - Data Models for MCP Banking Test Framework
Comprehensive data models for banking operations and test management
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
import uuid

# Enums for consistent data types
class CustomerStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CLOSED = "closed"

class AccountStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    FROZEN = "frozen"

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PROCESSING = "processing"
    DECLINED = "declined"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class KYCStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"

# Core Banking Models
@dataclass
class Address:
    """Address information for customers"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country
        }

@dataclass
class Customer:
    """Banking customer model with comprehensive information"""
    customer_id: str = field(default_factory=lambda: f"CUST_{uuid.uuid4().hex[:8].upper()}")
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    date_of_birth: Optional[date] = None
    ssn: str = ""
    address: Optional[Address] = None
    credit_score: int = 0
    customer_since: Optional[date] = None
    status: CustomerStatus = CustomerStatus.ACTIVE
    risk_level: RiskLevel = RiskLevel.MEDIUM
    kyc_status: KYCStatus = KYCStatus.NOT_STARTED
    account_ids: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "age": self.age,
            "ssn": self.ssn,
            "address": self.address.to_dict() if self.address else None,
            "credit_score": self.credit_score,
            "customer_since": self.customer_since.isoformat() if self.customer_since else None,
            "status": self.status.value,
            "risk_level": self.risk_level.value,
            "kyc_status": self.kyc_status.value,
            "account_ids": self.account_ids,
            "preferences": self.preferences,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

@dataclass
class Account:
    """Banking account model with detailed financial information"""
    account_id: str = field(default_factory=lambda: f"ACC_{uuid.uuid4().hex[:8].upper()}")
    customer_id: str = ""
    account_type: str = "checking"
    account_number: str = ""
    routing_number: str = ""
    balance: Decimal = field(default_factory=lambda: Decimal("0.00"))
    available_balance: Decimal = field(default_factory=lambda: Decimal("0.00"))
    currency: str = "USD"
    status: AccountStatus = AccountStatus.ACTIVE
    opened_date: Optional[date] = None
    closed_date: Optional[date] = None
    last_activity: Optional[datetime] = None
    overdraft_limit: Decimal = field(default_factory=lambda: Decimal("0.00"))
    overdraft_fee: Decimal = field(default_factory=lambda: Decimal("35.00"))
    interest_rate: float = 0.0
    minimum_balance: Decimal = field(default_factory=lambda: Decimal("0.00"))
    monthly_fee: Decimal = field(default_factory=lambda: Decimal("0.00"))
    fee_waiver_balance: Decimal = field(default_factory=lambda: Decimal("1500.00"))
    transaction_limits: Dict[str, Decimal] = field(default_factory=dict)
    features: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def is_overdrawn(self) -> bool:
        return self.balance < 0
    
    @property
    def available_overdraft(self) -> Decimal:
        if self.overdraft_limit > 0:
            return max(Decimal("0.00"), self.overdraft_limit + self.balance)
        return Decimal("0.00")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "account_type": self.account_type,
            "account_number": self.account_number,
            "routing_number": self.routing_number,
            "balance": str(self.balance),
            "available_balance": str(self.available_balance),
            "currency": self.currency,
            "status": self.status.value,
            "opened_date": self.opened_date.isoformat() if self.opened_date else None,
            "closed_date": self.closed_date.isoformat() if self.closed_date else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "overdraft_limit": str(self.overdraft_limit),
            "overdraft_fee": str(self.overdraft_fee),
            "interest_rate": self.interest_rate,
            "minimum_balance": str(self.minimum_balance),
            "monthly_fee": str(self.monthly_fee),
            "fee_waiver_balance": str(self.fee_waiver_balance),
            "transaction_limits": {k: str(v) for k, v in self.transaction_limits.items()},
            "features": self.features,
            "is_overdrawn": self.is_overdrawn,
            "available_overdraft": str(self.available_overdraft),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

@dataclass
class Transaction:
    """Banking transaction model with comprehensive tracking"""
    transaction_id: str = field(default_factory=lambda: f"TXN_{uuid.uuid4().hex[:8].upper()}")
    account_id: str = ""
    transaction_type: str = "payment"
    amount: Decimal = field(default_factory=lambda: Decimal("0.00"))
    currency: str = "USD"
    description: str = ""
    merchant: Optional[str] = None
    merchant_category: Optional[str] = None
    location: Optional[str] = None
    status: TransactionStatus = TransactionStatus.PENDING
    timestamp: datetime = field(default_factory=datetime.now)
    posted_date: Optional[date] = None
    balance_after: Optional[Decimal] = None
    reference_number: str = field(default_factory=lambda: f"REF{uuid.uuid4().hex[:6].upper()}")
    authorization_code: Optional[str] = None
    from_account: Optional[str] = None
    to_account: Optional[str] = None
    fee_amount: Decimal = field(default_factory=lambda: Decimal("0.00"))
    exchange_rate: float = 1.0
    original_amount: Optional[Decimal] = None
    original_currency: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def total_amount(self) -> Decimal:
        return self.amount + self.fee_amount
    
    @property
    def is_debit(self) -> bool:
        return self.transaction_type in ['withdrawal', 'payment', 'fee', 'transfer_out']
    
    @property
    def is_credit(self) -> bool:
        return self.transaction_type in ['deposit', 'credit', 'refund', 'transfer_in']
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "transaction_type": self.transaction_type,
            "amount": str(self.amount),
            "currency": self.currency,
            "description": self.description,
            "merchant": self.merchant,
            "merchant_category": self.merchant_category,
            "location": self.location,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "balance_after": str(self.balance_after) if self.balance_after else None,
            "reference_number": self.reference_number,
            "authorization_code": self.authorization_code,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "fee_amount": str(self.fee_amount),
            "total_amount": str(self.total_amount),
            "exchange_rate": self.exchange_rate,
            "original_amount": str(self.original_amount) if self.original_amount else None,
            "original_currency": self.original_currency,
            "is_debit": self.is_debit,
            "is_credit": self.is_credit,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

@dataclass
class LoanApplication:
    """Loan application model for banking products"""
    application_id: str = field(default_factory=lambda: f"LOAN_{uuid.uuid4().hex[:8].upper()}")
    customer_id: str = ""
    loan_type: str = "personal"  # personal, auto, mortgage, business
    requested_amount: Decimal = field(default_factory=lambda: Decimal("0.00"))
    currency: str = "USD"
    purpose: str = ""
    term_months: int = 0
    interest_rate: float = 0.0
    status: str = "pending"  # pending, approved, denied, withdrawn
    application_date: date = field(default_factory=date.today)
    decision_date: Optional[date] = None
    approved_amount: Optional[Decimal] = None
    monthly_payment: Optional[Decimal] = None
    collateral: Optional[str] = None
    employment_info: Dict[str, Any] = field(default_factory=dict)
    financial_info: Dict[str, Any] = field(default_factory=dict)
    credit_check_results: Dict[str, Any] = field(default_factory=dict)
    documents: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "application_id": self.application_id,
            "customer_id": self.customer_id,
            "loan_type": self.loan_type,
            "requested_amount": str(self.requested_amount),
            "currency": self.currency,
            "purpose": self.purpose,
            "term_months": self.term_months,
            "interest_rate": self.interest_rate,
            "status": self.status,
            "application_date": self.application_date.isoformat(),
            "decision_date": self.decision_date.isoformat() if self.decision_date else None,
            "approved_amount": str(self.approved_amount) if self.approved_amount else None,
            "monthly_payment": str(self.monthly_payment) if self.monthly_payment else None,
            "collateral": self.collateral,
            "employment_info": self.employment_info,
            "financial_info": self.financial_info,
            "credit_check_results": self.credit_check_results,
            "documents": self.documents,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

@dataclass 
class Card:
    """Banking card model (debit/credit cards)"""
    card_id: str = field(default_factory=lambda: f"CARD_{uuid.uuid4().hex[:8].upper()}")
    account_id: str = ""
    customer_id: str = ""
    card_number: str = ""  # Masked for security
    card_type: str = "debit"  # debit, credit, prepaid
    card_network: str = "visa"  # visa, mastercard, amex, discover
    expiry_date: str = ""  # MM/YY format
    status: str = "active"  # active, blocked, expired, cancelled
    daily_limit: Decimal = field(default_factory=lambda: Decimal("1000.00"))
    monthly_limit: Decimal = field(default_factory=lambda: Decimal("5000.00"))
    international_enabled: bool = True
    contactless_enabled: bool = True
    pin_set: bool = False
    activation_date: Optional[date] = None
    last_used: Optional[datetime] = None
    failed_attempts: int = 0
    features: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_id": self.card_id,
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "card_number": self.card_number,
            "card_type": self.card_type,
            "card_network": self.card_network,
            "expiry_date": self.expiry_date,
            "status": self.status,
            "daily_limit": str(self.daily_limit),
            "monthly_limit": str(self.monthly_limit),
            "international_enabled": self.international_enabled,
            "contactless_enabled": self.contactless_enabled,
            "pin_set": self.pin_set,
            "activation_date": self.activation_date.isoformat() if self.activation_date else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "failed_attempts": self.failed_attempts,
            "features": self.features,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# Utility functions for model management
def create_sample_customer() -> Customer:
    """Create a sample customer for testing"""
    address = Address(
        street="123 Main St",
        city="Anytown", 
        state="CA",
        zip_code="12345"
    )
    
    return Customer(
        first_name="John",
        last_name="Doe",
        email="john.doe@email.com",
        phone="(555) 123-4567",
        date_of_birth=date(1985, 6, 15),
        ssn="123-45-6789",
        address=address,
        credit_score=750,
        customer_since=date(2020, 1, 15),
        status=CustomerStatus.ACTIVE,
        risk_level=RiskLevel.LOW,
        kyc_status=KYCStatus.VERIFIED
    )

def create_sample_account(customer_id: str) -> Account:
    """Create a sample account for testing"""
    return Account(
        customer_id=customer_id,
        account_type="checking",
        account_number="1234567890",
        routing_number="123456789",
        balance=Decimal("2500.75"),
        available_balance=Decimal("2500.75"),
        status=AccountStatus.ACTIVE,
        opened_date=date(2020, 1, 20),
        overdraft_limit=Decimal("500.00"),
        interest_rate=0.05,
        monthly_fee=Decimal("12.00"),
        features=["online_banking", "mobile_app", "bill_pay"]
    )

def create_sample_transaction(account_id: str) -> Transaction:
    """Create a sample transaction for testing"""
    return Transaction(
        account_id=account_id,
        transaction_type="payment",
        amount=Decimal("45.67"),
        description="Coffee Shop Purchase",
        merchant="Starbucks",
        merchant_category="restaurants",
        status=TransactionStatus.COMPLETED,
        balance_after=Decimal("2455.08"),
        tags=["food", "beverage"]
    )

# Model registry for dynamic model creation
MODEL_REGISTRY = {
    "customer": Customer,
    "account": Account,
    "transaction": Transaction,
    "loan_application": LoanApplication,
    "card": Card,
    "address": Address
}

def create_model_instance(model_type: str, **kwargs) -> Any:
    """Create a model instance dynamically"""
    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model_class = MODEL_REGISTRY[model_type]
    return model_class(**kwargs)

def get_model_schema(model_type: str) -> Dict[str, Any]:
    """Get the schema for a model type"""
    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model_class = MODEL_REGISTRY[model_type]
    return {
        "model_type": model_type,
        "fields": [field.name for field in model_class.__dataclass_fields__.values()],
        "required_fields": [
            field.name for field in model_class.__dataclass_fields__.values() 
            if field.default == field.default_factory == dataclass.MISSING
        ]
    }
