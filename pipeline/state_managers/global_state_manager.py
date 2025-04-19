import uuid
from typing import List
from pipeline.type_defs import MandatoryScreeningParams, OptionalScreeningParamsGroup


class GlobalStateManager:
    """Global state manager for the pipeline."""

    __instance = None

    def __init__(
        self,
        job_role: str,
        mandatory_screening_params: MandatoryScreeningParams = [],
        optional_screening_params: List[OptionalScreeningParamsGroup] = [],
        job_description: str = "",
    ):
        """Initialize the global state manager."""
        # Job role
        self.job_role: str = job_role

        # Screening Params
        self.use_partial_matching: bool = True
        self.use_case_sensitive: bool = False
        self.use_strict_experience_check: bool = False
        self.mandatory_screening_params: MandatoryScreeningParams = (
            mandatory_screening_params or []
        )
        self.optional_screening_params: List[OptionalScreeningParamsGroup] = (
            optional_screening_params or []
        )
        self.working_exp_criteria: float = 2.0  # Default minimum years of experience

        # Variables to store job description
        self.job_description: str = job_description

        # Variables to store results for LLM analysis
        self.resumes_for_llm_analysis: List[str] = []
        self.pipeline_run_id = str(uuid.uuid4())
        self.mandatory_screening_params_from_llm: MandatoryScreeningParams = []
        self.optional_screening_params_from_llm: List[OptionalScreeningParamsGroup] = []
        self.distilled_job_description_from_llm: str = ""
        self.years_of_experience_from_llm: float = 2.0

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(GlobalStateManager, cls).__new__(cls)

        return cls.__instance
