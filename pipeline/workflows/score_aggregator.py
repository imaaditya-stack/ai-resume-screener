from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager


class ScoreAggregator(WorkflowUnit):
    """Pipeline stage that calculates the final score based on keyword matching results."""

    @logger
    def execute_workflow_unit(
        self,
        state: PipelineStateManager,
        global_state: GlobalStateManager = None,
    ) -> PipelineStateManager:
        """Aggregate the scores from the mandatory and optional keyword matching results"""

        state.score = state.mandatory_keywords_score + state.optional_keywords_score

        return state, state.score

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager = None
    ) -> bool:
        """Validate that the state has mandatory keywords score and optional keywords score."""
        return hasattr(state, "mandatory_keywords_score") and hasattr(
            state, "optional_keywords_score"
        )
