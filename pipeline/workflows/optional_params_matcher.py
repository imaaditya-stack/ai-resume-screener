from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.utils.keyword_matching import KeywordMatchingUtils


class OptionalParamsMatcher(WorkflowUnit):
    """Pipeline stage that checks for optional keyword groups and calculates scores."""

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> PipelineStateManager:
        """Calculate scores for optional keyword groups and update state"""

        optional_score = 0.0
        total_weight = 0
        found_groups = {}

        # Calculate experience factor for boosting
        experience_factor = min(1.5, 1 + (state.extracted_working_exp / 10))

        # First pass - calculate base scores without boost
        for group in global_state.optional_screening_params:
            group_name = group["name"]
            group_weight = group["weight"]
            total_weight += group_weight  # No factor here - just sum raw weights

            matched_terms = []
            for term in group["terms"]:
                exists, matched_text = KeywordMatchingUtils.regex_based_keyword_matcher(
                    keyword=term.strip(),
                    text=state.processed_content_of_resume,
                    case_sensitive=global_state.use_case_sensitive,
                    use_partial_matching=global_state.use_partial_matching,
                )
                if exists:
                    matched_terms.append(matched_text.capitalize())

            if matched_terms:
                optional_score += group_weight / len(matched_terms)
                found_groups[group_name] = matched_terms

        # Calculate base percentage without boost
        if total_weight > 0:
            base_percentage = optional_score / total_weight
        else:
            base_percentage = 0

        # Apply experience boost to the final percentage, not to individual weights
        boosted_percentage = min(1.0, base_percentage * experience_factor)

        # Scale to get final score out of 40 points
        normalized_score = boosted_percentage * 40
        # Essential cap to ensure we never exceed 40 points
        normalized_score = min(normalized_score, 40)

        # Update state with results
        state.optional_keywords_score = normalized_score
        state.matched_optional_groups = found_groups

        return state, state.optional_keywords_score

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> bool:
        """Validate that the state has processed content and optional keywords."""
        return (
            hasattr(state, "processed_content_of_resume")
            and state.processed_content_of_resume
            and hasattr(global_state, "optional_screening_params")
            and global_state.optional_screening_params
        )
