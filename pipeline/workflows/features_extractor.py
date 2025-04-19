from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
import re
from pipeline.decorators import logger


class DataExtractor(WorkflowUnit):

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> PipelineStateManager:
        """
        Extracts total years of experience, including decimal values and cases where only months are mentioned.
        """

        text = state.processed_content_of_resume

        # Pattern to capture decimal or whole number years
        years_pattern = (
            r"(\d+\.?\d*)\s*\+?\s*(?:years|year|yrs)\s*(?:of\s+experience|exp|working)?"
        )

        # Pattern to capture only months (to be converted into years)
        months_pattern = (
            r"(\d+)\s*(?:months|month|mo)\s*(?:of\s+experience|exp|working)?"
        )

        max_experience = 0.0

        # Find years of experience (supports decimals like "2.6 years")
        years_match = re.findall(years_pattern, text, re.IGNORECASE)
        if years_match:
            # Convert to float to handle decimals
            max_experience = max(map(float, years_match))

        # Find months of experience and convert to years
        months_match = re.findall(months_pattern, text, re.IGNORECASE)
        if months_match:
            # Convert months to fraction of a year
            months_experience = max(map(int, months_match)) / 12
            max_experience = max(max_experience, months_experience)

        state.extracted_working_exp = (
            round(max_experience, 2) if max_experience > 0 else 0.0
        )

        return state, state.extracted_working_exp

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ):
        return (
            state.processed_content_of_resume
            and type(state.processed_content_of_resume) is str
        )
