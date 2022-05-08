# -*- coding: utf-8 -*-


import uuid
import pytest

from src.core import RQ
from cases.env import *


@pytest.fixture()
def admin_login(request):
    '''
    管理员登录
    '''
    rq = RQ(base_url=url)
    rq.request(
        'get',
        '/apis/rudder/v1/oauth2/admin',
        params={'password': admin_password}
    ).expect(200)

    access_token = rq.resp.json()['data']['access_token']
    rq.set_headers(authorization=f'Bearer {access_token}')

    request.cls.rq = rq
    return rq


@pytest.fixture()
def create_tenant(admin_login):
    '''
    创建租户
    '''
    tenant_title = str(uuid.uuid1())[0:6]

    rq = admin_login
    rq.request(
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

    reset_key = rq.resp.json()['data']['reset_key']
    tenant_id = rq.resp.json()['data']['tenant_id']
    rq.reset_key = reset_key
    rq.tenant_id = tenant_id

    return rq


@pytest.fixture()
def tenant_reset_password(create_tenant):
    '''
    重置租户密码
    '''
    rq = create_tenant

    return rq


@pytest.fixture()
def tenant_login(request):
    '''
    租户登录
    '''
    rq = RQ(base_url=url)
    rq.request(
        'get',
        f'/apis/security/v1/oauth/{tenant_id}/token',
        params={'grant_type': 'password',
                'username': tenant_user,
                'password': tenant_password}
    ).expect(200)

    access_token = rq.resp.json()['data']['access_token']
    rq.set_headers(authorization=f'Bearer {access_token}')

    request.cls.rq = rq
    return rq
