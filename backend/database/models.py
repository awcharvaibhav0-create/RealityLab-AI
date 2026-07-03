from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Business:
    id: str
    name: str
    type: str
    category: str
    location: str
    created_date: datetime
    updated_date: datetime
    status: str


@dataclass
class BusinessSettings:
    business_id: str
    currency: str
    language: str
    timezone: str
    preferred_forecast_horizon: int
    report_preferences: str
    privacy_settings: str


@dataclass
class Analysis:
    id: str
    business_id: str
    start_time: datetime
    version: str
    status: str
    end_time: Optional[datetime] = None
    confidence: Optional[int] = None


@dataclass
class Scenario:
    id: str
    analysis_id: str
    name: str
    description: Optional[str] = None
    estimated_investment: Optional[float] = None
    estimated_complexity: Optional[str] = None


@dataclass
class Forecast:
    id: str
    scenario_id: str
    month: int
    revenue: float
    expenses: float
    profit: float
    customers: int
    cash_flow: float


@dataclass
class Recommendation:
    id: str
    analysis_id: str
    winning_scenario_id: str
    overall_score: int
    confidence: int
    explanation: str
    trade_offs: str
    timestamp: datetime


@dataclass
class Report:
    id: str
    analysis_id: str
    report_metadata: str
    generation_time: datetime
    checksum: str
    version: str
    pdf_path: Optional[str] = None
    json_path: Optional[str] = None
    csv_path: Optional[str] = None


@dataclass
class Assumption:
    id: str
    analysis_id: str
    name: str
    value: float
    source: str
    confidence: int
    version: str


@dataclass
class KnowledgeVersion:
    id: str
    knowledge_package: str
    version: str
    created: datetime
    checksum: str
    status: str


@dataclass
class Feedback:
    id: str
    analysis_id: str
    implemented: bool
    user_satisfaction: str
    timestamp: datetime
    actual_monthly_revenue: Optional[float] = None
    actual_monthly_profit: Optional[float] = None
    comments: Optional[str] = None


@dataclass
class Learning:
    id: str
    analysis_id: str
    forecast_accuracy: float
    recommendation_success: float
    improvement_suggestions: str
    timestamp: datetime


@dataclass
class AuditLog:
    id: str
    action: str
    user_id: str
    details: str
    timestamp: datetime


@dataclass
class Event:
    id: str
    event_name: str
    payload: str
    timestamp: datetime
    analysis_id: Optional[str] = None


@dataclass
class Config:
    config_key: str
    config_value: str
    updated_at: datetime


@dataclass
class Cache:
    cache_key: str
    category: str
    payload: str
    expires_at: datetime
    created_at: datetime
