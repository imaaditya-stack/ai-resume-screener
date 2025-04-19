from concurrent.futures import ThreadPoolExecutor, as_completed
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.exceptions import PipelineFailedException
from typing import List, Tuple
from pipeline.decorators import logger


class WorkflowUnit:
    def execute_workflow_unit(self, state, global_state: GlobalStateManager = None):
        """
        Process the pipeline stage
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} should implement `execute_workflow_unit` method"
        )

    def assert_prerequisites_for_workflow_unit(
        self, state, global_state: GlobalStateManager = None
    ):
        raise NotImplementedError(
            f"{self.__class__.__name__} should implement `assert_prerequisites_for_workflow_unit` method"
        )

    def abort_workflow_unit_from_execution(self, reason):
        self.skip_pipeline_from_execution = True
        self.pipeline_skip_reason = reason
        raise PipelineFailedException(reason)


class ConcurrentWorkflowUnitsCluster:
    def __init__(self, workflow_units: List[WorkflowUnit]):
        self.workflow_units = workflow_units


class PipelineOrchestrator:
    def __init__(self, workflow_units: List[Tuple[str, WorkflowUnit]]):
        self.workflow_units = workflow_units
        self.stopped_at_workflow_unit = None
        self.stop_reason = None
        self.pipeline_status = None
        self.error_type = None
        self.max_workers = 4
        self.workflow_unit_name = None

    def set_failure(self, name: str, reason: str, exc: Exception = None):
        raise PipelineFailedException(
            reason=reason,
            workflow_unit_name=name,
            exc=exc,
        )

    def __process_workflow_unit(
        self,
        workflow_unit: WorkflowUnit,
        state: PipelineStateManager = None,
        global_state: GlobalStateManager = None,
    ):
        if not isinstance(workflow_unit, WorkflowUnit):
            raise ValueError(
                f"Workflow unit `{self.workflow_unit_name}` is not a valid workflow unit"
            )

        # Validate prerequisites for the workflow unit
        if workflow_unit.assert_prerequisites_for_workflow_unit(state, global_state):
            result = workflow_unit.execute_workflow_unit(state, global_state)
        else:
            self.set_failure(
                self.workflow_unit_name,
                "Prerequisites not met for workflow unit",
            )

        return result

    def orchestrate(
        self,
        state: PipelineStateManager = None,
        global_state: GlobalStateManager = None,
    ):

        # Guard Rails
        if not self.workflow_units:
            raise ValueError("Workflow units cannot be empty")

        if state is None:
            state = PipelineStateManager()  # Initialize the state if it is not provided

        if global_state is None:
            global_state = (
                GlobalStateManager()
            )  # Initialize the global state if it is not provided

        try:
            for __definition__, workflow_unit in self.workflow_units:

                __workflow_unit_name__ = (
                    __definition__ or workflow_unit.__class__.__name__
                )
                self.workflow_unit_name = __workflow_unit_name__
                if isinstance(workflow_unit, ConcurrentWorkflowUnitsCluster):
                    self.orchestrate_concurrent_cluster(
                        workflow_unit.workflow_units, state, global_state
                    )
                    continue

                self.__process_workflow_unit(
                    workflow_unit=workflow_unit,
                    state=state,
                    global_state=global_state,
                )

                # If the pipeline is skipped, stop the pipeline and resume for next data in the queue
                if state.skip_pipeline_from_execution:
                    break

        # Ignore pipeline failures which are expected and continue with next data in the queue
        except PipelineFailedException as e:
            pass

        # Handle pipeline failures which are not expected
        except Exception as e:
            self.set_failure(
                self.workflow_unit_name,
                f"Pipeline failed due to unexpected error: {str(e)}",
                exc=e,
            )
            raise e

        return state

    def orchestrate_concurrent_cluster(
        self,
        stages: List[Tuple[str, WorkflowUnit]],
        state,
        global_state: GlobalStateManager = None,
    ):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for __definition__, stage in stages:
                self.workflow_unit_name = __definition__

                future = executor.submit(
                    self.__process_workflow_unit,
                    workflow_unit=stage,
                    state=state,
                    global_state=global_state,
                )
                futures.append(future)

            for future in as_completed(futures):
                future.result()

        return state
