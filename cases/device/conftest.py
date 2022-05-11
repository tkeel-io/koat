# -*- coding: utf-8 -*-


import pytest

from cases.env import *
from src.helper import random_string


@pytest.fixture()
def create_templates(request, tenant_login):
    '''
    创建模版
    '''
    name = random_string()
    request.cls.rq.http(
        'post',
        f'/apis/tkeel-device/v1/templates',
        json={'name': name, 'description': "这是一个测试摸版"}
    ).expect(200)
