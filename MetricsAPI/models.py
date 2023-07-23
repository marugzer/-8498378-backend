#CandidateId:8498378

from dataclasses import dataclass

@dataclass
class AverageMetricDto:
    MonthYear: str=""
    Fcs: float = 0.0
    Rcsi: float = 0.0
    HealthAccess: float = 0.0
    MarketAccess: float = 0.0
    LivelihoodCoping: float = 0.0

@dataclass
class MetricDto:
    People: int = 0
    Prevalence: float = 0.0

@dataclass
class MetricsDto:
    Fcs: MetricDto
    Rcsi: MetricDto
    HealthAccess: MetricDto
    MarketAccess: MetricDto
    LivelihoodCoping: MetricDto

@dataclass
class ConvertedDto:
    Country: dict    
    Date: str    
    Metrics: MetricsDto

@dataclass
class ApiResponseDto:    
    Country: str
    StartDate: str
    EndDate :str
    ResultMetrics=[]
    Variance : float= 0.0

