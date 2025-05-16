import logging
from abc import ABC, abstractmethod
from typing import Any, TypedDict

import requests

logger = logging.getLogger(__name__)


class LoaderException(Exception):
    """
    Exception raised for errors that occur during data loading operations.

    This exception is used to wrap and propagate errors that occur when loading data
    from external sources, such as network errors or invalid responses.
    """

    pass


class DefaultPageLoader:
    """
    Default loader for paginated data from external APIs.

    This class handles loading data from a paginated API endpoint, parsing the response,
    and extracting entity URLs and pagination information.
    """

    def __init__(self, url: str, **kwargs):
        """
        Initialize the page loader with a URL and optional parameters.

        Args:
            url: The URL to load data from
            **kwargs: Additional parameters to use when loading data
        """
        self.url = url
        self.kwargs = kwargs

    def load(self) -> tuple[list[str], str | None]:
        """
        Loads the content of the specified URL, retrieves its response, and parses
        the data. Ensures proper logging and error handling when the page cannot
        be loaded or if a bad response is received.

        Raises:
            LoaderException: If there is an exception during the request or if the
                response status code is not 200.

        Returns:
            tuple[list[str], str | None]: Parsed data obtained from the response.
        """
        try:
            logger.info(f"Loading page.", extra={"url": self.url})
            response = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            logger.exception(e, extra={"url": self.url})
            raise LoaderException from e

        if response.status_code != 200:
            logger.error(
                f"Bad response status code",
                extra={
                    "url": self.url,
                    "status_code": response.status_code,
                    "response_text": response.text,
                },
            )
            raise LoaderException(response.text)

        return self.parse_response(response.json())

    def parse_response(self, response_data: dict) -> tuple[list[str], str | None]:
        """
        Parse the JSON response from the API.

        This method extracts entity URLs from the 'results' field and the URL for the next page
        from the 'next' field in the response data.

        Args:
            response_data: The JSON response data from the API

        Returns:
            A tuple containing a list of entity URLs and the URL for the next page (or None if there is no next page)
        """
        entity_urls = [entity["url"] for entity in response_data["results"]]
        next_url = response_data["next"] if "next" in response_data else None
        return entity_urls, next_url


class DefaultEntityLoader:
    """
    Default loader for individual entity data from external APIs.

    This class handles loading data for a specific entity from an API endpoint
    and returning the raw JSON response.
    """

    def __init__(self, url: str, **kwargs):
        """
        Initialize the entity loader with a URL and optional parameters.

        Args:
            url: The URL to load entity data from
            **kwargs: Additional parameters to use when loading data
        """
        self.url = url
        self.kwargs = kwargs

    def load(self) -> dict:
        """
        Load entity data from the specified URL.

        This method sends a GET request to the provided URL and handles potential
        request exceptions or non-successful HTTP response codes. If the request
        succeeds and the status code is 200, it returns the JSON response.

        Raises:
            LoaderException: If there is an error during the request or if the
                             HTTP response status code is not 200.

        Returns:
            The JSON response data as a dictionary
        """
        try:
            logger.info(f"Loading page.", extra={"url": self.url})
            response = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            logger.exception(e, extra={"url": self.url})
            raise LoaderException from e

        if response.status_code != 200:
            logger.error(
                f"Bad response status code",
                extra={
                    "url": self.url,
                    "status_code": response.status_code,
                    "response_text": response.text,
                },
            )
            raise LoaderException(response.text)

        return response.json()
