"""Base classes and utilities for agent tools."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, create_model


class BaseTool(ABC):
    """
    Abstract base class for agent tools.

    Tools should inherit from this class and implement the execute method.
    The input_model should be a Pydantic model defining the tool's parameters.
    """

    name: str
    description: str
    input_model: BaseModel

    def __call__(self, **kwargs: Any) -> str:
        """Execute the tool with validated input."""
        # Validate input using Pydantic model
        validated_input = self.input_model(**kwargs)
        return self.execute(validated_input)

    @abstractmethod
    def execute(self, input_data: BaseModel) -> str:
        """Execute the tool logic with validated input."""

    def get_schema(self) -> dict[str, Any]:
        """Return the JSON schema for the tool's input parameters."""
        return self.input_model.model_json_schema()


def tool(name: str, description: str, input_model: BaseModel):
    """
    Decorator to create a tool from a function.

    Args:
        name: Tool name
        description: Tool description
        input_model: Pydantic model for input validation

    Returns:
        Decorated function that implements the Tool protocol
    """

    def decorator(func):
        class FunctionTool(BaseTool):
            name = name
            description = description
            input_model = input_model

            def execute(self, input_data: BaseModel) -> str:
                return func(input_data)

        return FunctionTool()

    return decorator


def create_input_model(name: str, **field_definitions) -> BaseModel:
    """
    Create a Pydantic model for tool input validation.

    Args:
        name: Model name
        **field_definitions: Field definitions as (type, Field(...)) tuples

    Returns:
        Pydantic model class

    Example:
        from pydantic import Field
        ReadFileInput = create_input_model(
            "ReadFileInput",
            path=(str, Field(description="Path to the file to read"))
        )
    """
    return create_model(name, **field_definitions)
