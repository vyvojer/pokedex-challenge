import re
from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    """
    Abstract base class for data transformers.

    This class defines the interface for transformers that convert raw data from
    external sources into a format suitable for the application's data model.
    Concrete transformer implementations should inherit from this class and
    implement the transform method.
    """

    def __init__(self, data: dict, **kwargs: dict):
        """
        Initialize the transformer with data and optional parameters.

        Args:
            data: The raw data to transform
            **kwargs: Additional parameters to use during transformation
        """
        self.data = data
        self.kwargs = kwargs

    @abstractmethod
    def transform(self) -> dict:
        """
        Transform the raw data into a format suitable for the application.

        This method must be implemented by concrete transformer classes to
        convert the raw data into a format that can be used by the application's
        data model.

        Returns:
            The transformed data as a dictionary
        """
        raise NotImplementedError
