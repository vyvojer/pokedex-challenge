import logging
from abc import ABC, abstractmethod
from typing import Any, TypedDict

import requests

logger = logging.getLogger(__name__)


class LoaderException(Exception):
    pass


class DefaultPageLoader:
    def __init__(self, url: str, **kwargs):
        self.url = url
        self.kwargs = kwargs

    def load(self) -> tuple[list[str], str | None]:
        """
        Loads data from a specified URL and parses the response.

        This method sends a GET request to the provided URL and handles potential
        request exceptions or non-successful HTTP response codes. If the request
        succeeds and the status code is 200, it then parses the JSON response.

        :raises LoaderException: If there is an error during the request or if the
                                 HTTP response status code is not 200.

        :return: A tuple containing a list of strings (parsed data) and an optional
                 string (additional parsed detail). This result depends on how the
                 JSON response is processed by the `parse_response` method.
        :rtype: tuple[list[str], str|None]
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
        entity_urls = [entity["url"] for entity in response_data["results"]]
        next_url = response_data["next"] if "next" in response_data else None
        return entity_urls, next_url


class DefaultEntityLoader:
    def __init__(self, url: str, **kwargs):
        self.url = url
        self.kwargs = kwargs

    def load(self) -> dict:
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
