from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.utils.text_processing import TextProcessingUtils


class ResumeDataProcessor(WorkflowUnit):

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager = None
    ) -> PipelineStateManager:
        """
        Clean and preprocess the resume content
        """
        content = TextProcessingUtils.process_content(state.raw_content_of_resume)

        state.processed_content_of_resume = content.strip()

        return state, "Resume processed successfully"

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager = None
    ) -> bool:
        return state.raw_content_of_resume and type(state.raw_content_of_resume) is str
