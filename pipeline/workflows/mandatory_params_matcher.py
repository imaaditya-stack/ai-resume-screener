from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.utils.keyword_matching import KeywordMatchingUtils


class MandatoryParamsMatcher(WorkflowUnit):

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> PipelineStateManager:
        """Check mandatory keywords and return results"""
        missing = []
        matched_keywords = []

        for keyword in global_state.mandatory_screening_params:
            exists, matched_text = KeywordMatchingUtils.regex_based_keyword_matcher(
                keyword=keyword,
                text=state.processed_content_of_resume,
                case_sensitive=global_state.use_case_sensitive,
                use_partial_matching=global_state.use_partial_matching,
            )
            matched_keyword = (
                matched_text if global_state.use_partial_matching else keyword
            )
            if not exists:
                missing.append(keyword)
            else:
                matched_keywords.append(matched_keyword.capitalize())

        state.mandatory_keyword_matches = matched_keywords
        state.missing_mandatory_keywords = missing
        state.passed = len(missing) == 0

        if state.passed:
            state.mandatory_keywords_score = 60
        else:
            state.skip_pipeline_from_execution = True
            state.pipeline_skip_reason = "Mandatory Parameters not matched. The resume is missing required skills which are mandatory for the role."

        return state, state.passed

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ):
        if not global_state.mandatory_screening_params:
            raise ValueError(
                "Mandatory Parameters not set. Please set the mandatory parameters in the global state."
            )

        return True
