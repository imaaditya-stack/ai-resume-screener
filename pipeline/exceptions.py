import traceback
from enum import Enum


class FailureType(Enum):
    """Enum to define failure types"""

    VALIDATION_ERROR = "VALIDATION_ERROR"  # Failed validation but not an exception
    PIPELINE_ERROR = "PIPELINE_ERROR"  # Expected pipeline error
    SYSTEM_ERROR = "SYSTEM_ERROR"  # Unexpected system error


class PipelineFailedException(Exception):
    def __init__(
        self,
        reason: str,
        workflow_unit_name: str = None,
        failure_type: FailureType = FailureType.PIPELINE_ERROR,
        exc: Exception = None,
    ):
        self.reason = reason
        self.workflow_unit_name = workflow_unit_name
        self.failure_type = failure_type
        self.original_exception = exc
        self.traceback = traceback.format_exc() if exc else None
        super().__init__(self._format_message())

    def __str__(self):
        return self._format_message()

    def _format_message(self):
        """Format the error message with detailed information about the failure.

        Returns:
            str: A formatted error message containing:
                - Failure type (VALIDATION_ERROR, PIPELINE_ERROR, or SYSTEM_ERROR)
                - Workflow unit name where the error occurred
                - Error reason/description
                - Original exception details if present
                - Stack trace if available
        """
        message_parts = [
            f"[{self.failure_type.value}]",
            f"Workflow Unit: {self.workflow_unit_name or 'Unknown Unit'}",
            f"Reason: {self.reason}",
        ]

        if self.traceback:
            message_parts.append(f"Stack Trace:\n{self.traceback}")

        return "\n".join(message_parts)

    def to_dict(self):
        return {
            "workflow_unit_name": self.workflow_unit_name,
            "reason": self.reason,
            "failure_type": self.failure_type.value,
            "error_details": self.error_details,
            "traceback": self.traceback,
        }
