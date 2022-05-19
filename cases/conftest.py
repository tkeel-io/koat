# -*- coding: utf-8 -*-


import pytest
from requests_toolbelt.sessions import BaseUrlSession


from cases.env import admin_password, url, tenant_user, tenant_id
from src.helper import random_string
from src.helper import search as jq


@pytest.fixture()
def admin_login(request):
    '''
    管理员登录
    '''
    # 在测试运行前,使用 parametrize 传递参数,更新默认参数
    # 参考 test_tenant.py -> TestTenant

    payload = {'password': admin_password}
    if hasattr(request, 'name'):
        payload.update(request.param)

    bs = BaseUrlSession(base_url=url)
    resp = bs.get('/apis/rudder/v1/oauth2/admin', params=payload)
    assert resp.status_code == 200

    access_token = jq('data.access_token', resp.json())
    bs.headers.update(authorization=f'Bearer {access_token}')

    request.cls.bs = bs


@pytest.fixture()
def create_tenant(request, admin_login):
    '''
    创建租户空间
    '''
    tenant_title = random_string()

    payload = {
        'title': tenant_title,
        'auth_type': "internal",
        'admin': {
            'username': "admin",
            'nick_name': "admin"
        },
        'remark': ""
    }
    resp = request.cls.bs.post('/apis/security/v1/tenants', json=payload)
    assert resp.status_code == 200

    request.cls.tenant_id = jq('data.tenant_id', resp.json())
    request.cls.reset_key = jq('data.reset_key', resp.json())


@pytest.fixture()
def tenant_reset_password(request, create_tenant):
    '''
    重置租户密码
    '''
    reset_key = request.cls.reset_key

    payload = {
        'reset_key': reset_key,
        'new_password': "changeme"
    }

    resp = request.cls.bs.post('/apis/security/v1/oauth/rspwd', json=payload)
    assert resp.status_code == 200

    request.cls.username = jq('data.username', resp.json())
    request.cls.tenant_id = jq('data.tenant_id', resp.json())


@pytest.fixture()
def tenant_login(request, tenant_reset_password):
    '''
    租户登录
    '''
    # tenant_user = request.cls.username
    # tenant_id = request.cls.tenant_id

    bs = BaseUrlSession(base_url=url)

    payload = {
        'grant_type': 'password',
        'username': tenant_user,
        'password': 'changeme'
    }

    resp = bs.get(f'/apis/security/v1/oauth/{tenant_id}/token', params=payload)

    assert resp.status_code == 200

    access_token = jq('data.access_token', resp.json())
    bs.headers.update(authorization=f'Bearer {access_token}')

    request.cls.bs = bs
