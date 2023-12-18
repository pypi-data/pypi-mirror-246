from cores.model.request import RequestObj

from typing import Dict


class Request(object):
    def __init__(self, token: str, content_type: str):
        if not token:
            self._token = str()  # to be defined
        else:
            self._token = token
        self._content_type = content_type
        self._header: Dict = {'Content-Type': self._content_type,
                              'Authorization': f'Bearer {self._token}'}
        self._request_object: RequestObj = None

    def request_generate(self) -> RequestObj:
        return self._request_object


class GetRequest(Request):

    def __init__(self, token: str, content_type: str):
        super().__init__(token, content_type)
        self.request_object = RequestObj(**dict(header=self._header))


class PostRequest(Request):

    def __init__(self, token: str, content_type: str, body: Dict):
        super().__init__(token, content_type)
        self.request_object = RequestObj(**dict(header=self._header,
                                                body=body))


class AttachRequest(Request):

    def __init__(self, token: str, content_type: str, body: Dict,  file_name: str = '', file_location: str = ''):
        super().__init__(token, content_type)
        file_upload = [('my_file', (file_name, open(file_location, 'rb')))]
        self.request_object = RequestObj(**dict(header=self._header,
                                                body=body,
                                                files=file_upload))
