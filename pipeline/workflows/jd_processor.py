from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.utils.text_processing import TextProcessingUtils


class JobDescriptionDataProcessor(WorkflowUnit):

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> PipelineStateManager:
        """
        Clean and preprocess the job description content
        """
        content = global_state.job_description
        content = TextProcessingUtils.process_content(content)

        global_state.processed_job_description = content.strip()
        return state, "Job description processed successfully"

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> bool:
        return (
            global_state.job_description and type(global_state.job_description) is str
        )
