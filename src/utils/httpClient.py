from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.gen import coroutine, Return

import json

@coroutine
def http_post_async(url, header, body):
    http_client = AsyncHTTPClient()
    request = HTTPRequest(url, method='POST', headers = header, body = json.dumps(body))
    response = yield http_client.fetch(request)
    raise Return(response.body)