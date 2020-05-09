import os

from scrapy.http import TextResponse

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
