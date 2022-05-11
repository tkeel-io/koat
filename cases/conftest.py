# -*- coding: utf-8 -*-


import pytest


from src.core import RQ
from cases.env import *
from src.helper import random_string


@pytest.fixture()
def admin_login(request):
    '''
    管理员登录
    '''

    # 在测试运行前使用 parametrize 传递参数
    # 参考 test_tenant.py -> TestTenant
    psw = request.param

    rq = RQ(base_url=url)
    rq.http(
        'get',
        '/apis/rudder/v1/oauth2/admin',
        params={'password': admin_password}
    ).expect(200)

    access_token = rq.jq('data.access_token')
    rq.set_headers(authorization=f'Bearer {access_token}')

    request.cls.rq = rq


@pytest.fixture()
def create_tenant(request, admin_login):
    '''
    创建租户空间
    '''
    tenant_title = random_string()

    request.cls.rq.http(
        'post',
        '/apis/security/v1/tenants',
        json={
            'title': tenant_title,
            'auth_type': "internal",
            'admin': {
                'username': "admin",
                'nick_name': "admin"
            },
            'remark': ""
        }
    ).expect(200)

    request.cls.tenant_id = request.cls.rq.jq('data.tenant_id')
    request.cls.reset_key = request.cls.rq.jq('data.reset_key')


@pytest.fixture()
def tenant_reset_password(request, create_tenant):
    '''
    重置租户密码
    '''
    reset_key = request.cls.reset_key

    request.cls.rq.http(
        'post',
        '/apis/security/v1/oauth/rspwd',
        json={
            'reset_key': reset_key,
            'new_password': "changeme"
        }

    ).expect(200)

    request.cls.username = request.cls.rq.jq('data.username')
    request.cls.tenant_id = request.cls.rq.jq('data.tenant_id')


@pytest.fixture()
def tenant_login(request, tenant_reset_password):
    '''
    租户登录
    '''
    # tenant_user = request.cls.username
    # tenant_id = request.cls.tenant_id

    rq = RQ(base_url=url)
    rq.http(
        'get',
        f'/apis/security/v1/oauth/{tenant_id}/token',
        params={'grant_type': 'password',
                'username': tenant_user,
                'password': 'changeme'}
    ).expect(200)

    access_token = rq.jq('data.access_token')
    rq.set_headers(authorization=f'Bearer {access_token}')

    request.cls.rq = rq
