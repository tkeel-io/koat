# -*- coding: utf-8 -*-


import uuid
import pytest

from cases.env import *


@pytest.fixture()
def create_templates(request, tenant_login):
    '''
    创建模版
    '''
    rq = tenant_login
    name = str(uuid.uuid1())[0:6]
    rq.request(
        'post',
        f'/apis/tkeel-device/v1/templates',
        json={'name': name, 'description': "这是一个测试摸版"}
    ).expect(200)

    request.cls.rq = rq
    request.cls.templates_id = '123'
    return rq
