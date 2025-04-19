import os
import pymupdf

from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.exceptions import PipelineFailedException


class ResumeParser(WorkflowUnit):

    def __init__(self, path: str):

        self.path = path

    @logger
    def execute_workflow_unit(
        self,
        state: PipelineStateManager,
        global_state: GlobalStateManager = None,
    ) -> PipelineStateManager:
        """
        Extract text from a PDF file using PyMuPDF
        """
        text = ""
        if not self.path.endswith(".pdf"):
            logger.info(f"File {self.path} is not a PDF file, skipping...")
            return state, "File is not a PDF file, skipping..."

        try:
            # Open the PDF file
            with pymupdf.open(self.path) as doc:
                # Extract text from each page
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

        if len(text) == 0:
            state.skip_pipeline_from_execution = True
            state.pipeline_skip_reason = "Cannot extract text from resume. This may be because the resume is a scanned PDF document. Please ensure the resume contains selectable text."
            return state, "Resume is empty, skipping pipeline..."

        state.raw_content_of_resume = text

        return state, "Resume parsed successfully"

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager = None
    ):
        if not os.path.exists(self.path):
            self.abort_workflow_unit_from_execution(f"File not found at {self.path}")

        if not self.path.endswith(".pdf"):
            raise PipelineFailedException(
                f"File `{self.path}` is not a PDF file, skipping..."
            )

        return True
