from http import HTTPStatus
from typing import Generator

import requests


class TokenAuth(requests.auth.AuthBase):
    """
    TokenAuth offloads the complexity of managing the auth token header.
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["token"] = f"{self.token}"
        return request


def fetch_host_page(
    session: requests.Session,
    endpoint: str,
    limit: int = 1,
    skip: int = 0,
) -> list[dict] | None:
    """
    fetch_host_page does the hard work of retrieving a page of results from the api
    """
    try:
        result = session.post(endpoint, params={"skip": skip, "limit": limit}, data="")
        result.raise_for_status()
    except requests.HTTPError as err:
        if (
            # mypy happiness:
            # the HTTPError class doesn't guarantee a response object, though raise_for_status seems to
            err.response is not None
            and err.response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        ):
            # successfully reaching the end of the list results in a 500
            return None
        else:
            # we're otherwise in a bad situation, so reraise
            raise err

    # it might be useful to do some introspection on the result before returning the contents blindly
    # this could be a good next step for improving sanity in the system
    return result.json()


def fetch_hosts(
    endpoint: str,
    api_token: str,
    # default the limit to 1 so we don't need to add a second loop in the rest of the control flow
    # further batching the operation could be a good next step for optimization
    limit: int = 1,
    skip: int = 0,
) -> Generator[list[dict], None, None]:
    """
    fetch_hosts is a generator that retrieves hosts in a specified batch (limit) size

    the generator pattern should keep the memory footprint relatively small in the case
    that we suddenly have a lot more entries

    There's also an opportunity to leverage the etags present in the response headers.
    This could enable us to short-circuit downstream work by pruning the total number of responses.
    However, as always: https://wiki.c2.com/?PrematureOptimization
    """

    session = requests.sessions.Session()
    session.auth = TokenAuth(api_token)
    while (
        result := fetch_host_page(session, endpoint, limit=limit, skip=skip)
    ) is not None:
        yield result
        skip += limit

    return
