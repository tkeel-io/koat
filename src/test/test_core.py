# -*- coding: utf-8 -*-


from src.core import RQ


rq = RQ(base_url='https://yande.re')


class TestCore():

    def test_request(self):
        rq.request(
            'get',
            '/post.json',
            params={'limit': 1}
        ).expect(200)

    def test_core(self):
        rq.request(
            'get',
            '/post.json',
            params={'limit': 1}
        )
        rq.expect(200)
        rq.set_headers(test='anything')

        assert rq.headers['test'] == 'anything'
