from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager


class PreScreeningValidator(WorkflowUnit):

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> PipelineStateManager:
        """Validate experience requirements and return appropriate message"""
        if state.extracted_working_exp == 0.0:
            message = "Failed to extract experience from resume, continuing with further evaluation..."
            state.skip_pipeline = True
            state.pipeline_skip_reason = message
            return state, message

        if (
            global_state.use_strict_experience_check
            and state.extracted_working_exp < global_state.working_exp_criteria
        ):
            message = f"Experience is less than the required experience! Required experience: {global_state.working_exp_criteria} years, but found experience: {state.extracted_working_exp} years"
            state.skip_pipeline = True
            state.pipeline_skip_reason = message
            return state, message

        return state, "Experience matched! Proceeding with further evaluation..."

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ):
        return True
