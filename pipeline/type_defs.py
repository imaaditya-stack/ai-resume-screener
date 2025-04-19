from typing import TypedDict, List, NewType
from pydantic import BaseModel, Field, ConfigDict

# Define as a NewType instead of a class that extends List
MandatoryScreeningParams = NewType("MandatoryScreeningParams", List[str])


class OptionalScreeningParamsGroup(TypedDict):
    """Type definition for optional keyword groups"""

    name: str
    weight: int
    terms: List[str]


class JobDescriptionConfig(BaseModel):
    """Validated model for job description configuration"""

    distilled_description: str
    mandatory_keywords: List[str]  # Simplify to use plain List[str]
    optional_keywords: List[OptionalScreeningParamsGroup]
    years_of_experience: float = Field(default=0.0, ge=0.0)

    model_config = ConfigDict(arbitrary_types_allowed=True)
