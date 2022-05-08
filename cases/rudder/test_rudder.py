# -*- coding: utf-8 -*-


import uuid
import pytest


@pytest.mark.usefixtures("admin_login")
class TestRudder():

    @pytest.fixture()
    def test_create_tenant(self):
        '''
        创建租户空间
        '''
        tenant_title = str(uuid.uuid1())[0:6]
        self.rq.request(
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

        tenant_id = self.rq.resp.json()['data']['tenant_id']
        return tenant_id

    @pytest.mark.run(order=2)
    def test_edit_tenant(self, test_create_tenant):
        '''
        编辑租户空间
        '''
        tenant_id = test_create_tenant
        new_tenant_title = str(uuid.uuid1())[0:8]
        self.rq.request(
            'put',
            f'/apis/security/v1/tenants/{tenant_id}',
            json={
                'title': new_tenant_title,
                'remark': "这是一个修改版"
            }
        ).expect(200)

    @pytest.mark.run(order=1)
    def test_delete_tenant(self, test_create_tenant):
        '''
        删除租户空间
        '''
        tenant_id = test_create_tenant
        self.rq.request(
            'delete',
            f'/apis/security/v1/tenants/{tenant_id}',
        ).expect(200)
