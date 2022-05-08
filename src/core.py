# -*- coding: utf-8 -*-


from requests_toolbelt import sessions


class RQ(sessions.BaseUrlSession):

    base_url = None
    resp = None

    def __init__(self, base_url=None):
        super().__init__(base_url=None)
        self.verify = False
        self.timeout = (60, 300)
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        self.resp = super().request(method, url, *args, **kwargs)
        return self

    def set_headers(self, **headers):
        self.headers.update(headers)
        return self

    def expect(self, status_code):
        assert self.resp.status_code == status_code
        return self
