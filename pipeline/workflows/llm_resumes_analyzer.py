import ollama
from pipeline.config import __MOCK_LLM_MODE__
from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.prompts.llm_analysis import PROMPT_V2
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.exceptions import PipelineFailedException
import json
import time


class LLMResumesAnalyzer(WorkflowUnit):
    @logger
    def execute_workflow_unit(
        self,
        state: PipelineStateManager,
        global_state: GlobalStateManager = None,
    ):

        resumes_str = "\n".join(
            [
                f"Resume {i+1}:\n{resume}"
                for i, resume in enumerate(global_state.resumes_for_llm_analysis)
            ]
        )

        if not global_state.job_description:
            raise PipelineFailedException(
                "Job description is not set. Please set the job description first."
            )

        try:
            prompt = PROMPT_V2.format(
                RESUMES=resumes_str,
                JOB_DESCRIPTION=global_state.job_description,
            )
        except Exception as e:
            raise PipelineFailedException(f"Error formatting prompt: {e}")

        with open("llm_resumes_analyzer_prompt.txt", "w") as f:
            f.write(prompt)

        if __MOCK_LLM_MODE__:
            time.sleep(5)
            with open("llm_resumes_analyzer_output.json", "r") as f:
                output_from_llm_analysis = f.read()

            try:
                output_from_llm_analysis = json.loads(output_from_llm_analysis)
                output_from_llm_analysis = json.dumps(output_from_llm_analysis)
            except json.JSONDecodeError:
                print("Failed to parse JSON, using raw string")
        else:
            output_from_llm_analysis = ollama.generate(
                model="qwen2.5-coder", prompt=prompt, format="json"
            ).response

        if not __MOCK_LLM_MODE__:
            with open("llm_resumes_analyzer_output.json", "w") as f:
                f.write(output_from_llm_analysis)

        global_state.output_from_llm_analysis = output_from_llm_analysis

        return state, global_state.output_from_llm_analysis

    def assert_prerequisites_for_workflow_unit(
        self,
        state: PipelineStateManager,
        global_state: GlobalStateManager = None,
    ):
        return (
            True
            if hasattr(global_state, "resumes_for_llm_analysis")
            and len(global_state.resumes_for_llm_analysis) > 0
            else False
        )
