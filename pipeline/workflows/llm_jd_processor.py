from pipeline.decorators import logger
from pipeline.pipeline import WorkflowUnit
from pipeline.prompts.llm_jd_processing import PROMPT
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
import ollama
import json
import time
from pipeline.config import __MOCK_LLM_MODE__


class LLMJobDescriptionProcessor(WorkflowUnit):
    """Uses LLM to process and optimize the job description"""

    @logger
    def execute_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> PipelineStateManager:
        """Process the job description with an LLM"""

        # Get the job description from the state
        job_description = global_state.job_description

        prompt = PROMPT.format(JOB_DESCRIPTION=job_description)

        with open("llm_jd_processor_prompt.txt", "w") as f:
            f.write(prompt)

        if __MOCK_LLM_MODE__:
            time.sleep(5)
            with open("llm_jd_processor_output.json", "r") as f:
                output_from_llm = f.read()
        else:
            output_from_llm = ollama.generate(
                model="qwen2.5-coder", prompt=prompt, format="json"
            ).response

        # Parse the JSON response and update state
        try:
            output_from_llm_json = json.loads(output_from_llm)

            # Save to JSON file for debugging
            if not __MOCK_LLM_MODE__:
                with open("llm_jd_processor_output.json", "w") as f:
                    json.dump(output_from_llm_json, f)

            # Store in state object
            global_state.mandatory_screening_params = output_from_llm_json[
                "mandatory_keywords"
            ]
            global_state.optional_screening_params = output_from_llm_json[
                "optional_keywords"
            ]
            global_state.distilled_job_description_from_llm = output_from_llm_json[
                "distilled_description"
            ]
            global_state.working_exp_criteria = output_from_llm_json[
                "years_of_experience"
            ]

        except Exception as e:
            # Fallback to default keywords if parsing fails
            print(f"Error parsing LLM keyword output: {str(e)}")

        return state, {
            "distilled_jd": global_state.distilled_job_description_from_llm,
            "mandatory_keywords": global_state.mandatory_screening_params,
            "optional_keywords": global_state.optional_screening_params,
            "years_of_experience": global_state.working_exp_criteria,
        }

    def assert_prerequisites_for_workflow_unit(
        self, state: PipelineStateManager, global_state: GlobalStateManager
    ) -> bool:
        return (
            global_state.job_description and type(global_state.job_description) is str
        )
