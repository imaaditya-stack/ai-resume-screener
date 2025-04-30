from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
import re
from pipeline.decorators import logger

EMAIL_REGEX = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
CONTACT_REGEX = r"(?<!\d)(\+?91[-\s]?)?[6789]\d{9}(?!\d)|(\+?91[-\s]?)?\(?[6789]\d{2}\)?[-\s]?\d{3}[-\s]?\d{4}(?!\d)"
YEARS_REGEX = (
    r"(\d+\.?\d*)\s*\+?\s*(?:years|year|yrs)\s*(?:of\s+experience|exp|working)?"
)
MONTHS_REGEX = r"(\d+)\s*(?:months|month|mo)\s*(?:of\s+experience|exp|working)?"


class DataExtractor(WorkflowUnit):

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> PipelineStateManager:
        """
        Extracts total years of experience, including decimal values and cases where only months are mentioned.
        """

        text = state.processed_content_of_resume

        max_experience = 0.0

        # Find years of experience (supports decimals like "2.6 years")
        years_match = re.findall(YEARS_REGEX, text, re.IGNORECASE)
        if years_match:
            # Convert to float to handle decimals
            max_experience = max(map(float, years_match))

        # Find months of experience and convert to years
        months_match = re.findall(MONTHS_REGEX, text, re.IGNORECASE)
        if months_match:
            # Convert months to fraction of a year
            months_experience = max(map(int, months_match)) / 12
            max_experience = max(max_experience, months_experience)

        state.extracted_working_exp = (
            round(max_experience, 2) if max_experience > 0 else 0.0
        )

        # Extract email address
        email_match = re.search(EMAIL_REGEX, text)
        if email_match:
            state.extracted_email = email_match.group(0)

        # Extract contact number
        contact_match = re.search(CONTACT_REGEX, text)
        if contact_match:
            state.extracted_contact = contact_match.group(0)

        return state, {
            "extracted_working_exp": state.extracted_working_exp,
            "extracted_email": state.extracted_email,
            "extracted_contact": state.extracted_contact,
        }

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ):
        return (
            state.processed_content_of_resume
            and type(state.processed_content_of_resume) is str
        )
