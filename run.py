from pipeline.pipeline import PipelineOrchestrator
from pipeline.workflows.validators import PreScreeningValidator
from pipeline.workflows.mandatory_params_matcher import MandatoryParamsMatcher
from pipeline.workflows.optional_params_matcher import OptionalParamsMatcher
from pipeline.workflows.score_aggregator import ScoreAggregator
from pipeline.workflows.resume_parser import ResumeParser
from pipeline.workflows.resume_data_processor import ResumeDataProcessor
from pipeline.workflows.features_extractor import DataExtractor
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.config import ROLE_MATCHING_DEFINITIONS, JOB_DESC_FOR_JAVA_DEVELOPER
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

storage_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./__storage__/JAVA")
)


def process_resume(file, storage_path, global_state):
    pipeline_orchestrator = PipelineOrchestrator(
        [
            ("Resume Parser", ResumeParser(path=os.path.join(storage_path, file))),
            ("Resume Data Processor", ResumeDataProcessor()),
            ("Data Extractor", DataExtractor()),
            ("Pre-screening Validator", PreScreeningValidator()),
            ("Mandatory Keywords Matcher", MandatoryParamsMatcher()),
            ("Optional Keywords Matcher", OptionalParamsMatcher()),
            ("Score Aggregator", ScoreAggregator()),
        ]
    )
    return pipeline_orchestrator.orchestrate(PipelineStateManager(), global_state)


def main():
    try:
        global_state = GlobalStateManager(
            job_role="JAVA_DEVELOPER",
            mandatory_screening_params=ROLE_MATCHING_DEFINITIONS["JAVA_DEVELOPER"][
                "mandatory"
            ],
            optional_screening_params=ROLE_MATCHING_DEFINITIONS["JAVA_DEVELOPER"][
                "optional_groups"
            ],
            job_description=JOB_DESC_FOR_JAVA_DEVELOPER,
        )
        results = []
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = [
                executor.submit(process_resume, file, storage_path, global_state)
                for file in os.listdir(storage_path)
            ]
            results = [future.result() for future in as_completed(futures)]
        return results
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    start_time = time.time()
    results = main()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
