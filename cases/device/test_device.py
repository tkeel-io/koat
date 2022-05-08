# -*- coding: utf-8 -*-


import uuid
import pytest


@pytest.mark.usefixtures("tenant_login")
class TestDevice():

    def test_create_templates(self):
        '''
        创建模版
        '''
        name = str(uuid.uuid1())[0:6]
        self.rq.request(
            'post',
            f'/apis/tkeel-device/v1/templates',
            json={'name': name, 'description': "这是一个测试摸版"}
        ).expect(200)
