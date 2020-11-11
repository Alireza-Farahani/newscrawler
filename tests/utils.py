import functools
import os

import scrapydo
from scrapy.http import TextResponse, Response

from definitions import TEST_RESOURCES_DIR


def fake_response(file_name, url="https://fake_response.com"):
    """:returns a scrapy :class:`Response` object, filled with the file content
    :param url: url that response is served from, not 'request url'.
    :param file_name: saved response file name. files should be in TEST_RESOURCES_DIR. see definitions.py
    """
    with open(os.path.join(TEST_RESOURCES_DIR, file_name), 'r') as file:
        body = file.read()
    return fake_response_by_body(body, url)


def fake_response_by_body(body: str, url="https://fake_response.com"):
    """:returns a scrapy :class:`Response` object, filled with the file content
    :param url: url that response is served from, not 'request url'.
    :param body: response body. Any valid html is acceptable
    """
    return TextResponse(url=url, body=body, encoding='utf-8')


def _retry(n: int):
    def retry_decorator(func):
        @functools.wraps(func)
        def function_wrapper(*args, **kwargs):
            for i in range(n):
                result = func(*args, **kwargs)
                if result:
                    return result
            raise ValueError(f'Cannot obtain a valid value after {n} tries.')

        return function_wrapper

    return retry_decorator


@_retry(3)
def real_response(url):
    scrapydo.setup()
    resp: Response = scrapydo.fetch(url, timeout=10)
    return resp if 200 <= resp.status < 300 else None
