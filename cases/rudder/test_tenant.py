# -*- coding: utf-8 -*-


import uuid
import pytest


@pytest.mark.usefixtures("create_tenant")
class TestTenant():

    def test_create_tenant(self):
        '''
        创建租户空间
        '''
        pass

    def test_tenant_reset_password(self,tenant_reset_password):
        '''
        重置租户密码
        '''
        pass

    @pytest.mark.run(order=1)
    def test_edit_tenant(self):
        '''
        编辑租户空间
        '''
        tenant_id = self.tenant_id
        new_tenant_title = str(uuid.uuid1())[0:8]
        self.rq.http(
            'put',
            f'/apis/security/v1/tenants/{tenant_id}',
            json={
                'title': new_tenant_title,
                'remark': "这是一个修改版"
            }
        ).expect(200)

    @pytest.mark.run(order=2)
    def test_delete_tenant(self):
        '''
        删除租户空间
        '''
        tenant_id = self.tenant_id
        self.rq.http(
            'delete',
            f'/apis/security/v1/tenants/{tenant_id}',
        ).expect(200)
