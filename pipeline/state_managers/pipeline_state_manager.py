from typing import List, Dict


class PipelineStateManager:
    """State manager for the pipeline."""

    __instance = None

    def __init__(self):
        # Content of the resume
        self.raw_content_of_resume: str = ""
        self.processed_content_of_resume: str = ""

        # Extracted Features
        self.extracted_working_exp: float = 0.0
        self.extracted_email: str = ""
        self.extracted_contact: str = ""

        # Missing mandatory keywords
        self.missing_mandatory_keywords: List[str] = []

        # Mandatory keyword matches
        self.mandatory_keyword_matches: List[str] = []

        # Optional keyword matches
        self.optional_keywords_score: float = 0.0
        self.mandatory_keywords_score: float = 0.0
        self.matched_optional_groups: Dict[str, List[str]] = {}

        # Score
        self.score: float = 0.0

        # Passed
        self.passed: bool = False

        # Semantic similarity score
        self.semantic_similarity_score: float = 0.0

        # Skip Pipeline Flag
        self.skip_pipeline_from_execution: bool = False
        self.pipeline_skip_reason: str = ""
