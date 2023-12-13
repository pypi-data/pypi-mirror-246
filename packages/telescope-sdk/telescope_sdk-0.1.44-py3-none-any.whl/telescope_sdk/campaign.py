from enum import Enum
from typing import List, Optional
from telescope_sdk.common import UserFacingDataType
from pydantic import BaseModel
from telescope_sdk.company import CompanySizeRange, FoundedYearRange, RevenueRange


class CampaignStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'ERROR'


class ExampleCompany(BaseModel):
    id: str
    name: str


class LocationType(str, Enum):
    city = 'city'
    state = 'state'


class LocationFilter(BaseModel):
    type: LocationType
    name: str


class IdealCustomerProfile(BaseModel):
    example_companies: List[ExampleCompany]
    job_titles: List[str]
    keywords: List[str] = []
    negative_keywords: List[str] = []
    country_codes: List[List[str]] = []
    employee_country_codes: List[List[str]] = []
    industries: List[str] = []
    company_size_range: CompanySizeRange = CompanySizeRange()
    company_types: List[str] = []
    founded_year_range: FoundedYearRange = FoundedYearRange()
    require_email: Optional[bool] = False
    hq_location_filters: Optional[LocationFilter] = []
    employee_location_filters: Optional[LocationFilter] = []
    revenue_range: Optional[RevenueRange] = RevenueRange()
    only_show_verified_emails: Optional[bool] = False
    hide_companies_in_another_campaign: Optional[bool] = False
    hide_leads_in_another_campaign: Optional[bool] = False


class Campaign(UserFacingDataType):
    name: str
    status: CampaignStatus
    sequence_id: Optional[str] = None
    outreach_enabled: Optional[bool] = None
    replenish: bool
    icp: IdealCustomerProfile
