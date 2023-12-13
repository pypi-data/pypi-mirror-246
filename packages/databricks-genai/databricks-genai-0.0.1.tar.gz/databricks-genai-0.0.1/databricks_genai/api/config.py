"""Wrapper around MAPI engine in MCLI."""

import logging
import os
from typing import Any, Callable, TypeVar

from databricks.sdk import WorkspaceClient
from mcli import config

_TCallable = TypeVar('_TCallable', bound=Callable[..., Any])  # pylint: disable=invalid-name

logger = logging.getLogger(__name__)


def get_me() -> str:
    """
    Get who is currently logged in.

    Returns:
        str: The name of the current user.
    """
    w = WorkspaceClient()
    return w.current_user.me().user_name


def configure_request(func: _TCallable) -> _TCallable:
    """
    Decorator that configures a default retry policy for all MAPI requests

    Args:
        func (Callable[..., Any]): The function that should be retried
    """

    def setup(*args, **kwargs):
        w = WorkspaceClient()
        ctx = w.dbutils.entry_point.getDbutils().notebook().getContext()
        api_url = ctx.apiUrl().get()
        api_token = ctx.apiToken().get()
        endpoint = f'{api_url}/api/2.0/genai-mapi/graphql'

        previous_api_key = os.getenv(config.MOSAICML_API_KEY_ENV)
        previous_endpoint = os.getenv(config.MOSAICML_API_ENDPOINT_ENV)

        logger.debug(
            "Setting up MAPI connection with api_token %s and endpoint %s",
            api_token, endpoint)

        os.environ[config.MOSAICML_API_KEY_ENV] = f'Bearer {api_token}'
        os.environ[config.MOSAICML_API_ENDPOINT_ENV] = endpoint

        res = func(*args, **kwargs)

        if previous_api_key:
            os.environ[config.MOSAICML_API_KEY_ENV] = previous_api_key
        if previous_endpoint:
            os.environ[config.MOSAICML_API_ENDPOINT_ENV] = previous_endpoint

        return res

    return setup
